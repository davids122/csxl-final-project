"""Tests for the equipment service"""

import datetime
from unittest.mock import create_autospec
from backend.entities.user_entity import UserEntity
from backend.models.StagedCheckoutRequest import StagedCheckoutRequest
from backend.models.equipment_checkout import EquipmentCheckout

from backend.models.equipment_checkout_request import EquipmentCheckoutRequest
from backend.models.user import User
from backend.test.services.reset_table_id_seq import reset_table_id_seq
from backend.entities.role_entity import RoleEntity
from backend.models.equipment_type import EquipmentType
from backend.models.role import Role
from backend.services.exceptions import (
    UserPermissionException,
)
from ....models.equipment import Equipment
from ....services.equipment import (
    DuplicateEquipmentCheckoutRequestException,
    EquipmentAlreadyCheckedOutException,
    EquipmentCheckoutNotFoundException,
    EquipmentCheckoutRequestNotFoundException,
    EquipmentService,
    EquipmentNotFoundException,
    WaiverNotSignedException,
)
from ....services.user import UserService
import pytest
from sqlalchemy.orm import Session

from .user_equipment_data import (
    equipment,
    quest_3,
    arduino,
    insert_fake_data,
    checkouts,
)
from ..user_data import user, ambassador


@pytest.fixture(autouse=True)
def equipment_service(session: Session):
    """This PyTest fixture is injected into each test parameter of the same name below.
    It constructs a new, empty EquipmentService object."""
    equipment_service = EquipmentService(session)
    return equipment_service


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Inserts fake data to the test session."""

    # Add user for testing purposes
    user_entity = UserEntity.from_model(user)
    session.add(user_entity)

    # Add ambassador role for testing permissions specific to ambassadors.
    ambassador_role: Role = Role(id=2, name="ambassadors")
    entity = RoleEntity.from_model(ambassador_role)
    session.add(entity)
    session.commit()
    reset_table_id_seq(session, RoleEntity, RoleEntity.id, 3)

    # Insert fake equipment data for testing
    insert_fake_data(session)
    session.commit()
    yield


def test_get_all(equipment_service: EquipmentService):
    """Tests that all equipment can be retrieved"""
    fetched_equipment = equipment_service.get_all()
    assert fetched_equipment is not None
    assert len(fetched_equipment) == len(equipment)
    assert isinstance(fetched_equipment[0], Equipment)


def test_update(equipment_service: EquipmentService):
    """Tests that an item can be updated"""
    changed_item = Equipment(
        equipment_id=1,
        model="Meta Quest 3",
        equipment_image="placeholder",
        condition=8,
        is_checked_out=True,
    )
    equipment_service._permission = create_autospec(equipment_service._permission)

    update = equipment_service.update(changed_item, ambassador)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.crud.checkout", "equipment"
    )

    assert isinstance(update, Equipment)
    assert update == changed_item


def test_update_not_authorized(equipment_service: EquipmentService):
    """Tests that an item cannot be updated when the user does not have ambassador permissions"""
    changed_item = Equipment(
        equipment_id=1,
        model="Meta Quest 3",
        equipment_image="placeholder",
        condition=8,
        is_checked_out=True,
    )
    equipment_service._permission = create_autospec(equipment_service._permission)
    try:
        equipment_service.update(changed_item, user)
    except Exception as e:
        assert True


def test_update_equipment_not_in_db(equipment_service: EquipmentService):
    """Tests that an error is thrown when the update method is called on an item that is not in the database."""
    changed_item = Equipment(
        equipment_id=100,
        model="Ipod Nano",
        equipment_image="placeholder",
        condition=6,
        is_checked_out=True,
    )

    equipment_service._permission = create_autospec(equipment_service._permission)

    try:
        update = equipment_service.update(changed_item, ambassador)
        pytest.fail()
    except Exception as e:
        assert True


def test_get_equipment_by_id(equipment_service: EquipmentService):
    """Tests that a specific equipment item can be retrieved given an id"""
    equipment_service._permission = create_autospec(equipment_service._permission)

    item = equipment_service.get_equipment_by_id(1, ambassador)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.view.checkout", "equipment"
    )

    assert item == quest_3


def test_get_equipment_by_id_not_in_db(equipment_service: EquipmentService):
    """
    Tests that EquipmentNotFoundException is thrown when the get_equipment_by_id method is called
    on an id that does not exist in the database
    """
    equipment_service._permission = create_autospec(equipment_service._permission)

    try:
        equipment_service.get_equipment_by_id(478473874, ambassador)
        pytest.fail()
    except EquipmentNotFoundException as e:
        assert True


def test_get_equipment_by_id_not_authorized(equipment_service: EquipmentService):
    """Tests that user cannot call get_equipment_by_id if they do not have ambassador permissions"""
    try:
        equipment_service.get_equipment_by_id(1, user)
        pytest.fail()
    except Exception as e:
        assert True


def test_get_all_equipment_is_correct(equipment_service: EquipmentService):
    """Tests that when all equipment is retrieved the fields are still correct"""
    fetched_equipment = equipment_service.get_all()
    assert fetched_equipment[0] == quest_3
    assert fetched_equipment[1] == arduino


def test_get_all_types(equipment_service: EquipmentService):
    """Tests that all equipment properly converted to equipment type"""
    fetched_equipment_types = equipment_service.get_all_types()
    assert fetched_equipment_types is not None
    assert isinstance(fetched_equipment_types[0], EquipmentType)


def test_get_all_types_inventory_correct(equipment_service: EquipmentService):
    """Tests for correct num_available for each equipment type"""
    fetched_equipment_types = equipment_service.get_all_types()
    assert fetched_equipment_types[0].num_available == 1
    assert fetched_equipment_types[1].num_available == 2


def test_get_all_types_when_zero_available(equipment_service: EquipmentService):
    """Tests for correct num_available when equipment is checked out"""
    # first update database so Meta Quest 3 is checked out
    changed_item = Equipment(
        equipment_id=1,
        model="Meta Quest 3",
        equipment_image="placeholder",
        condition=8,
        is_checked_out=True,
    )
    equipment_service._permission = create_autospec(equipment_service._permission)

    update = equipment_service.update(changed_item, ambassador)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.crud.checkout", "equipment"
    )

    _ = equipment_service.update(changed_item, ambassador)

    fetched_equipment_types = equipment_service.get_all_types()
    assert fetched_equipment_types[1].num_available == 0


def test_get_all_requests(equipment_service: EquipmentService):
    """Tests that get_all_requests returns correct number of requests"""

    equipment_service._permission = create_autospec(equipment_service._permission)

    fetched_requests = equipment_service.get_all_requests(ambassador)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.view.checkout", "equipment"
    )

    assert len(fetched_requests) == 2


def test_get_all_requests_not_authorized(equipment_service: EquipmentService):
    """Tests that a user cannot get all checkout requests"""
    equipment_service._permission = create_autospec(equipment_service._permission)
    try:
        equipment_service.get_all_requests(user)

    except Exception as e:
        assert True


def test_get_all_requests_returns_correct_requests(equipment_service: EquipmentService):
    """Tests that get_all_requests returns the correct checkout requests"""
    equipment_service._permission = create_autospec(equipment_service._permission)

    fetched_requests = equipment_service.get_all_requests(ambassador)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.view.checkout", "equipment"
    )

    assert (
        fetched_requests[0].model == "Meta Quest 3"
        and fetched_requests[0].pid == 111111111
    )
    assert (
        fetched_requests[1].model == "Arduino Uno"
        and fetched_requests[1].pid == 999999999
    )


def test_delete_request(equipment_service: EquipmentService):
    """Tests that delete_request properly deletes a checkout request"""

    to_delete = EquipmentCheckoutRequest(
        user_name="Sally Student", model="Meta Quest 3", pid=111111111
    )
    equipment_service._permission = create_autospec(equipment_service._permission)

    equipment_service.delete_request(ambassador, to_delete)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.crud.checkout", "equipment"
    )

    requests = equipment_service.get_all_requests(ambassador)

    assert len(requests) == 1


def test_delete_requests_not_authorized(equipment_service: EquipmentService):
    """Tests that a checkout request cannot be deleted when the user does not have ambassador permissions"""
    to_delete = EquipmentCheckoutRequest(
        user_name="Sally Student", model="Meta Quest 3", pid=111111111
    )
    equipment_service._permission = create_autospec(equipment_service._permission)

    try:
        equipment_service.delete_request(user, to_delete)
    except Exception as e:
        assert True


def test_get_requested_equipment(equipment_service: EquipmentService):
    """Tests for correct available equipment for request"""
    equipment_service._permission = create_autospec(equipment_service._permission)
    available_equipment = equipment_service.get_equipment_for_request(
        ambassador, "Meta Quest 3"
    )

    assert len(available_equipment) == 1
    assert isinstance(available_equipment[0], Equipment)


def test_get_requested_equipment_none_available(equipment_service: EquipmentService):
    """Tests for return of empty list for no available equipment"""
    equipment_service._permission = create_autospec(equipment_service._permission)
    available_equipment = equipment_service.get_equipment_for_request(
        ambassador, "Oculus"
    )

    assert len(available_equipment) == 0


def test_waiver_not_signed_exception(equipment_service: EquipmentService):
    """Tests a WaiverNotSignedException is thrown"""

    request = EquipmentCheckoutRequest(
        user_name="Kris", model="Meta Quest 3", pid=111111111
    )
    user = User(
        id=3,
        pid=111111111,
        onyen="user",
        email="user@unc.edu",
        first_name="Sally",
        last_name="Student",
        pronouns="She / They",
        signed_equipment_wavier=False,
    )
    try:
        equipment_service.add_request(request, user)
    except WaiverNotSignedException as e:
        assert True


def test_duplicate_request_exception(equipment_service: EquipmentService):
    """Tests a DuplicateEquipmentCheckoutRequestException is thrown"""

    request = EquipmentCheckoutRequest(
        user_name="Kris", model="Meta Quest 3", pid=111111111
    )
    request_two = EquipmentCheckoutRequest(
        user_name="Kris", model="Meta Quest 3", pid=111111111
    )
    user = User(
        id=3,
        pid=111111111,
        onyen="user",
        email="user@unc.edu",
        first_name="Sally",
        last_name="Student",
        pronouns="She / They",
        signed_equipment_wavier=True,
    )

    try:
        equipment_service.add_request(request, user)
        equipment_service.add_request(request_two, user)
    except DuplicateEquipmentCheckoutRequestException as e:
        assert True


def test_equipment_request_not_found(equipment_service: EquipmentService):
    """Tests a EquipmentCheckoutRequestNotFoundException is thrown"""

    equipment_service._permission = create_autospec(equipment_service._permission)

    request = EquipmentCheckoutRequest(
        user_name="Kris", model="Meta Quest 3", pid=123456789
    )

    try:
        equipment_service.delete_request(ambassador, request)
    except EquipmentCheckoutRequestNotFoundException as e:
        assert True


def test_add_request(equipment_service: EquipmentService):
    """Tests adding a request properly creates and adds equipment request"""

    request = EquipmentCheckoutRequest(
        user_name="Kris", model="Meta Quest 3", pid=222222222
    )

    request = equipment_service.add_request(request, ambassador)
    assert isinstance(request, EquipmentCheckoutRequest)

def test_add_request_while_staged_request_exists(equipment_service: EquipmentService):
    """Tests that a user cannot add a checkout request if they already have a staged request."""

    req = EquipmentCheckoutRequest(
        user_name="baller", model="Arduino Uno", pid=999999999
    )

    try: 
        equipment_service.add_request(req, ambassador)
        assert False
    except DuplicateEquipmentCheckoutRequestException as e:
        assert True


def test_update_wavier_signed_field_unsigned(equipment_service: EquipmentService):
    """Tests that the service properly updates the waiver signed field when its unsigned."""

    updated_user = equipment_service.update_waiver_signed_field(user)
    assert updated_user.signed_equipment_wavier == True


def test_update_wavier_signed_field_user_not_found(equipment_service: EquipmentService):
    root = User(
        id=1,
        pid=454545455,
        onyen="Saul Goodman",
        email="kevinG@unc.edu",
        first_name="Brent",
        last_name="Munsell",
        pronouns="She / Her / Zhe",
        signed_equipment_wavier=False,
    )

    try:
        root = equipment_service.update_waiver_signed_field(root)

    except Exception as e:
        assert True


def test_get_all_staged_requests(equipment_service: EquipmentService):
    """Tests that get_all_staged_requests returns the correct staged requests"""

    equipment_service._permission = create_autospec(equipment_service._permission)

    fetched_requests = equipment_service.get_all_staged_requests(ambassador)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.view.checkout", "equipment"
    )

    assert len(fetched_requests) == 2


def test_create_staged_request(equipment_service: EquipmentService):
    """Tests that create_staged_request can create a new staged request"""

    equipment_service._permission = create_autospec(equipment_service._permission)

    stage = StagedCheckoutRequest(
        user_name="Lebron James", model="equipment", pid=232323232, id_choices=[1]
    )

    stage = equipment_service.create_staged_request(ambassador, stage)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.crud.checkout", "equipment"
    )

    assert isinstance(stage, StagedCheckoutRequest)


def test_create_staged_request_not_authorized(equipment_service: EquipmentService):
    """Tests that staged request cannot be created when the user does not have ambassador permissions"""

    stage = StagedCheckoutRequest(
        user_name="Lebron James", model="equipment", pid=232323232, id_choices=[1]
    )

    try:
        equipment_service.create_staged_request(user, stage)
        pytest.fail()
    except Exception as e:
        assert True


def test_delete_staged_request(equipment_service: EquipmentService):
    """Tests that delete_staged_request properly deletes a staged request"""

    to_delete = StagedCheckoutRequest(
        user_name="Sally Student", model="Meta Quest 3", pid=111111111, id_choices=[5]
    )
    equipment_service._permission = create_autospec(equipment_service._permission)

    equipment_service.delete_staged_request(ambassador, to_delete)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.crud.checkout", "equipment"
    )

    requests = equipment_service.get_all_staged_requests(ambassador)

    assert len(requests) == 1


def test_delete_staged_request_not_authorized(equipment_service: EquipmentService):
    """Tests that a staged request cannot be deleted when the user does not have ambassador permissions"""
    to_delete = StagedCheckoutRequest(
        user_name="Sally Student", model="equipment", pid=111111111, id_choices=[5]
    )
    equipment_service._permission = create_autospec(equipment_service._permission)

    try:
        equipment_service.delete_staged_request(user, to_delete)
    except Exception as e:
        assert True


def test_delete_staged_request_not_found(equipment_service: EquipmentService):
    """Tests that a StagedCheckoutRequestNotFoundException is thrown"""

    equipment_service._permission = create_autospec(equipment_service._permission)

    to_delete = StagedCheckoutRequest(
        user_name="Lebron James", model="equipment", pid=232323232, id_choices=[1]
    )

    try:
        equipment_service.delete_staged_request(ambassador, to_delete)
    except Exception as e:
        assert True


def test_get_all_active_checkouts(equipment_service: EquipmentService):
    """Tests that get_all_active_checkouts returns the correct checkouts"""
    equipment_service._permission = create_autospec(equipment_service._permission)

    fetched_checkouts = equipment_service.get_all_active_checkouts(ambassador)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.view.checkout", "equipment"
    )

    assert fetched_checkouts[0] == checkouts[0]
    assert fetched_checkouts[1] == checkouts[1]


def test_get_all_active_checkouts_does_not_return_inactive_checkouts(
    equipment_service: EquipmentService,
):
    """test_get_all_active_checkouts_does_not_return_inactive_checkouts"""
    equipment_service._permission = create_autospec(equipment_service._permission)

    fetched_checkouts = equipment_service.get_all_active_checkouts(ambassador)

    equipment_service._permission.enforce.assert_called_with(
        ambassador, "equipment.view.checkout", "equipment"
    )

    assert len(fetched_checkouts) == 5


def test_get_all_active_checkouts_not_authorized(equipment_service: EquipmentService):
    """Tests that active checkouts cannot be viewed when the user does not have ambassador permissions"""
    equipment_service._permission = create_autospec(equipment_service._permission)

    try:
        equipment_service.get_all_active_checkouts(user)
    except Exception as e:
        assert True


def test_create_checkout(equipment_service: EquipmentService):
    """Tests that create_checkout can create a new checkout"""
    equipment_service._permission = create_autospec(equipment_service._permission)

    to_add = EquipmentCheckout(
        user_name="Lebron James",
        pid=232323232,
        equipment_id=1,
        model="Meta Quest 3",
        is_active=True,
        started_at=datetime.datetime.now(),
        end_at=datetime.datetime.now(),
    )

    to_add = equipment_service.create_checkout(to_add, ambassador)

    # equipment_service._permission.enforce.assert_called_with(
    #     ambassador, "equipment.create_checkout", "equipment"
    # )

    assert isinstance(to_add, EquipmentCheckout)


def test_create_checkout_adds_to_active_checkouts(equipment_service: EquipmentService):
    """
    Tests that when create_checkout adds a checkout with is_active=True it shows up
    when get_all_active_checkouts is called
    """
    equipment_service._permission = create_autospec(equipment_service._permission)

    to_add = EquipmentCheckout(
        user_name="Tyrese Haliburton",
        pid=123456789,
        equipment_id=2,
        model="Arduino Uno",
        is_active=True,
        started_at=datetime.datetime.now(),
        end_at=datetime.datetime.now(),
    )

    equipment_service.create_checkout(to_add, ambassador)

    # equipment_service._permission.enforce.assert_called_with(
    #     ambassador, "equipment.create_checkout", "equipment"
    # )

    fetched_checkouts = equipment_service.get_all_active_checkouts(ambassador)
    assert len(fetched_checkouts) == 6
    assert fetched_checkouts[5] == to_add


def test_create_checkout_does_not_add_inactive_checkout_to_active_checkouts(
    equipment_service: EquipmentService,
):
    """
    Tests that when create_checkout adds a checkout with is_active=False it does not
    show up when get_all_active_checkouts is called
    """
    equipment_service._permission = create_autospec(equipment_service._permission)

    to_add = EquipmentCheckout(
        user_name="Brent Munsell",
        pid=666666666,
        equipment_id=3,
        model="Arduino Uno",
        is_active=False,
        started_at=datetime.datetime.now(),
        end_at=datetime.datetime.now(),
    )

    equipment_service.create_checkout(to_add, ambassador)

    # equipment_service._permission.enforce.assert_called_with(
    #     ambassador, "equipment.create_checkout", "equipment"
    # )

    fetched_checkouts = equipment_service.get_all_active_checkouts(ambassador)
    assert len(fetched_checkouts) == 5
    assert fetched_checkouts[0] == checkouts[0]
    assert fetched_checkouts[1] == checkouts[1]


def test_create_checkout_not_authorized(equipment_service: EquipmentService):
    """Tests that checkout cannot be created when the user does not have ambassador permissions"""

    to_add = EquipmentCheckout(
        user_name="Drake",
        pid=987654321,
        equipment_id=23,
        model="book",
        is_active=True,
        started_at=datetime.datetime.now(),
        end_at=datetime.datetime.now(),
    )

    try:
        equipment_service.create_checkout(to_add, user)
        pytest.fail()
    except Exception as e:
        assert True


def test_create_checkout_updates_is_checked_out(equipment_service: EquipmentService):
    """Tests that create_checkout updates the is_checked_out field of the item being checked out"""
    equipment_service._permission = create_autospec(equipment_service._permission)

    to_add = EquipmentCheckout(
        user_name="Lebron James",
        pid=232323232,
        equipment_id=1,
        model="Meta Quest 3",
        is_active=True,
        started_at=datetime.datetime.now(),
        end_at=datetime.datetime.now(),
    )

    to_add = equipment_service.create_checkout(to_add, ambassador)

    equipment_item = equipment_service.get_equipment_by_id(
        to_add.equipment_id, ambassador
    )
    assert equipment_item.is_checked_out == True


def test_create_checkout_does_not_work_on_checked_out_equipment(
    equipment_service: EquipmentService,
):
    """
    Tests that create_checkout throws an error when the item to be checked out
    is already checked out
    """
    equipment_service._permission = create_autospec(equipment_service._permission)

    to_add = EquipmentCheckout(
        user_name="Michael Kidd-Gilchrist",
        pid=454545676,
        equipment_id=4,
        model="Arduino Uno",
        is_active=True,
        started_at=datetime.datetime.now(),
        end_at=datetime.datetime.now(),
    )

    try:
        equipment_service.create_checkout(to_add, ambassador)
        pytest.fail()
    except EquipmentAlreadyCheckedOutException as e:
        assert True


def test_return_checkout_updates_is_active(equipment_service: EquipmentService):
    """Tests that return_checkout changes the is_active field in the given checkout to False"""
    equipment_service._permission = create_autospec(equipment_service._permission)

    returned_item = equipment_service.return_checkout(checkouts[1], ambassador)

    assert not returned_item.is_active


def test_return_checkout_changes_end_time(equipment_service: EquipmentService):
    """
    Tests that return_checkout changes end_at field of the checkout
    This test only checks that the end time changes, checking that it changes
    to the correct time will need to be done manually
    """
    equipment_service._permission = create_autospec(equipment_service._permission)

    end_time = checkouts[3].end_at

    changed_end_time = equipment_service.return_checkout(
        checkouts[3], ambassador
    ).end_at

    assert end_time != changed_end_time


def test_return_checkout_changes_equipment_entity(equipment_service: EquipmentService):
    """
    Tests that return_checkout changes the is_checked_out field of the equipment
    item that is being returned
    """
    equipment_service._permission = create_autospec(equipment_service._permission)

    equipment_service.return_checkout(checkouts[4], ambassador)

    updated_equipment_item: Equipment = equipment_service.get_equipment_by_id(
        checkouts[4].equipment_id, ambassador
    )
    assert not updated_equipment_item.is_checked_out


def test_return_checkout_error_if_checkout_not_active(
    equipment_service: EquipmentService,
):
    """Tests that return_checkout raises an Exception if the checkout to be returned is not active"""
    equipment_service._permission = create_autospec(equipment_service._permission)

    try:
        equipment_service.return_checkout(checkouts[2], ambassador)
        pytest.fail()
    except Exception as e:
        assert True


def test_return_checkout_error_if_not_in_db(equipment_service: EquipmentService):
    """
    Tests that return_checkout raises EquipmentCheckoutNotFoundException if checkout
    to be returned is not found in the database
    """
    equipment_service._permission = create_autospec(equipment_service._permission)

    to_return = EquipmentCheckout(
        user_name="Darius Garland",
        pid=222333444,
        equipment_id=1,
        model="Meta Quest 3",
        is_active=True,
        started_at=datetime.datetime.now(),
        end_at=datetime.datetime.now(),
    )

    try:
        equipment_service.return_checkout(to_return, ambassador)
        pytest.fail()
    except EquipmentCheckoutNotFoundException as e:
        assert True


def test_return_checkout_not_authorized(equipment_service: EquipmentService):
    """Tests that checkout cannot be returned when user does not have ambassador permissions"""

    try:
        equipment_service.return_checkout(checkouts[1], user)
        pytest.fail()
    except Exception as e:
        assert True

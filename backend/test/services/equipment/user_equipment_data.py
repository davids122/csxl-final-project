"""Mock data for equipment testing.

"""

import pytest
from sqlalchemy.orm import Session
from backend.entities.equipment_checkout_entity import EquipmentCheckoutEntity
from backend.entities.equipment_checkout_request_entity import (
    EquipmentCheckoutRequestEntity,
)
from backend.entities.permission_entity import PermissionEntity
from backend.entities.staged_checkout_request_entity import StagedCheckoutRequestEntity
from backend.entities.user_entity import UserEntity
from backend.models.StagedCheckoutRequest import StagedCheckoutRequest
from backend.models.equipment_checkout_request import EquipmentCheckoutRequest
from datetime import datetime

from backend.models.permission import Permission
from backend.test.services.role_data import ambassador_role
from ..reset_table_id_seq import reset_table_id_seq
from ....entities.equipment_entity import EquipmentEntity
from ....models.equipment import Equipment
from ....models.equipment_checkout import EquipmentCheckout
from enum import Enum


__authors__ = ["Nicholas Mountain, Jacob Brown, Ayden Franklin"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class DeviceType(Enum):
    META_QUEST_3 = "https://s7d1.scene7.com/is/image/dmqualcommprod/meta-quest-3-1?$QC_Responsive$&fmt=png-alpha"

    ARDUINO_UNO = (
        "https://www.circuitbasics.com/wp-content/uploads/2020/05/Arduino-Uno.png"
    )


quest_3 = Equipment(
    equipment_id=1,
    model="Meta Quest 3",
    equipment_image=DeviceType.META_QUEST_3.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)
arduino = Equipment(
    equipment_id=2,
    model="Arduino Uno",
    equipment_image=DeviceType.ARDUINO_UNO.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

arduino2 = Equipment(
    equipment_id=3,
    model="Arduino Uno",
    equipment_image=DeviceType.ARDUINO_UNO.value,
    condition=10,
    is_checked_out=False,
    condition_notes=[],
    checkout_history=[],
)

arduino3 = Equipment(
    equipment_id=4,
    model="Arduino Uno",
    equipment_image=DeviceType.ARDUINO_UNO.value,
    condition=10,
    is_checked_out=True,
    condition_notes=[],
    checkout_history=[],
)

quest_3_two = Equipment(
    equipment_id=5,
    model="Meta Quest 3",
    equipment_image=DeviceType.META_QUEST_3.value,
    condition=9,
    is_checked_out=True,
    condition_notes=["Lights on fire whenever it is turned on."],
    checkout_history=[111111111],
)

arduino4 = Equipment(
    equipment_id=6,
    model="Arduino Uno",
    equipment_image=DeviceType.ARDUINO_UNO.value,
    condition=10,
    is_checked_out=True,
    condition_notes=[],
    checkout_history=[],
)

arduino5 = Equipment(
    equipment_id=7,
    model="Arduino Uno",
    equipment_image=DeviceType.ARDUINO_UNO.value,
    condition=10,
    is_checked_out=True,
    condition_notes=[],
    checkout_history=[],
)

arduino6 = Equipment(
    equipment_id=8,
    model="Arduino Uno",
    equipment_image=DeviceType.ARDUINO_UNO.value,
    condition=10,
    is_checked_out=True,
    condition_notes=[],
    checkout_history=[],
)

# checkout_request_quest_3 = EquipmentCheckoutRequest(
#     user_name="Sally Student", model="Meta Quest 3", pid=111111111
# )

checkout_request_arduino = EquipmentCheckoutRequest(
    user_name="Rhonda Root", model="Arduino Uno", pid=999999999
)

staged_checkout_request_quest_3 = StagedCheckoutRequest(
    user_name="Sally Student", model="Meta Quest 3", pid=111111111, id_choices=[5]
)

staged_checkout_request_arduino = StagedCheckoutRequest(
    user_name="Rhonda Root", model="Arduino Uno", pid=999999999, id_choices=[2]
)

ambassador_permission_crud_checkout = Permission(
    id=4, action="equipment.crud.checkout", resource="equipment"
)

ambassador_permission_view_checkout = Permission(
    id=5, action="equipment.view.checkout", resource="equipment"
)

equipment_checkout1 = EquipmentCheckout(
    user_name="Amy",
    pid=999999999,
    equipment_id=2,
    model="Arduino Uno",
    is_active=True,
    started_at=datetime.now(),
    end_at=datetime.now(),
)

equipment_checkout2 = EquipmentCheckout(
    user_name="Sally",
    pid=111111111,
    equipment_id=5,
    model="Meta Quest 3",
    is_active=True,
    started_at=datetime.now(),
    end_at=datetime.now(),
)

equipment_checkout3 = EquipmentCheckout(
    user_name="Sally",
    pid=111111111,
    equipment_id=3,
    model="Arduino Uno",
    is_active=False,
    started_at=datetime.now(),
    end_at=datetime.now(),
)

equipment_checkout4 = EquipmentCheckout(
    user_name="Nick",
    pid=730477365,
    equipment_id=6,
    model="Arduino Uno",
    is_active=True,
    started_at=datetime.now(),
    end_at=datetime.now(),
)

equipment_checkout5 = EquipmentCheckout(
    user_name="David",
    pid=233455677,
    equipment_id=7,
    model="Arduino Uno",
    is_active=True,
    started_at=datetime.now(),
    end_at=datetime.now(),
)

equipment_checkout6 = EquipmentCheckout(
    user_name="Kris",
    pid=988766544,
    equipment_id=8,
    model="Arduino Uno",
    is_active=True,
    started_at=datetime.now(),
    end_at=datetime.now(),
)

permissions = [ambassador_permission_crud_checkout, ambassador_permission_view_checkout]

equipment = [
    quest_3,
    arduino,
    arduino2,
    arduino3,
    quest_3_two,
    arduino4,
    arduino5,
    arduino6,
]

checkout_requests = [checkout_request_arduino]

staged_requests = [staged_checkout_request_quest_3, staged_checkout_request_arduino]

checkouts = [
    equipment_checkout1,
    equipment_checkout2,
    equipment_checkout3,
    equipment_checkout4,
    equipment_checkout5,
    equipment_checkout6,
]


def insert_fake_data(session: Session):
    global equipment

    # Create entities for test equipment data
    entities = []
    for item in equipment:
        entity = EquipmentEntity.from_model(item)
        session.add(entity)
        entities.append(entity)

    # Create entities for test equipment checkout request data
    request_entities = []
    for item in checkout_requests:
        entity = EquipmentCheckoutRequestEntity.from_model(item)
        session.add(entity)
        request_entities.append(entity)

    # Create entities for test stage request data
    staged_entities = []
    for item in staged_requests:
        entity = StagedCheckoutRequestEntity.from_model(item)
        session.add(entity)
        staged_entities.append(entity)

    # Create entities for test checkout dataa
    checkout_entities = []
    for item in checkouts:
        entity = EquipmentCheckoutEntity.from_model(item)
        session.add(entity)
        checkout_entities.append(entity)

    # Add ambassador equipment permission for testing
    for i in range(0, len(permissions)):
        ambassador_permission_entity = PermissionEntity(
            id=permissions[i].id,
            role_id=ambassador_role.id,
            action=permissions[i].action,
            resource=permissions[i].resource,
        )
        session.add(ambassador_permission_entity)

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(session, EquipmentEntity, EquipmentEntity.id, len(equipment) + 1)
    reset_table_id_seq(
        session, PermissionEntity, PermissionEntity.id, len(permissions) + 4
    )
    reset_table_id_seq(
        session,
        EquipmentCheckoutRequestEntity,
        EquipmentCheckoutRequestEntity.id,
        len(checkout_requests) + 1,
    )
    reset_table_id_seq(
        session, EquipmentCheckoutEntity, EquipmentCheckoutEntity.id, len(checkouts) + 1
    )

    # Commit all changes
    session.commit()

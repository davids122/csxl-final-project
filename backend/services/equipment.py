"""
The equipment service allows the API to manipulate equipment in the database.
"""

from datetime import datetime
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.entities.equipment_checkout_request_entity import (
    EquipmentCheckoutRequestEntity,
)
from backend.entities.staged_checkout_request_entity import StagedCheckoutRequestEntity
from backend.entities.user_entity import UserEntity
from backend.models.StagedCheckoutRequest import StagedCheckoutRequest
from backend.models.equipment_checkout_request import EquipmentCheckoutRequest

from backend.models.equipment_type import EquipmentType
from backend.models.equipment_checkout import EquipmentCheckout
from .permission import PermissionService

from ..database import db_session
from ..models.equipment import Equipment
from ..entities.equipment_entity import EquipmentEntity
from ..entities.equipment_checkout_entity import EquipmentCheckoutEntity
from ..models import User

# Excluding this import for now, however, we will need to use in later sprints for handling different types of users
# from .permission import PermissionService

__authors__ = ["Jacob Brown, Ayden Franklin"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class DuplicateEquipmentCheckoutRequestException(Exception):
    """DuplicateEquipmentCheckoutRequestException is raised when a user tries to make a second checkout request for the same equipment type"""

    def __init__(self, model: str):
        super().__init__(
            f"You already have an active checkout or checkout request for {model}"
        )


class EquipmentCheckoutRequestNotFoundException(Exception):
    """EquipmentCheckoutRequestNotFoundException is raised when an equipment checkout request is searched for and does not exist"""

    def __init__(self, request: EquipmentCheckoutRequest):
        super().__init__(f"Could not find request: {request}")


class EquipmentAlreadyCheckedOutException(Exception):
    """EquipmentAlreadyCheckedOutException is raised when a user tries to checkout an item that is already checked out"""

    def __init__(self, id: int):
        super().__init__(f"Equipment item with id: {id} is already checkout out")


class EquipmentCheckoutNotFoundException(Exception):
    """EquipmentCheckoutNotFoundException is raised when a user tries to return a checkout that is not found in the database"""

    def __init__(self, id: int):
        super().__init__(
            f"Could not find active checkout for equipment item with id: {id}"
        )


class EquipmentNotFoundException(Exception):
    """EquipmentNotFoundException is raised when trying to access a piece of equipment that does not exist"""

    def __init__(self, id: int):
        super().__init__(f"No Equipment found matching equipment_id: {id}")


class WaiverNotSignedException(Exception):
    """WaiverNotSignedException is raised when a user tries to make an equipment checkout request before they have signed the liability waiver"""

    def __init__(self):
        super().__init__(
            "You must sign the liability waiver before you can request an equipment checkout"
        )


class StagedCheckoutRequestNotFoundException(Exception):
    """StagedCheckoutRequestNotFoundException is raised when a user tries to access a staged checkout request that does not exist"""

    def __init__(self, request: StagedCheckoutRequest):
        super().__init__(f"Could not find staged checkout request: {request}")


class EquipmentService:
    """Service that performs all of the actions on the equipment table."""

    def __init__(
        self,
        session: Session = Depends(db_session),
    ):
        """Initialize the session for querying the db."""
        self._session = session
        self._permission = PermissionService(session=self._session)

    def get_all(self) -> list[Equipment]:
        """Return a list of all equipment in the db."""
        # Create the query for getting all equipment entities.
        query = select(EquipmentEntity)
        # execute the query grabbing each row from the equipment table
        query_result = self._session.scalars(query).all()
        # convert the query results into 'Equipment' models and return as a list
        return [result.to_model() for result in query_result]

    def update(self, item: Equipment, subject: User) -> Equipment:
        """
        updates a specific equipment item.

        Args:
            model (Equipment): The model to update.
            model (User): The user that is checking out the equipment.

        Returns:
            Equipment: the checked out equipment.

        Raises:
            EquipmentNotFoundException if there is no equipment item with the same
            id as the given item
        """

        # ensure user has ambassador permissions
        self._permission.enforce(subject, "equipment.crud.checkout", "equipment")

        # get item with matching equipment_id from db
        query = select(EquipmentEntity).where(
            EquipmentEntity.equipment_id == item.equipment_id
        )
        entity_item: EquipmentEntity | None = self._session.scalar(query)
        # if item with matching id was found, update it
        if entity_item:
            entity_item.update(item)

            self._session.commit()
            return entity_item.to_model()
        # if no item was found, raise exception
        else:
            raise EquipmentNotFoundException(item.equipment_id)

    def get_equipment_by_id(self, id: int, subject: User) -> Equipment:
        """
        Gets a specific equipment item by its equipment id

        Args:
            int (id): the equipment id of the desired equipment item
            model (User): The user that is searching for the equipment

        Returns:
            Equipment: the desired equipment item

        Raises:
            EquipmentNotFoundException if there is no equipment item with the given
            equipment id
        """
        # ensure user has ambassador permissions
        self._permission.enforce(subject, "equipment.view.checkout", "equipment")

        # get item with matching equipment_id from db
        query = select(EquipmentEntity).where(EquipmentEntity.equipment_id == id)
        entity_item: EquipmentEntity | None = self._session.scalar(query)
        # if item with matching id was found, return it
        if entity_item:
            return entity_item.to_model()
        # if no item was found, raise exception
        else:
            raise EquipmentNotFoundException(id)

    def get_all_types(self) -> list[EquipmentType]:
        """
        Converts equipment into list of EquipmentType models

        Args:
            None.

        Returns:
            the unique names of all equipment and the number of each type of equipment.
        """

        all_equipment = self.get_all()
        equipment_types = []

        for equipment in all_equipment:
            # flag to keep track whether the equipment model was succesfully mapped to a equipment_type entry
            caught = False
            for equipment_type in equipment_types:
                if equipment.model == equipment_type.model:
                    # If equipment is currently checked out, not added to num_available
                    if not equipment.is_checked_out:
                        equipment_type.num_available += 1

                    # equipment was successfully mapped to an existing equipment type in the return list
                    caught = True
                    break
            if not caught:
                # If equipment passed through type list without getting caught, this is the first time encountering its type

                if equipment.is_checked_out:
                    # If the equipment is checked out, add its type to the type list, but initialize num_available to 0
                    new_type = EquipmentType(
                        model=equipment.model,
                        num_available=0,
                        equipment_img_URL=equipment.equipment_image,
                    )
                else:
                    # If the equipment is not checked out, add its type to the type list and initialize num_available to 1
                    new_type = EquipmentType(
                        model=equipment.model,
                        num_available=1,
                        equipment_img_URL=equipment.equipment_image,
                    )
                equipment_types.append(new_type)

        return equipment_types

    def add_request(
        self, request: EquipmentCheckoutRequest, user: User
    ) -> EquipmentCheckoutRequest:
        """
        creates an equipment checkout request.

        Args:
            request (EquipmentCheckoutRequest): the checkout request to add.
            user (User): the user trying to request a checkout.

        Returns:
            EquipmentCheckoutRequest: the checkout request we added.

        Raises:
            WaiverNotSignedException if the user has not signed the liability waiver.
        """

        # Check if the user has signed the liability waiver.
        if not user.signed_equipment_wavier:
            raise WaiverNotSignedException

        # Check if the user has already submitted a checkout request for the same type of equipment.
        priorCheckoutRequest = (
            self._session.query(EquipmentCheckoutRequestEntity)
            .filter(
                EquipmentCheckoutRequestEntity.model == request.model,
                EquipmentCheckoutRequestEntity.pid == request.pid,
            )
            .one_or_none()
        )

        # Check if the user has already submitted a staged request for the same type of equipment.
        priorStagedRequest = (
            self._session.query(StagedCheckoutRequestEntity)
            .filter(
                StagedCheckoutRequestEntity.model == request.model,
                StagedCheckoutRequestEntity.pid == request.pid,
            )
            .one_or_none()
        )

        # Check if the user already has a checkout.
        priorCheckout = (
            self._session.query(EquipmentCheckoutEntity)
            .filter(
                EquipmentCheckoutEntity.model == request.model,
                EquipmentCheckoutEntity.pid == request.pid,
                EquipmentCheckoutEntity.is_active,
            )
            .one_or_none()
        )

        # if the user is trying to send a duplicate request, raise exception
        if priorCheckoutRequest or priorStagedRequest or priorCheckout:
            raise DuplicateEquipmentCheckoutRequestException(request.model)

        # create new object
        equipment_checkout_request_entity = EquipmentCheckoutRequestEntity.from_model(
            request
        )

        # add new object to table and commit changes
        self._session.add(equipment_checkout_request_entity)
        self._session.commit()

        # return added object
        return equipment_checkout_request_entity.to_model()

    def delete_request(self, subject: User, request: EquipmentCheckoutRequest) -> None:
        """
        Delete an equipment checkout request

        Args:
            subject (User): the user trying to delete the request
            request (EquipmentCheckoutRequest): the request to be deleted
        """

        self._permission.enforce(
            subject, "equipment.crud.checkout", resource="equipment"
        )
        # find object to delete
        obj = (
            self._session.query(EquipmentCheckoutRequestEntity)
            .filter(
                EquipmentCheckoutRequestEntity.model == request.model,
                EquipmentCheckoutRequestEntity.pid == request.pid,
            )
            .one_or_none()
        )

        # ensure object exists
        if obj:
            # delete object and commit
            self._session.delete(obj)
            self._session.commit()
        else:
            # raise exception
            raise EquipmentCheckoutRequestNotFoundException(request)

    def get_all_requests(self, subject: User) -> list[EquipmentCheckoutRequest]:
        """Return a list of all equipment checkout requests in the db"""
        # enforce ambasssador permission
        self._permission.enforce(
            subject, "equipment.view.checkout", resource="equipment"
        )
        # create the query for getting all equipment checkout request entities.
        query = select(EquipmentCheckoutRequestEntity)
        # execute the query grabbing each row from the equipment table
        query_result = self._session.scalars(query).all()
        # convert the query results into 'EquipmentReservationRequest' models and return as a list
        return [result.to_model() for result in query_result]

    def get_equipment_for_request(self, subject: User, model: str) -> list[Equipment]:
        """returns a list of all available equipment corresponding to the checkout request's model"""

        # query for all equipment that matches the checkout request model type AND is not checked out
        query = select(EquipmentEntity).where(
            EquipmentEntity.model == model,
            EquipmentEntity.is_checked_out == False,
        )

        # return list of queried equipment entities as equipment models
        return [result.to_model() for result in self._session.scalars(query).all()]

    def update_waiver_signed_field(self, user: User) -> User:
        """Updates the signed_equipment_waiver field of a user after they have signed a waiver"""
        # create new user model that is the same as the one to be updated,
        # but with the signed_equipment_waiver being true
        updated_user: User = user
        updated_user.signed_equipment_wavier = True

        # query for user to be updated
        query = select(UserEntity).where(UserEntity.pid == user.pid)
        entity_item: UserEntity | None = self._session.scalar(query)

        # if user was found, update signed waiver field
        if entity_item:
            entity_item.update(updated_user)

            self._session.commit()
            return entity_item.to_model()

        # if user not found, raise exception
        else:
            raise Exception(f"Could not find user {user.first_name} {user.last_name}")

    def get_all_staged_requests(self, subject: User) -> list[StagedCheckoutRequest]:
        """Return a list of all staged checkout requests in the db"""

        # enforce ambasssador permission
        self._permission.enforce(
            subject, "equipment.view.checkout", resource="equipment"
        )

        # create the query for getting all equipment checkout request entities.
        query = select(StagedCheckoutRequestEntity)
        # execute the query grabbing each row from the equipment table
        query_result = self._session.scalars(query).all()
        # convert the query results into 'EquipmentReservationRequest' models and return as a list
        return [result.to_model() for result in query_result]

    def create_staged_request(
        self, subject: User, staged_request: StagedCheckoutRequest
    ) -> StagedCheckoutRequest:
        """Create a staged checkout request"""

        # enforce ambasssador permission
        self._permission.enforce(
            subject, "equipment.crud.checkout", resource="equipment"
        )

        # set id_choices field to ids of available equipment
        staged_request.id_choices = [
            eq.equipment_id
            for eq in self.get_equipment_for_request(subject, staged_request.model)
        ]

        # create new object
        staged_checkout_request_entity = StagedCheckoutRequestEntity.from_model(
            staged_request
        )

        # add new object to table and commit changes
        self._session.add(staged_checkout_request_entity)
        self._session.commit()

        # return added object
        return staged_checkout_request_entity.to_model()

    def delete_staged_request(
        self, subject: User, staged_request: StagedCheckoutRequest
    ) -> None:
        """Delete a staged checkout request"""

        # enforce ambasssador permission
        self._permission.enforce(
            subject, "equipment.crud.checkout", resource="equipment"
        )

        # find stage request entity to delete
        staged_entity = (
            self._session.query(StagedCheckoutRequestEntity)
            .filter(
                StagedCheckoutRequestEntity.pid == staged_request.pid,
                StagedCheckoutRequestEntity.model == staged_request.model,
            )
            .one_or_none()
        )

        if staged_entity:
            # delete entity from db and commit changes
            self._session.delete(staged_entity)
            self._session.commit()
        else:
            # raise exception
            raise StagedCheckoutRequestNotFoundException(staged_request)

    def get_all_active_checkouts(self, subject: User) -> list[EquipmentCheckout]:
        """
        Gets all checkouts that are "active" i.e. that item is currently checked out

        Returns:
            An array of all EquipmentCheckouts, as models, that are "active"
        """
        self._permission.enforce(subject, "equipment.view.checkout", "equipment")
        # Create the query for getting all equipment checkout entities.
        query = select(EquipmentCheckoutEntity).where(
            EquipmentCheckoutEntity.is_active == True
        )
        # execute the query grabbing each row from the equipment table
        query_result = self._session.scalars(query).all()
        # convert the query results into 'Equipment' models and return as a list
        return [result.to_model() for result in query_result]

    def create_checkout(
        self, checkout: EquipmentCheckout, subject: User
    ) -> EquipmentCheckout:
        """
        Creates a new checkout entity and adds it to the database
        Updates the is_checked_out field of the equipment item being checked out to be True

        Args:
            Request (EquipmentCheckout): the checkout to add.
            user (User): User that is trying to

        Returns:
            The checkout that was added

        Raises:
            EquipmentAlreadyCheckedOutException if the equipment already has an active
            checkout associated with it
        """
        self._permission.enforce(subject, "equipment.crud.checkout", "equipment")

        equipment_checkout_entity = EquipmentCheckoutEntity.from_model(checkout)

        # add new object to table
        self._session.add(equipment_checkout_entity)

        # get equipment model to be updated
        equipment_item: Equipment = self.get_equipment_by_id(
            checkout.equipment_id, subject
        )
        # if item is already checked out, raise exception
        if equipment_item.is_checked_out:
            raise EquipmentAlreadyCheckedOutException(checkout.equipment_id)
        # change is_checked_out field to true
        equipment_item.is_checked_out = True
        # update equipment entity to be checked out
        self.update(equipment_item, subject)

        self._session.commit()

        return equipment_checkout_entity.to_model()

    def return_checkout(
        self, checkout: EquipmentCheckout, subject: User
    ) -> EquipmentCheckout:
        """
        Changes the is_active field of the checkout being returned to False
        Changes the end_at field of the checkout to the time of the return
        Changes the is_checked_out field of the equipment item being returned to be False

        Args:
            checkout (EquipmentCheckout): the checkout being returned
            subject (User): the user confirming the checkout return

        Returns:
            the checkout that was returned

        Raises:
            Exception if checkout to be returned is not active
            EquipmentCheckoutNotFoundException if checkout to be returned is not found in the database
        """
        # enforce authorization
        # TODO add method specific permission
        self._permission.enforce(subject, "equipment.crud.checkout", "equipment")
        # ensure that checkout is active
        if not checkout.is_active:
            raise Exception("The equipment you are trying to return is not checked out")

        # get equipment model to be updated
        equipment_item: Equipment = self.get_equipment_by_id(
            checkout.equipment_id, subject
        )
        # change is_checked_out field to false
        equipment_item.is_checked_out = False
        # update equipment entity to be checked out
        self.update(equipment_item, subject)

        # get matching checkout from the db
        # matching equipment_id and is_active will ensure it is the same
        # checkout, there can only be one active checkout at once for a given item
        query = select(EquipmentCheckoutEntity).where(
            EquipmentCheckoutEntity.equipment_id == checkout.equipment_id,
            EquipmentCheckoutEntity.is_active == checkout.is_active,
        )
        entity_item: EquipmentCheckoutEntity | None = self._session.scalar(query)

        # set time that the return happened
        checkout.end_at = datetime.now()
        # set is_active to false
        checkout.is_active = False

        # if matching checkout exists, update it
        if entity_item:
            entity_item.update(checkout)

            self._session.commit()
            return entity_item.to_model()
        # if no checkout was found, raise exception
        else:
            raise EquipmentCheckoutNotFoundException(checkout.equipment_id)

    # TODO: Uncomment during sp02 if we decide to add admin functions for adding/deleting equipment.
    # def add_item(self, item: Equipment) -> Equipment:
    #     """
    #     Creates a new equipment entity and adds to the data base

    #     Args:
    #         model (Equipment): The model to insert into the db.

    #     Returns:
    #         Equipment: the inserted equipment.
    #     """

    #     entity = EquipmentEntity.from_model(item)
    #     self._session.add(entity)
    #     self._session.commit()
    #     return entity.to_model()

    # def delete_item(self, item: Equipment) -> Equipment:
    #     """
    #     Delets an Equipment item from the database

    #     Args:
    #         model (Equipment): The model to delete from the db.

    #     Returns:
    #         Equipment: the deleted equipment.
    #     """

    #     entity = EquipmentEntity.from_model(item)
    #     self._session.delete(entity)
    #     self._session.commit()
    #     return entity.to_model()

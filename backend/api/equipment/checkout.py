"""Equipment Checkout API

This API is used to manage and list user equipment checkouts"""

from fastapi import APIRouter, Depends, HTTPException
from backend.models.StagedCheckoutRequest import StagedCheckoutRequest

from backend.models.equipment_checkout import EquipmentCheckout
from backend.models.equipment_checkout_request import EquipmentCheckoutRequest

from backend.models.equipment_type import EquipmentType
from backend.models.user import User
from ...models.equipment import Equipment
from ...services.equipment import (
    DuplicateEquipmentCheckoutRequestException,
    EquipmentCheckoutNotFoundException,
    EquipmentCheckoutRequestNotFoundException,
    EquipmentService,
    WaiverNotSignedException
)

from backend.api.authentication import registered_user

__authors__ = ["Nicholas Mountain", "Jacob Brown", "Ayden Franklin", "David Sprague"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

api = APIRouter(prefix="/api/equipment")
openapi_tags = {
    "name": "Equipment",
    "description": "Get Equipment and update equipment properties.",
}


@api.get("/get_all", tags=["Equipment"])
def get_all(
    equipment_service: EquipmentService = Depends(),
) -> list[Equipment]:
    """
    Gets all equipment

    Parameters:
        equipment_service: dependency on 'EquipmentService'

    Returns:
        List of equipment in the database
    """

    return equipment_service.get_all()


@api.put("/update", tags=["Equipment"])
def update(
    item: Equipment,
    equipment_service: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> Equipment:
    """
    Update an equipment item

    Parameters:
        item: Item to be updated in the database
        subject: a valid User model representing the currently logged in User
        equipmentService: a valid 'EquipmentService'

    Returns:
        Equipment: the updated Equipment item

    Raises:
        HTTPException 422 if update() raises an Exception
    """

    try:
        # Attempt to update the equipment item.
        return equipment_service.update(item, subject)
    except Exception as e:
        # Raise exception if data incorrectly formatted / not authorized.
        raise HTTPException(status_code=422, detail=str(e))


@api.get("/get_all_types", tags=["Equipment"])
def get_all_types(
    equipment_service: EquipmentService = Depends(),
) -> list[EquipmentType]:
    """
    Gets equipment types and the respective number of items of that type.

    Parameters:
        equipment_service: a valid 'EquipmentService'

    Returns:
        List of equipment types.
    """

    return equipment_service.get_all_types()


@api.post("/add_request", tags=["Equipment"])
def add_request(
    equipmentCheckoutRequest: EquipmentCheckoutRequest,
    equipmentService: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> EquipmentCheckoutRequest:
    """
    Adds a new checkout request.

    Parameters:
        equipment_service: a valid 'EquipmentService'
        subject: a valid registered user
        equipmentCheckoutRequest: a valid equipmentCheckoutRequest

    Returns:
        Newly created equipment checkout request

    Raises:
        WavierNotSignedException if user has not signed waiver

    """
    try:
        # attempt to add a checkout request
        return equipmentService.add_request(equipmentCheckoutRequest, subject)
    except DuplicateEquipmentCheckoutRequestException as e:
        # raise http exception if user has already requested to check out an item of the same model
        raise HTTPException(status_code=403, detail=str(e))
    except WaiverNotSignedException as e:
        raise HTTPException(status_code=451, detail=str(e))


@api.delete("/delete_request", tags=["Equipment"])
def delete_request(
    equipmentCheckoutRequest: EquipmentCheckoutRequest,
    equipmentService: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> None:
    """
    Deletes an existing checkout request

    Parameters:
        equipment_service: a valid 'EquipmentService'
        subject: a valid registered user
        equipmentCheckoutRequest: a valid equipmentCheckoutRequest

    Returns:
        None

    Raises:
        EquipmentCheckoutRequestNotFoundException if request does not exist
    """
    try:
        # attempt to delete a checkout request
        return equipmentService.delete_request(subject, equipmentCheckoutRequest)
    except EquipmentCheckoutRequestNotFoundException as e:
        # raise http exception if the checkout request to be deleted is not found
        raise HTTPException(status_code=422, detail=str(e))


@api.get("/get_all_requests", tags=["Equipment"])
def get_all_requests(
    equipmentService: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> list[EquipmentCheckoutRequest]:
    """
    Gets all pending checkout requests

    Parameters:
        equipmentService: a valid 'EquipmentService'
        subject: a valid registered user

    Returns:
        List of all pending checkout requests
    """

    return equipmentService.get_all_requests(subject)


@api.get("/get_equipment_for_request/{model}", tags=["Equipment"])
def get_all_for_request(
    model: str,
    equipmentService: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> list[Equipment]:
    """
    Gets all available equipment for a confirmed checkout request

    Parameters:
        model: An equipment type as a string
        equipment_service: a valid 'EquipmentService'
        subject: a valid registered user

    Returns:
        List of all available requested equipment
    """

    return equipmentService.get_equipment_for_request(subject, model)


@api.put("/update_waiver_field", tags=["Equipment"])
def update_waiver_field(
    equipment_service: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> User:
    """
    Update the signed waiver field of a user

    Parameters:
        equipment_service: a valid 'EquipmentService'
        subject: a valid User model representing the currently logged in User

    Returns:
        User: the updated User model
    """

    try:
        # Attempt to update user's signed waiver field
        return equipment_service.update_waiver_signed_field(subject)
    except Exception as e:
        # Raise exception if field cannot be updated
        raise HTTPException(status_code=422, detail=str(e))

@api.get("/get_all_staged_requests", tags=["Equipment"])
def get_all_staged_requests(
    equipment_service: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> list[StagedCheckoutRequest]:
    """
    Gets staged equipment checkout requests from db

    Params:
        None

    Returns:
        Array of staged equipment checkouts
    """
    try:
        return equipment_service.get_all_staged_requests(subject)
    # TODO make this the correct exception and status code
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@api.post("/create_staged_request", tags=["Equipment"])
def create_staged_request(
    staged_request: StagedCheckoutRequest,
    equipment_service: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> StagedCheckoutRequest:
    """
    Creates a staged equipment checkout request from db
    
    Params:
        staged_request: A StagedCheckoutRequest Model
        
    Returns:
        StagedCheckoutRequest model that was created

    Raises:
        422 Exception if fails to create staged request
    """
    try:
        return equipment_service.create_staged_request(subject, staged_request)
    # TODO make this the correct error and status code, not thinking about this right now
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))
    
@api.delete("/delete_staged_request", tags=["Equipment"])
def delete_staged_request(
    staged_request: StagedCheckoutRequest,
    equipment_service: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> None:
    """
    Deletes a staged equipment checkout request from db
    
    Params:
        staged_request: A StagedCheckoutRequest Model
        
    Returns:
        None

    Raises:
        422 Exception if fails to delete staged request
    """
    try:
        return equipment_service.delete_staged_request(subject, staged_request)
    # TODO make this the correct error and status code, not thinking about this right now
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@api.get("/get_all_active_checkouts", tags=["Equipment"])
def get_all_active_checkouts(
    equipment_service: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> list[EquipmentCheckout]:
    """
    Gets equipment checkouts

    Parameters:
        equipment_service: a valid 'EquipmentService'

    Returns:
        Array of equipment checkouts
    """
    try:
        return equipment_service.get_all_active_checkouts(subject)
    # TODO make this the correct exception and status code
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@api.post("/create_checkout", tags=["Equipment"])
def create_equipment_checkout(
    checkout: EquipmentCheckout,
    equipment_service: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> EquipmentCheckout:
    """
    Creates an equipment checkout
    
    Params:
        checkout: An EquipmentCheckout Model
        equipment_service: a valid 'EquipmentService'
    Returns:
        EquipmentCheckout model that was created

    Raises:
        422 Exception if fails to create checkout
    """
    try:
        return equipment_service.create_checkout(checkout, subject)
    # TODO make this the correct error and status code, not thinking about this right now
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@api.put("/return_checkout", tags=["Equipment"])
def return_checkout(
    checkout: EquipmentCheckout,
    equipment_service: EquipmentService = Depends(),
    subject: User = Depends(registered_user),
) -> EquipmentCheckout:
    """
    Returns an equipment checkout
    
    Params:
        checkout: An EquipmentCheckout model
        equipment_service: a valid 'EquipmentService'
        subject: a valid User model representing the currently logged in User

    Returns:
        EquipmentCheckout model that was returned

    Raises:
        404 Exception if equipment being returned is not found
        422 Exception if equipment being returned is not checked out
    """

    try:
        return equipment_service.return_checkout(checkout, subject)
    # if Equipment not found, raise 404 exception
    except EquipmentCheckoutNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    # if other error, error was raised because equipment being returned is not checked out
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

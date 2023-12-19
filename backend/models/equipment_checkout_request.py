"""Equipment checkout request model serves as the data object for representing a request to checkout a pience of equipment."""

from pydantic import BaseModel
from .user import User

__authors__ = ["Nicholas Mountain, David Sprague"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EquipmentCheckoutRequest(BaseModel):
    """
    Pydantic model to represent a request to checkout a piece of equipment.

    This model is based on the `EquipmentCheckoutRequestEntity` model, which defines the shape
    of the `EquipmentCheckoutRequest` database in the PostgreSQL database.
    """

    user_name: str
    model: str
    pid: int

"""Equipment checout model serves as the data object for representing equipment checkouts across application layers."""

from datetime import datetime
from pydantic import BaseModel

__authors__ = ["David Sprague"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EquipmentCheckout(BaseModel):
    """
    Pydantic model to represent how Equipment Checkouts are identified in the system.

    This model is based on the `EquipmentCheckoutEntity` model.
    """

    user_name: str
    pid: int
    equipment_id: int
    model: str
    is_active: bool = True
    started_at: datetime
    end_at: datetime

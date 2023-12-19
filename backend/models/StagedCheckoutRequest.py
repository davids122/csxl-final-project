"""Staged Checkout request model serves as the data object for represent staged checkout requests across application layers."""

from pydantic import BaseModel

__authors__ = ["Jacob Brown"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class StagedCheckoutRequest(BaseModel):
    """ "
    Pydantic model to represent how StagedCheckoutRequest is identified in the system.

    This model is based on the `StagedCheckoutRequestEntity` model, which defines the shape
    of the `StagedCheckoutRequest` database in the PostgreSQL database.
    """

    user_name: str
    model: str
    id_choices: list[int] = []
    pid: int

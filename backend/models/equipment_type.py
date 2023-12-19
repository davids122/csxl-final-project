"""Equipment Type model serves as a data object to map database equipment to objects for each unique equipment type"""

from pydantic import BaseModel

__authors__ = ["Ayden Franklin"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EquipmentType(BaseModel):
    """
    Pydantic model to encapsulate unique equipment types and keep track of inventory and details
    """

    model: str
    num_available: int
    equipment_img_URL: str

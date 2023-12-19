"""Definition of SQLAlchemy table-backed object mapping entity for Equipment."""

from sqlalchemy import Boolean, Integer, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self

from backend.models.equipment import Equipment
from .entity_base import EntityBase
from .user_role_table import user_role_table

__authors__ = ["Jacob Brown, Nicholas Mountain"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EquipmentEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Equipment` table"""

    # Name for the equipment table in the PostgreSQL database

    __tablename__ = "equipment"

    # Unique ID for the equipment entry
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Equipment ID of the equipment (should be unique per equipment)
    equipment_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    # Name of the model of the item ex. Meta Quest 3
    model: Mapped[str] = mapped_column(String(64))
    # Image to represent the item
    equipment_image: Mapped[str] = mapped_column(String)
    # Shows if item is currently checked out
    is_checked_out: Mapped[bool] = mapped_column(Boolean)
    # Shows the current condition of the item
    condition: Mapped[int] = mapped_column(Integer)
    # Notes on how the condition of the item has changed throughout checkouts
    condition_notes: Mapped[list[str]] = mapped_column(
        ARRAY(String), nullable=True, default=None
    )
    # List of the PIDs of students who have checkout out this item
    checkout_history: Mapped[list[int]] = mapped_column(
        ARRAY(Integer), nullable=True, default=None
    )

    @classmethod
    def from_model(cls, model: Equipment) -> Self:
        """
        Create an EquipmentEntity from an Equipment model.

        Args:
            model (Equipment): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted).
        """
        return cls(
            equipment_id=model.equipment_id,
            model=model.model,
            equipment_image=model.equipment_image,
            is_checked_out=model.is_checked_out,
            condition=model.condition,
            condition_notes=model.condition_notes,
            checkout_history=model.checkout_history,
        )

    def to_model(self) -> Equipment:
        """
        Create an Equipment model from a EquipmentEntity.

        Returns:
            Equipment: An Equipment model for API usage.
        """
        return Equipment(
            equipment_id=self.equipment_id,
            model=self.model,
            equipment_image=self.equipment_image,
            is_checked_out=self.is_checked_out,
            condition=self.condition,
            condition_notes=self.condition_notes,
            checkout_history=self.checkout_history,
        )

    def update(self, model: Equipment) -> None:
        """
        Update an EquipmentEntity from an Equipment model.

        Args:
            model (Equipment): The model to update the entity from.

        Returns:
            None
        """
        if model.equipment_id != self.equipment_id:
            raise ReferenceError(
                "Failed to update Equipment Entity because model id did not match entity id."
            )

        self.model = model.model
        self.equipment_image = model.equipment_image
        self.is_checked_out = model.is_checked_out
        self.condition = model.condition
        self.condition_notes = model.condition_notes
        self.checkout_history = model.checkout_history

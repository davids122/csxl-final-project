"""Definition of SQLAlchemy table-backed object mapping entity for Equipment checkouts."""
from datetime import datetime
from sqlalchemy import Boolean, Integer, String, ARRAY, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Self

from backend.models.equipment import Equipment
from backend.models.equipment_checkout import EquipmentCheckout
from .entity_base import EntityBase
from .user_role_table import user_role_table

__authors__ = ["Jacob Brown, Nicholas Mountain"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


class EquipmentCheckoutEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Equipment Checkout` table"""

    # Name for the equipment checkout table in the PostgreSQL database

    __tablename__ = "equipment_checkouts"

    # Unique ID for the equipment checkout entry
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # User name of the student that checked out the equipment
    user_name: Mapped[str] = mapped_column(String(64))
    # Pid of user that checkout out the equipment
    pid: Mapped[int] = mapped_column(Integer)
    # Equipment ID of the equipment that is being checked out
    equipment_id: Mapped[int] = mapped_column(Integer)
    # Name of the model of the item that is being checked out
    model: Mapped[str] = mapped_column(String(64))
    # Boolean field to represent whether the checkout is currently active(item is checked out)
    is_active: Mapped[bool] = mapped_column(Boolean)
    # DateTime to represent when the checkout began
    started_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    # DateTime to represent when the checkout ended(when item was checked back in)
    end_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    @classmethod
    def from_model(cls, model: EquipmentCheckout) -> Self:
        """
        Create an EquipmentCheckoutEntity from an EquipmentCheckout model.

        Args:
            model (EquipmentCheckout): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted).
        """
        return cls(
            user_name=model.user_name,
            pid=model.pid,
            equipment_id=model.equipment_id,
            model=model.model,
            is_active=model.is_active,
            started_at=model.started_at,
            end_at=model.end_at,
        )

    def to_model(self) -> EquipmentCheckout:
        """
        Create an Equipment Checkout model from a EquipmentCheckoutEntity.

        Returns:
            EquipmentCheckout: An Equipment Checkout model for API usage.
        """
        return EquipmentCheckout(
            user_name=self.user_name,
            pid=self.pid,
            equipment_id=self.equipment_id,
            model=self.model,
            is_active=self.is_active,
            started_at=self.started_at,
            end_at=self.end_at,
        )

    def update(self, model: EquipmentCheckout) -> None:
        """
        Update an EquipmentCheckoutEntity from an EquipmentCheckout model.

        Args:
            model (EquipmentCheckout): The model to update the entity from.

        Returns:
            None
        """
        # start time will guarantee same unique checkout and will never need to be updated
        if model.started_at != self.started_at:
            raise ReferenceError(
                "Failed to update EquipmentCheckoutEntity because model start time did not match entity start time"
            )

        self.user_name = model.user_name
        self.pid = model.pid
        self.equipment_id = model.equipment_id
        self.is_active = model.is_active
        self.end_at = model.end_at

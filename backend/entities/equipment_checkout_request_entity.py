"""Definition of SQLAlchemy table-backed object mapping entity for equipment checkout requests. """


from typing import Self
from sqlalchemy import Integer, String
from .entity_base import EntityBase
from sqlalchemy.orm import Mapped, mapped_column
from backend.models.equipment_checkout_request import EquipmentCheckoutRequest


class EquipmentCheckoutRequestEntity(EntityBase):
    # Name for the equipment checkout request table in the PostgreSQL database

    __tablename__ = "equipment_checkout_requests"

    # Unique ID for the equipment checkout request entry
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # User name of the user that is requesting a checkout
    user_name: Mapped[str] = mapped_column(String(64))
    # Name of the model of the equipment requested
    model: Mapped[str] = mapped_column(String(64))
    # PID of the user that is requesting a checkout
    pid: Mapped[int] = mapped_column(Integer)

    @classmethod
    def from_model(cls, model: EquipmentCheckoutRequest) -> Self:
        """
        Create an EquipmentCheckoutRequestEntity from an EquipmentCheckoutRequest model.

        Args:
            model (EquipmentCheckoutResquest): The model to create the entity from.

        Returns:
            Self: The entity (not yet persisted).
        """
        return cls(
            user_name=model.user_name,
            model=model.model,
            pid=model.pid,
        )

    def to_model(self) -> EquipmentCheckoutRequest:
        """
        Create an EquipmentCheckoutRequest model from a EquipmentCheckoutRequestEntity.

        Returns:
            EquipmentCheckoutRequest: An EquipmentCheckoutRequest model for API usage.
        """
        return EquipmentCheckoutRequest(
            user_name=self.user_name, model=self.model, pid=self.pid
        )

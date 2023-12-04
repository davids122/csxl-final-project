"""Definition of SQLAlchemy table-backed object mapping entity for staged checkout requests. """

from backend.entities.entity_base import EntityBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ARRAY
from typing import Self

from backend.models.StagedCheckoutRequest import StagedCheckoutRequest


class StagedCheckoutRequestEntity(EntityBase):
    __tablename__ = "staged_checkout_requests"

    # The id of the staged checkout request.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # User name of the user that is requesting a checkout.
    user_name: Mapped[str] = mapped_column(String)
    # The model of the item to be checked out
    model: Mapped[str] = mapped_column(String)
    # The pid of the user making the checkout.
    pid: Mapped[int] = mapped_column(Integer)
    # The id selected by the ambassador to checkout for the user.
    id_choices: Mapped[list[int]] = mapped_column(
        ARRAY(Integer), nullable=True, default=[]
    )

    @classmethod
    def from_model(cls, model: StagedCheckoutRequest) -> Self:
        """
        Create a StagedCheckoutRequestEntity from a StagedCheckoutRequest.

        Args:
            Model: the model to create the entity from

        returns:
            Self: the entity (not yet persisted)
        """
        return cls(
            user_name=model.user_name,
            model=model.model,
            pid=model.pid,
            id_choices=model.id_choices,
        )

    def to_model(self) -> StagedCheckoutRequest:
        """
        Create a StagedCheckoutRequest from a StagedCheckoutRequestEntity.

        Args:
            Entity: the entity to create the model from

        returns:
            Model: the model (not yet persisted)
        """
        return StagedCheckoutRequest(
            user_name=self.user_name,
            model=self.model,
            pid=self.pid,
            id_choices=self.id_choices,
        )

    def update(self, model: StagedCheckoutRequest) -> None:
        """
        Update a StagedCheckoutRequestEntity from a StagedCheckoutRequest.

        Args:
            Model: the model to update the entity from

        returns:
            None
        """
        # if model.id != self.id:
        #     raise ReferenceError(
        #         "Failed to update StagedCheckoutRequest Entity because model id did not match entity id."
        #     )

        # Update the entity to match the model.
        self.user_name = model.user_name
        self.model = model.model
        self.pid = model.pid
        self.id_choices = model.id_choices

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
    # The pid of the user making the checkout. 
    pid: Mapped[int] = mapped_column(Integer)
    # The id selected by the ambassador to checkout for the user.
    selected_id: Mapped[int] = mapped_column(Integer, nullable=True)
    # Array to represent the available id choices for a user to checkout.
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
            id=model.id,
            user_name=model.user_name,
            pid=model.pid,
            selected_id=model.selected_id,
            id_choices=model.id_choices
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
            id=self.id,
            user_name=self.user_name,
            pid=self.pid,
            selected_id=self.selected_id,
            id_choices=self.id_choices
        )
    
    def update(self, model: StagedCheckoutRequest) -> None:
        """
        Update a StagedCheckoutRequestEntity from a StagedCheckoutRequest.
        
        Args: 
            Model: the model to update the entity from
            
        returns:
            None
        """
        if model.id != self.id:
            raise ReferenceError(
                "Failed to update StagedCheckoutRequest Entity because model id did not match entity id."
            )
        
        # Update the entity to match the model.
        self.user_name = model.user_name
        self.pid = model.pid
        self.selected_id = model.selected_id
        self.id_choices = model.id_choices
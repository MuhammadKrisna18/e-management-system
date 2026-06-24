
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any

from app.domain.repositories.booking_repository import BookingRepository
from app.domain.repositories.event_repository import EventRepository
from app.domain.repositories.refund_repository import RefundRepository
from app.domain.repositories.ticket_repository import TicketRepository

# Type variables for repository implementations
TAggregate = TypeVar('TAggregate')
TCommand = TypeVar('TCommand')
TResult = TypeVar('TResult')


class BaseCommandHandler(ABC, Generic[TCommand, TResult]):
    
    def handle(self, command: TCommand) -> TResult:
        # Step 1: Validate input
        self._validate_command(command)
        
        # Step 2: Get or create aggregate
        aggregate = self._get_or_create_aggregate(command)
        
        # Step 3: Execute business logic
        result = self._execute_business_logic(aggregate, command)
        
        # Step 4: Persist changes
        self._persist_changes(aggregate)
        
        # Step 5: Return result
        return result
    
    def _validate_command(self, command: TCommand) -> None:
        if command is None:
            raise ValueError("Command cannot be None")
    
    @abstractmethod
    def _get_or_create_aggregate(self, command: TCommand) -> TAggregate:
        pass
    
    @abstractmethod
    def _execute_business_logic(self, aggregate: TAggregate, command: TCommand) -> Any:
        pass
    
    @abstractmethod
    def _persist_changes(self, aggregate: TAggregate) -> None:
        pass


class BaseReadHandler(ABC, Generic[TCommand, TResult]):
    
    def handle(self, query: TCommand) -> TResult:
        # Step 1: Validate query
        self._validate_query(query)
        
        # Step 2: Retrieve data
        data = self._retrieve_data(query)
        
        # Step 3: Format response
        return self._format_response(data, query)
    
    def _validate_query(self, query: TCommand) -> None:
        if query is None:
            raise ValueError("Query cannot be None")
    
    @abstractmethod
    def _retrieve_data(self, query: TCommand) -> Any:
        pass
    
    @abstractmethod
    def _format_response(self, data: Any, query: TCommand) -> TResult:
        pass

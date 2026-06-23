"""
Base Command Handler

Provides common pattern for all command handlers.
Eliminates code duplication across handlers.
"""

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
    """
    Abstract base class for command handlers.
    
    Implements common pattern:
    1. Validate input
    2. Retrieve/Create aggregate
    3. Execute business logic
    4. Save aggregate
    5. Return result
    
    Subclasses implement the specific business logic.
    """
    
    def handle(self, command: TCommand) -> TResult:
        """
        Handle command execution.
        
        Template method implementing common pattern:
        - Validate command
        - Get/create aggregate
        - Execute business logic
        - Persist changes
        - Return result
        
        Args:
            command: Command object with parameters
            
        Returns:
            Result of command execution
        """
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
        """
        Validate command parameters.
        
        Override in subclass to add command-specific validation.
        
        Args:
            command: Command to validate
            
        Raises:
            ValueError: If validation fails
        """
        if command is None:
            raise ValueError("Command cannot be None")
    
    @abstractmethod
    def _get_or_create_aggregate(self, command: TCommand) -> TAggregate:
        """
        Get existing aggregate or create new one.
        
        Must be implemented by subclasses.
        
        Args:
            command: Command with aggregate identifier
            
        Returns:
            Retrieved or created aggregate
            
        Raises:
            NotFoundError: If aggregate not found and can't create
        """
        pass
    
    @abstractmethod
    def _execute_business_logic(self, aggregate: TAggregate, command: TCommand) -> Any:
        """
        Execute domain business logic.
        
        Calls aggregate methods to perform operations.
        
        Args:
            aggregate: Aggregate root to operate on
            command: Command parameters
            
        Returns:
            Intermediate result from business logic
        """
        pass
    
    @abstractmethod
    def _persist_changes(self, aggregate: TAggregate) -> None:
        """
        Persist aggregate changes.
        
        Must be implemented by subclasses.
        
        Args:
            aggregate: Modified aggregate to save
        """
        pass


class BaseReadHandler(ABC, Generic[TCommand, TResult]):
    """
    Abstract base class for query handlers.
    
    Implements common pattern:
    1. Validate query
    2. Retrieve data
    3. Format response
    """
    
    def handle(self, query: TCommand) -> TResult:
        """
        Handle query execution.
        
        Template method implementing read pattern:
        - Validate query
        - Retrieve data
        - Format response
        
        Args:
            query: Query object with parameters
            
        Returns:
            Formatted response
        """
        # Step 1: Validate query
        self._validate_query(query)
        
        # Step 2: Retrieve data
        data = self._retrieve_data(query)
        
        # Step 3: Format response
        return self._format_response(data, query)
    
    def _validate_query(self, query: TCommand) -> None:
        """
        Validate query parameters.
        
        Override in subclass for query-specific validation.
        
        Args:
            query: Query to validate
            
        Raises:
            ValueError: If validation fails
        """
        if query is None:
            raise ValueError("Query cannot be None")
    
    @abstractmethod
    def _retrieve_data(self, query: TCommand) -> Any:
        """
        Retrieve data from repositories.
        
        Must be implemented by subclasses.
        
        Args:
            query: Query with filter parameters
            
        Returns:
            Retrieved raw data
        """
        pass
    
    @abstractmethod
    def _format_response(self, data: Any, query: TCommand) -> TResult:
        """
        Format data into response DTO.
        
        Converts domain objects to DTOs.
        
        Args:
            data: Raw data from retrieval
            query: Original query (for context)
            
        Returns:
            Formatted response
        """
        pass

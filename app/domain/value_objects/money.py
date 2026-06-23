"""
Money Value Object

Represents a monetary amount with currency.
Encapsulates amount validation and arithmetic operations.
"""

from app.domain.constants import ErrorMessages, ValidationMessages


class Money:
    """
    Value object representing a monetary amount.
    
    Immutable and can only be compared by value.
    Validates that amounts are non-negative.
    """
    
    def __init__(self, amount: float) -> None:
        """
        Initialize Money value object.
        
        Args:
            amount: Monetary amount (must be non-negative)
            
        Raises:
            ValueError: If amount is negative
            TypeError: If amount is not a number
        """
        if not isinstance(amount, (int, float)):
            raise TypeError(f"Amount must be numeric, got {type(amount).__name__}")
        
        if amount < 0:
            raise ValueError(ValidationMessages.PRICE_CANNOT_BE_NEGATIVE)
        
        self.amount: float = float(amount)
    
    def add(self, other: 'Money') -> 'Money':
        """
        Add two Money objects.
        
        Args:
            other: Money object to add
            
        Returns:
            Money: New Money object with sum of amounts
            
        Raises:
            TypeError: If other is not a Money instance
        """
        if not isinstance(other, Money):
            raise TypeError(f"Expected Money, got {type(other).__name__}")
        
        return Money(self.amount + other.amount)
    
    def subtract(self, other: 'Money') -> 'Money':
        """
        Subtract Money object from this one.
        
        Args:
            other: Money object to subtract
            
        Returns:
            Money: New Money object with difference
            
        Raises:
            TypeError: If other is not a Money instance
            ValueError: If result would be negative
        """
        if not isinstance(other, Money):
            raise TypeError(f"Expected Money, got {type(other).__name__}")
        
        result = self.amount - other.amount
        if result < 0:
            raise ValueError("Cannot subtract amount larger than current amount")
        
        return Money(result)
    
    def multiply(self, multiplier: float) -> 'Money':
        """
        Multiply Money amount by a factor.
        
        Args:
            multiplier: Factor to multiply by
            
        Returns:
            Money: New Money object with multiplied amount
            
        Raises:
            TypeError: If multiplier is not numeric
        """
        if not isinstance(multiplier, (int, float)):
            raise TypeError(f"Multiplier must be numeric, got {type(multiplier).__name__}")
        
        return Money(self.amount * multiplier)
    
    def __eq__(self, other: object) -> bool:
        """Check equality by amount value."""
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount
    
    def __lt__(self, other: 'Money') -> bool:
        """Compare if this amount is less than other."""
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount < other.amount
    
    def __le__(self, other: 'Money') -> bool:
        """Compare if this amount is less than or equal to other."""
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount <= other.amount
    
    def __gt__(self, other: 'Money') -> bool:
        """Compare if this amount is greater than other."""
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount > other.amount
    
    def __ge__(self, other: 'Money') -> bool:
        """Compare if this amount is greater than or equal to other."""
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount >= other.amount
    
    def __str__(self) -> str:
        """String representation of money amount."""
        return f"Rp {self.amount:,.2f}"
    
    def __repr__(self) -> str:
        """Developer representation."""
        return f"Money({self.amount})"
    
    def __hash__(self) -> int:
        """Make Money hashable for use in sets/dicts."""
        return hash(self.amount)

from app.domain.constants import ErrorMessages, ValidationMessages


class Money:
    
    def __init__(self, amount: float) -> None:
        if not isinstance(amount, (int, float)):
            raise TypeError(f"Amount must be numeric, got {type(amount).__name__}")
        
        if amount < 0:
            raise ValueError(ValidationMessages.PRICE_CANNOT_BE_NEGATIVE)
        
        self.amount: float = float(amount)
    
    def add(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError(f"Expected Money, got {type(other).__name__}")
        
        return Money(self.amount + other.amount)
    
    def subtract(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError(f"Expected Money, got {type(other).__name__}")
        
        result = self.amount - other.amount
        if result < 0:
            raise ValueError("Cannot subtract amount larger than current amount")
        
        return Money(result)
    
    def multiply(self, multiplier: float) -> 'Money':
        if not isinstance(multiplier, (int, float)):
            raise TypeError(f"Multiplier must be numeric, got {type(multiplier).__name__}")
        
        return Money(self.amount * multiplier)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount
    
    def __lt__(self, other: 'Money') -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount < other.amount
    
    def __le__(self, other: 'Money') -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount <= other.amount
    
    def __gt__(self, other: 'Money') -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount > other.amount
    
    def __ge__(self, other: 'Money') -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount >= other.amount
    
    def __str__(self) -> str:
        return f"Rp {self.amount:,.2f}"
    
    def __repr__(self) -> str:
        return f"Money({self.amount})"
    
    def __hash__(self) -> int:
        return hash(self.amount)
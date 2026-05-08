"""Authentication Service Interface"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class AuthenticationService(ABC):
    """Interface for authentication service"""

    @abstractmethod
    def authenticate(
        self,
        username: str,
        password: str,
    ) -> Dict[str, Any]:
        """
        Authenticate user
        
        Args:
            username: Username or email
            password: Password
            
        Returns:
            Dictionary with auth result {success, user_id, token, message}
        """
        pass

    @abstractmethod
    def validate_token(
        self,
        token: str,
    ) -> Dict[str, Any]:
        """
        Validate authentication token
        
        Args:
            token: Authentication token
            
        Returns:
            Dictionary with validation result {valid, user_id, expired}
        """
        pass

    @abstractmethod
    def get_current_user(
        self,
        token: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Get current authenticated user
        
        Args:
            token: Authentication token
            
        Returns:
            Dictionary with user data {id, username, email, roles}
        """
        pass

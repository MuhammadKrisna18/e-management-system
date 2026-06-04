"""
Pagination Utilities

Common pagination logic for query handlers.
"""

from math import ceil
from typing import List, Tuple, TypeVar, Generic

T = TypeVar('T')


class PaginationHelper(Generic[T]):
    """Helper class for paginating query results."""
    
    @staticmethod
    def paginate(
        items: List[T],
        page: int,
        page_size: int
    ) -> Tuple[List[T], int, int]:
        """
        Paginate items and calculate pagination info.
        
        Args:
            items: List of items to paginate
            page: Page number (1-based)
            page_size: Number of items per page
            
        Returns:
            Tuple of (paginated_items, total_count, total_pages)
            
        Raises:
            ValueError: If page or page_size invalid
        """
        if page < 1:
            raise ValueError("Page number must be >= 1")
        
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        
        total = len(items)
        total_pages = ceil(total / page_size) if total > 0 else 1
        
        # Validate page is within range
        if page > total_pages:
            page = total_pages
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_items = items[start_idx:end_idx]
        
        return paginated_items, total, total_pages
    
    @staticmethod
    def calculate_total_pages(total_count: int, page_size: int) -> int:
        """
        Calculate total number of pages.
        
        Args:
            total_count: Total number of items
            page_size: Items per page
            
        Returns:
            Total number of pages
        """
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        
        return ceil(total_count / page_size) if total_count > 0 else 1
    
    @staticmethod
    def calculate_skip_and_limit(
        page: int,
        page_size: int
    ) -> Tuple[int, int]:
        """
        Calculate skip and limit for database queries.
        
        Args:
            page: Page number (1-based)
            page_size: Items per page
            
        Returns:
            Tuple of (skip_count, limit_count)
        """
        if page < 1:
            raise ValueError("Page number must be >= 1")
        
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        
        skip = (page - 1) * page_size
        limit = page_size
        
        return skip, limit


from math import ceil
from typing import List, Tuple, TypeVar, Generic

T = TypeVar('T')


class PaginationHelper(Generic[T]):
    
    @staticmethod
    def paginate(
        items: List[T],
        page: int,
        page_size: int
    ) -> Tuple[List[T], int, int]:
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
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        
        return ceil(total_count / page_size) if total_count > 0 else 1
    
    @staticmethod
    def calculate_skip_and_limit(
        page: int,
        page_size: int
    ) -> Tuple[int, int]:
        if page < 1:
            raise ValueError("Page number must be >= 1")
        
        if page_size < 1:
            raise ValueError("Page size must be >= 1")
        
        skip = (page - 1) * page_size
        limit = page_size
        
        return skip, limit

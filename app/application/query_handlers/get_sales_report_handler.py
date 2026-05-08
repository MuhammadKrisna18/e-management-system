"""Get Sales Report Handler"""

from app.application.queries.get_sales_report_query import GetSalesReportQuery


class GetSalesReportHandler:
    """Handler for GetSalesReportQuery"""

    def __init__(self, booking_repository):
        self.booking_repository = booking_repository

    def handle(self, query: GetSalesReportQuery) -> dict:
        """
        Handle getting sales report
        
        Args:
            query: GetSalesReportQuery instance
            
        Returns:
            Sales report data
        """
        report = self.booking_repository.get_sales_report(
            event_id=query.event_id,
            start_date=query.start_date,
            end_date=query.end_date,
        )
        
        return report

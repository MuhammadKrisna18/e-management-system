from app.domain.entities.ticket_category import TicketCategory


class CreateTicketCategoryHandler:

    def __init__(
        self,
        repository
    ):
        self.repository = repository

    def handle(
        self,
        command
    ):
        aggregate = (
            self.repository.get_by_id(
                command.event_id
            )
        )

        category = TicketCategory(
            name=command.name,
            price=command.price,
            quota=command.quota,
            sales_start_date=command.sales_start_date,
            sales_end_date=command.sales_end_date,
            event_start_date=aggregate.event.start_date
        )

        aggregate.add_ticket_category(
            category
        )

        self.repository.save(
            aggregate
        )

        return aggregate

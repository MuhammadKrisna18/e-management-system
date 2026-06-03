class GetEventDetailsHandler:

    def __init__(
        self,
        repository
    ):
        self.repository = repository

    def handle(
        self,
        query
    ):

        return (
            self.repository
            .get_by_id(
                query.event_id
            )
        )
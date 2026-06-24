class GetAvailableEventsHandler:

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
            .find_published()
        )
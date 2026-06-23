class CancelEventHandler:

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

        aggregate.cancel()

        self.repository.save(
            aggregate
        )

        return aggregate

class PublishEventHandler:

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

        aggregate.publish()

        self.repository.save(
            aggregate
        )

        return aggregate
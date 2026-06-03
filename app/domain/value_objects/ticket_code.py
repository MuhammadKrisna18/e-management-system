import uuid


class TicketCode:

    def __init__(self, value=None):

        self.value = value or str(
            uuid.uuid4()
        )

    def __str__(self):
        return self.value
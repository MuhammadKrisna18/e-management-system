from datetime import datetime


class PaymentDeadline:

    def __init__(
        self,
        deadline: datetime
    ):
        self.deadline = deadline

    def is_expired(self):

        return (
            datetime.now()
            > self.deadline
        )
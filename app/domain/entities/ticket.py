class Ticket:

    def __init__(self, code: str):
        self.code = code
        self.status = "Active"

    def check_in(self):

        if self.status == "CheckedIn":
            raise ValueError(
                "Ticket already checked in"
            )

        if self.status == "Cancelled":
            raise ValueError(
                "Cancelled ticket cannot check in"
            )

        self.status = "CheckedIn"

    def cancel(self):
        self.status = "Cancelled"

from datetime import datetime


class Poops:
    """
    Track poops

    Instance Attributes:
    - today: number of poops today
    - total: number of poops in total
    - log: dictionary of poops on a data {data: number of poops}
    """
    today: int
    total: int
    log: dict[str, int]

    def __init__(self, today: int = 0, total: int = 0, log=None):
        if log is None:
            log = {}
        self.today = today
        self.total = total
        self.log = log

    def __str__(self):
        return f'Today: {self.today} ----- Total: {self.total}'

    def log_poop(self, n: int):
        """add n poops to today and total"""
        self.today += n
        self.total += n

        today = str(datetime.today().date())
        if today not in self.log:
            self.log[today] = n
        else:
            self.log[today] += n


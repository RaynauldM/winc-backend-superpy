from datetime import datetime


class SuperDatetime:
    def __init__(self):
        # datetime object
        self.dt = datetime.now()

    def get_datetime(self):
        return f"{self.dt.year}-{self.dt.month}-{self.dt.day}"

    def get_year(self):
        return self.dt.year

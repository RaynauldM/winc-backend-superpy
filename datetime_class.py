from datetime import datetime, timedelta


class SuperDatetime:
    def __init__(self):
        # datetime object
        self.dt = datetime.date(datetime.now())
        self.working_date = self.get_date()

    def advance_date(self, num):
        old_date = self.get_date()
        new_date = datetime.strptime(old_date, "%Y-%m-%d") + timedelta(days=num)

        self.set_date(new_date.strftime("%Y-%m-%d"))

    def get_date(self):
        with open("data/date.txt", "r") as file:
            content = file.read()
            if content == "":
                self.set_date("this_date")
                return content
            else:
                return content

    def get_datetime(self):
        return self.dt.strftime("%Y-%m-%d")

    def get_year(self):
        return_year = ""
        li = list(self.working_date)
        return_year += li[0]
        return_year += li[1]
        return_year += li[2]
        return_year += li[3]
        return return_year

    def get_yesterday(self):
        today = datetime.strptime(self.get_date(), "%Y-%m-%d")
        yesterday = today - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    def set_date(self, new_date="this_date"):
        if new_date == "this_date":
            with open("data/date.txt", "w") as file:
                file.write(self.get_datetime())
        else:
            new_date_obj = datetime.strptime(new_date, "%Y-%m-%d")
            new_date_str = new_date_obj.strftime("%Y-%m-%d")
            with open("data/date.txt", "w") as file:
                file.write(new_date_str)

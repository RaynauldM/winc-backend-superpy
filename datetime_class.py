from datetime import datetime


class SuperDatetime:
    def __init__(self):
        # datetime object
        self.dt = datetime.date(datetime.now())
        self.working_date = self.get_date()

    def get_date(self):
        with open("data/date.txt", "r") as file:
            content = file.read()
            if content == "":
                self.set_date("this_date")
                return content
            else:
                return content

    def set_date(self, new_date):
        if new_date == "this_date":
            with open("data/date.txt", "w") as file:
                file.write(self.get_datetime())
        else:
            new_date_obj = datetime.strptime(new_date, "%Y-%m")
            new_date_str = new_date_obj.strftime("%Y-%m")
            with open("data/date.txt", "w") as file:
                file.write(new_date_str)

    def get_datetime(self):
        return self.dt.strftime("%Y-%m")

    def get_year(self):
        return_year = ""
        li = list(self.working_date)
        return_year += li[0]
        return_year += li[1]
        return_year += li[2]
        return_year += li[3]
        return return_year

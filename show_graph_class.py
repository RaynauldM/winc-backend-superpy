import matplotlib.pyplot as plt

from datetime import datetime


class SuperPlot:
    def __init__(self, values, start_date, end_date):
        self.values = values
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")

    def plot(self):
        # Calculate the increment between dates
        num_dates = len(self.values)
        increment = (self.end_date - self.start_date) / (num_dates - 1)

        # Generate the list of dates
        dates = [self.start_date + increment * i for i in range(num_dates)]

        formated_dates = [date.strftime("%Y-%m-%d") for date in dates]

        plt.plot_date(formated_dates, self.values, linestyle="-")

        plt.xticks(rotation=45)

        plt.subplots_adjust(bottom=0.4)

        plt.title("SuperPy")

        plt.show()

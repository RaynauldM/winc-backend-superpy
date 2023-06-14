import csv
from pathlib import Path


class SuperCsv:
    def __init__(self):
        self.this_directory = Path.cwd()
        self.data_directory = Path(self.this_directory, "data")
        self.data_bought = Path(self.data_directory, "bought.csv")
        self.data_sold = Path(self.data_directory, "sold.csv")

    def add_bought(self, name, date, price, exp):
        with open(self.data_bought, "r") as file:
            reader = csv.reader(file)
            row_count = len(list(reader))
        with open(self.data_bought, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([row_count, name, date, price, exp])

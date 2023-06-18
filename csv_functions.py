import csv
from pathlib import Path
import tempfile
import shutil


class SuperCsv:
    def __init__(self):
        self.this_directory = Path.cwd()
        self.data_directory = Path(self.this_directory, "data")
        self.data_bought = Path(self.data_directory, "bought.csv")
        self.data_sold = Path(self.data_directory, "sold.csv")

    def add_bought(self, name, count, date, price, exp):
        with open(self.data_bought, "r") as file:
            reader = csv.reader(file)
            row_count = len(list(reader))
        with open(self.data_bought, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([row_count - 1, name, count, date, price, exp])

    def sell_product(self, bought_id, count, date, price):
        with open(self.data_sold, "r") as file:
            reader = csv.reader(file)
            row_count = len(list(reader))

        with open(self.data_sold, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([row_count - 1, bought_id, count, date, price])

        self.update_row(bought_id, count)

    def find_bought_id(self, product_name):
        return_list = []
        with open(self.data_bought, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if product_name in row:
                    return_list.append(row)
            return return_list

    def update_row(self, id, count):
        temp = tempfile.NamedTemporaryFile(mode="w", delete=False)

        with open(self.data_bought, "r") as file, temp:
            reader = csv.reader(file)
            writer = csv.writer(temp)

            for row in reader:
                if len(row) == 0:
                    continue
                if row[0] == id:
                    new_row = [None] * 6  # Initialize new_row with 6 elements
                    new_row[0] = row[0]
                    new_row[1] = row[1]
                    new_row[2] = str(int(row[2]) - int(count))
                    new_row[3] = row[3]
                    new_row[4] = row[4]
                    new_row[5] = row[5]
                    writer.writerow(new_row)
                else:
                    writer.writerow(row)

        shutil.move(temp.name, self.data_bought)

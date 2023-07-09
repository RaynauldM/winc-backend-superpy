import csv
import shutil
import sys
import tempfile

from datetime_class import SuperDatetime
from datetime import datetime, timedelta
from pathlib import Path

from rich import print


class SuperCsv:
    def __init__(self):
        # use of pathlib to make sure the txt files are always found
        self.this_directory = Path.cwd()
        self.data_directory = Path(self.this_directory, "data")
        self.data_bought = Path(self.data_directory, "bought.csv")
        self.data_sold = Path(self.data_directory, "sold.csv")
        self.sold_list = self.get_sold_list()

    # add to bought list
    def add_bought(self, name, count, date, price, exp):
        with open(self.data_bought, "r") as file:
            reader = csv.reader(file)
            row_count = len(list(reader))
        with open(self.data_bought, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([row_count - 1, name, count, date, price, exp])

    def find_bought_id(self, product_name):
        return_list = []
        with open(self.data_bought, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if product_name in row:
                    return_list.append(row)
            return return_list

    def get_count(self, id):
        with open(self.data_bought, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == str(id):
                    return row[2]

    def get_inventory(self):
        return_list = []
        with open(self.data_bought, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 0:
                    continue
                if row[0] == "id":
                    continue
                else:
                    return_list.append(row)

        return return_list

    def get_inventory_any_day(self, date):
        inventory = SuperCsv().get_inventory()
        filtered_inventory = [item for item in inventory if item[3].startswith(date)]
        return filtered_inventory

    def get_inventory_yesterday(self):
        yesterday = SuperDatetime().dt - timedelta(days=1)
        formatted_date = yesterday.strftime("%Y-%m-%d")
        inventory = SuperCsv().get_inventory()
        filtered_inventory = [
            item for item in inventory if item[3].startswith(formatted_date)
        ]
        return filtered_inventory

    def get_ordered_list(self):
        old_list = self.get_sold_list()
        new_list = sorted(old_list, key=lambda x: x[3])
        return new_list

    def get_profit(self, start_date, end_date):
        cost = 0.0
        revenue = self.get_revenue(start_date, end_date)
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        if self.is_file_empty(self.data_bought) is True:
            print("[red]nothing bought yet[/red]")
            input("")
            sys.exit()
        with open(self.data_bought, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 0:
                    continue
                try:
                    date = datetime.strptime(row[3], "%Y-%m-%d")
                    if start_datetime <= date <= end_datetime:
                        cost += float(row[4])
                except ValueError:
                    continue

        return revenue - cost

    def get_revenue(self, start_date, end_date):
        revenue = 0.0
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        if self.is_file_empty(self.data_sold) is True:
            print("[red]nothing sold yet[/red]")
            input("")
            sys.exit()
        with open(self.data_sold, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 0:
                    continue
                try:
                    date = datetime.strptime(row[3], "%Y-%m-%d")
                    if start_datetime <= date <= end_datetime:
                        revenue += float(row[4])
                except ValueError:
                    continue

        return revenue

    def get_sold_list(self):
        return_list = []
        with open(self.data_sold, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    if row[0] == "id":
                        continue
                    else:
                        return_list.append(row)
                except IndexError:
                    continue
        return return_list

    def is_file_empty(self, file):
        checked_list = []
        with open(file) as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 0:
                    continue
                checked_list.append(row)
        if len(checked_list) < 2:
            return True
        return False

    def sell_product(self, bought_id, count, date, price):
        with open(self.data_sold, "r") as file:
            reader = csv.reader(file)
            row_count = len(list(reader))

        with open(self.data_sold, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([row_count - 1, bought_id, count, date, price])

        self.update_row(bought_id, count)

    # make changes within a csv

    def update_row(self, id, count):
        temp = tempfile.NamedTemporaryFile(mode="w", delete=False, newline="")

        with open(self.data_bought, "r", newline="") as file, temp:
            reader = csv.reader(file)
            writer = csv.writer(temp)

            rows_to_write = []

            for row in reader:
                if len(row) == 0:
                    continue
                if row[0] == id:
                    new_row = [None] * 6
                    new_row[0] = row[0]
                    new_row[1] = row[1]
                    new_row[2] = str(int(row[2]) - int(count))
                    new_row[3] = row[3]
                    new_row[4] = row[4]
                    new_row[5] = row[5]
                    rows_to_write.append(new_row)
                elif any(row):
                    rows_to_write.append(row)

            writer.writerows(rows_to_write)

        shutil.move(temp.name, self.data_bought)

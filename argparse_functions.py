import argparse
import sys
from csv_functions import SuperCsv
from datetime_functions import SuperDatetime

choice_help_message = """
[buy] buy product,\n
[sell] sell product,\n
[report] show inventory\n
"""

# list to check if a string only contains numbers, dots and dash in the check_if_int method
symbols = [
    chr(i)
    for i in range(32, 127)
    if not chr(i).isdigit() and chr(i) != "." and chr(i) != "-"
]


class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="A program to help a supermarket keep track of products bought and sold"
        )

        # first positional argument, to be ommited to change the datetime
        self.parser.add_argument(
            "choice",
            nargs="?",
            default="default_argument",
            help=choice_help_message,
        )

        # second positional argument, in case of first argument == 'report'
        self.parser.add_argument(
            "report_choice",
            nargs="?",
            default="no_report_choice",
        )

        # optional arguments
        self.parser.add_argument(
            "-pn",
            "--product-name",
            help="name of the product to be bought in single form",
        )

        self.parser.add_argument(
            "-c", "--count", help="Set the amount of the product to buy"
        )
        self.parser.add_argument(
            "-p", "--price", help="set the price for the product to buy"
        )

        self.parser.add_argument(
            "-ed",
            "--expiration_date",
            help="set the expiration date for the product to buy, in the format [yyyy] to set only year or [yyyy-mm] to set year and month",
        )

        self.parser.add_argument("--now", action="store_true")

        self.parser.add_argument("--today", action="store_true")

        self.parser.add_argument("-yd", "--yesterday", action="store_true")

        self.parser.add_argument(
            "--date",
            help="type a date in [yyyy-mm] format to get the information of the chosen month",
        )

        self.parser.add_argument("-at", "--advance_time", type=int)

        self.choice = "default"
        self.report_choice = "default"
        self.product_name = "default"
        self.count = -99
        self.price = -99
        self.expiration_date = -99
        self.advance_time = "default"

        self.this_date = SuperDatetime()

    def checkArgument(self, var, string):
        if var is None or var == "":
            var = input(f"Please enter a {string}:\n")
        if var is None or var == "":
            input("Sorry, could not compute. Press enter to exit the program")
            sys.exit()
        return var

    def conformation(self):
        yes_no_input = input(
            f"On the date: {self.this_date.get_datetime()}\n you want to buy {self.count} {self.product_name}, for the price of {self.price}, which whill expire on {self.expiration_date}\n please enter [y] or [yes] if correct\n"
        )
        if yes_no_input == "yes" or yes_no_input == "y":
            SuperCsv().add_bought(
                self.product_name,
                self.count,
                self.this_date.get_datetime(),
                self.price,
                self.expiration_date,
            )
            print("ok, written to the harddrive.")
        else:
            input("No data saved. Press enter to exit")
            sys.exit()

    def default_error_message(self, text="Error, something went wrong"):
        print(text + "\nplease try again")
        input("")
        sys.exit()

    def check_product_name(self):
        pn = self.product_name
        plist = list(pn)
        if len(pn) == 0 or len(pn) > 20 or " " in plist:
            self.default_error_message("Invalid product name")

    def check_if_int(self, obj):
        li = list(obj)
        for i in li:
            if i in symbols:
                self.default_error_message("only numbers allowed")

    def check_expiration_date(self):
        ex_list = list(self.expiration_date)
        expiration_year = ex_list[0] + ex_list[1] + ex_list[2] + ex_list[3]
        this_year = self.this_date.get_year()
        if int(expiration_year) < int(this_year):
            self.default_error_message("expiration year has already passed")
        if len(self.expiration_date) == 4:
            self.expiration_date += "-01"
        elif "-" not in self.expiration_date:
            self.default_error_message("please input the date as [yyyy] or [yyyy-mm]")
        elif "-" in self.expiration_date:
            month = ""
            month += ex_list[-2]
            month += ex_list[-1]
            month = int(month)
            if month > 12:
                self.default_error_message("months can not exceed 12")

    def run(self):
        args = self.parser.parse_args()

        # collect the arguments
        self.choice = args.choice
        self.report_choice = args.report_choice
        self.product_name = args.product_name
        self.count = args.count
        self.price = args.price
        self.expiration_date = args.expiration_date
        self.advance_time = args.advance_time

        # work with the arguments
        # choice was [buy]
        if self.choice == "buy":
            self.product_name = self.checkArgument(
                self.product_name, "product name with underscore between words"
            )
            self.check_product_name()
            self.count = self.checkArgument(
                self.count, f"number of how many of {self.product_name} will be bought"
            )
            self.check_if_int(self.count)
            self.price = self.checkArgument(self.price, "price")
            self.check_if_int(self.price)
            self.expiration_date = self.checkArgument(
                self.expiration_date, "expiration date [yyyy] or [yyyy-mm]"
            )

            self.check_if_int(self.expiration_date)
            self.check_expiration_date()
            self.conformation()

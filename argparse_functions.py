import argparse
import sys

choice_help_message = """
[buy] buy produce,\n
[sell] sell produce,\n
[report] show inventory\n
"""


class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="A program to help a supermarket keep track of produce bought and sold"
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
            type=str,
            help="name of the product to be bought in single form",
        )
        self.parser.add_argument(
            "-p", "--price", help="set the price for the product to buy", type=int
        )

        self.parser.add_argument(
            "-ed",
            "--expiration_date",
            help="set the expiration date for the product to buy, in the format [yy] to set only year or [yyyy-mm-dd] to be specific",
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
        self.price = -99
        self.expiration_date = -99
        self.advance_time = "default"

    def checkArgument(self, var, string):
        if var is None or var == "":
            var = input(f"Please enter a {string}:\n")
        if var is None or var == "":
            input("Sorry, could not compute. Press enter to exit the programme")
            sys.exit()
        return var

    def conformation(self):
        yes_no_input = input(
            f"You want to buy a {self.product_name}, for the price of {self.price}, which whill expire on {self.expiration_date},\n please enter [y] or [yes] if correct\n"
        )
        if yes_no_input == "yes" or yes_no_input == "y":
            print("ok, written to the harddrive.")
        else:
            input("No data saved. Press enter to exit")
            sys.exit()

    def run(self):
        args = self.parser.parse_args()

        # collect the arguments
        self.choice = args.choice
        self.report_choice = args.report_choice
        self.product_name = args.product_name
        self.price = args.price
        self.expiration_date = args.expiration_date
        self.advance_time = args.advance_time

        # work with the arguments
        if self.choice == "buy":
            self.product_name = self.checkArgument(self.product_name, "product name")
            self.price = self.checkArgument(self.price, "price")
            self.expiration_date = self.checkArgument(
                self.expiration_date, "expiration date"
            )
            self.conformation()

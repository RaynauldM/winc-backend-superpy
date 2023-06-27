import argparse
import sys
from csv_class import SuperCsv
from datetime_class import SuperDatetime

choice_help_message = """
[buy] buy product,\n
[sell] sell product,\n
[report] report on report_choice,\n
[] work with date\n
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
            help="[inventory], [revenue], [profit]",
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
            "--expiration-date",
            help="set the expiration date for the product to buy, in the format [yyyy] to set only year or [yyyy-mm] to set year and month",
        )

        self.parser.add_argument(
            "--today", action="store_true", help="Use the current working date"
        )

        self.parser.add_argument(
            "-yd",
            "--yesterday",
            action="store_true",
            help="Use the day before the current working date",
        )

        self.parser.add_argument(
            "-set",
            "--set_date",
            default="default",
            help="Set the date in format [yyy-mm-dd]",
        )

        self.parser.add_argument(
            "-see",
            "--see_date",
            action="store_true",
            help="See the current working date",
        )

        self.parser.add_argument(
            "-rd",
            "--reset_date",
            action="store_true",
            help="Reset current working date to date of machine",
        )

        self.parser.add_argument(
            "-at",
            "--advance_time",
            default=0,
            type=int,
            help="Advance current date by chosen number of days",
        )

        self.parser.add_argument(
            "-cp",
            "--choose_parameter",
            action="store_true",
            help="Choose a specific period between two dates",
        )

        self.parser.add_argument(
            "-stard",
            "--start_date",
            default="default",
            help="Starting date for choose_parameter argument",
        )

        self.parser.add_argument(
            "-end",
            "--end_date",
            default="default",
            help="End date for choose_parameter argument",
        )

    # custom check to see if arguments are valid, a bit redundant, but I'll keep it in place still
    def checkArgument(self, var, string):
        if var is None or var == "":
            var = input(f"Please enter a {string}:\n")
        if var is None or var == "":
            self.default_error_message("could not compute, please try again")
        return var

    def check_count(self):
        self.check_if_int(self.count)
        if len(self.id_list) > 1:
            if (float(self.id_list[2]) - float(self.count)) < 0:
                self.default_error_message(
                    "This will bring us out of stock! Please try again"
                )
        else:
            if (float(self.id_list[0][2]) - float(self.count)) < 0:
                self.default_error_message(
                    "This will bring us out of stock! Please try again"
                )

    def check_expiration_date(self):
        ex_list = list(self.expiration_date)
        expiration_year = ex_list[0] + ex_list[1] + ex_list[2] + ex_list[3]
        this_year = SuperDatetime().get_year()
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

    def check_if_int(self, obj):
        li = list(obj)
        for i in li:
            if i in symbols:
                self.default_error_message("only numbers allowed")
        return True

    def check_product_name(self):
        if self.choice == "sell":
            pn = self.product_name
            plist = list(pn)
            if len(pn) == 0 or len(pn) > 20 or " " in plist:
                self.default_error_message("Invalid product name")
            self.id_list = SuperCsv().find_bought_id(self.product_name)
            if len(self.id_list) == 0:
                self.default_error_message(
                    f"{self.product_name} not found in bought list"
                )
            if len(self.id_list) > 1:
                print(f"found multiple {self.product_name}")
                for item in self.id_list:
                    print(item)
                possible_list = [item[0] for item in self.id_list]
                correct_id = input("please input the correct id\n")
                if correct_id in possible_list:
                    for item in self.id_list:
                        if item[0] == correct_id:
                            self.id_list = item
                else:
                    self.default_error_message("no matching id found, please try again")

    def conformation(self, buy_or_sell):
        if buy_or_sell == "buy":
            yes_input = input(
                f"On the date: {SuperDatetime().get_date()}\n you want to buy {self.count} {self.product_name}, for the price of {self.price}, which whill expire on {self.expiration_date}\n please enter [y] or [yes] if correct\n"
            )
            if yes_input == "yes" or yes_input == "y":
                SuperCsv().add_bought(
                    self.product_name,
                    self.count,
                    SuperDatetime().get_date(),
                    self.price,
                    self.expiration_date,
                )
                print("ok, written to the harddrive.")
            else:
                input("No data saved. Press enter to exit")
                sys.exit()
        elif buy_or_sell == "sell":
            yes_input = input(
                f"On the date: {SuperDatetime().get_date()}\n you want to sell {self.count} {self.product_name}, for the price of {self.price}\n please enter [y] or [yes] if correct\n"
            )
            if yes_input == "yes" or yes_input == "y":
                SuperCsv().sell_product(
                    self.id_list[0][0],
                    self.count,
                    SuperDatetime().get_date(),
                    self.price,
                )
                print("ok, written to the harddrive.")
            else:
                input("No data saved. Press enter to exit")
                sys.exit()

    def default_error_message(self, text="Error, something went wrong"):
        print(text + "\nplease try again")
        input("")
        sys.exit()

    def print_working_date(self):
        print(f"the working date is: {SuperDatetime().get_date()}")

    def super_print(self, list):
        for item in list:
            print(
                f"\nid: {item[0]}\nproduct: {item[1]}\ncount: {item[2]}\nbuy date: {item[3]}\nbuy price: {item[4]}\nexpiration: {item[5]}\n \n"
            )

    # methods for the choice argument

    def buy(self):
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
        self.conformation("buy")

    def no_choice(self):
        if self.see_date is True:
            self.print_working_date()
            input("")
            sys.exit()
        if self.reset_date is True:
            SuperDatetime().set_date()
            input(f"Changed date to {SuperDatetime().get_datetime()}")
            sys.exit()

        if self.advance_time > 0:
            SuperDatetime().advance_date(self.advance_time)
            print("Changed the date")
            sys.exit()

        if self.set_date != "default":
            if self.check_if_int(self.set_date):
                SuperDatetime().set_date(self.set_date)
                print("updated the date!")
                sys.exit()
            else:
                self.default_error_message("invalid input for setting the date")

    def report(self):
        if self.report_choice == "no_report_choice":
            self.default_error_message(
                "Please provide a second argument after [report].\nThe arguments you can choose are [inventory], [revenue] or [profit]."
            )
        elif self.report_choice == "inventory":
            if self.today:
                inventory = SuperCsv().get_inventory()
                if len(inventory) == 0:
                    self.default_error_message("Empty inventory for this day")
                else:
                    self.super_print(inventory)
            if self.yesterday:
                inventory = SuperCsv().get_inventory_yesterday()
                self.super_print(inventory)
            if self.set_date != "default":
                try:
                    setted_date = self.set_date
                    self.super_print(SuperCsv().get_inventory_any_day(setted_date))
                except ValueError:
                    self.default_error_message(
                        "Input date with format [yyyy-mm-dd] and make sure the date is posible"
                    )

        elif self.report_choice == "revenue":
            if self.today:
                today = SuperDatetime().working_date
                revenue = SuperCsv().get_revenue(today, today)
                print(f"Todays revenue: {revenue}")
            if self.yesterday:
                yesterday = SuperDatetime().get_yesterday()
                revenue = SuperCsv().get_revenue(yesterday, yesterday)
                print(f"Yesterdays revenue: {revenue}")
            if self.set_date != "default":
                try:
                    setted_date = self.set_date
                    print(
                        f"Profit for date {setted_date}: {SuperCsv().get_profit(setted_date,setted_date)}"
                    )
                except ValueError:
                    self.default_error_message(
                        "Input date with format [yyyy-mm-dd] and make sure the date is posible"
                    )
            if self.choose_param:
                print(
                    f"For the period {self.start_date} through {self.end_date}\nrevenue: {SuperCsv().get_revenue(self.start_date, self.end_date)}\n"
                )
        elif self.report_choice == "profit":
            if self.today:
                today = SuperDatetime().working_date
                profit = SuperCsv().get_profit(today, today)
                print(f"Todays profit is: {profit}")
            if self.yesterday:
                yesterday = SuperDatetime().get_yesterday()
                profit = SuperCsv().get_profit(yesterday, yesterday)
                print(f"Yesterdays profit is: {profit}")
            if self.set_date != "default":
                try:
                    setted_date = self.set_date
                    print(
                        f"Profit for date {setted_date}: {SuperCsv().get_profit(setted_date,setted_date)}"
                    )
                except ValueError:
                    self.default_error_message(
                        "Input date with format [yyyy-mm-dd] and make sure the date is posible"
                    )
            if self.choose_param:
                print(
                    f"For the period {self.start_date} through {self.end_date}\nprofit: {SuperCsv().get_profit(self.start_date, self.end_date)}"
                )

    def sell(self):
        self.product_name = self.checkArgument(
            self.product_name, "product name with underscore between words"
        )
        self.check_product_name()
        self.count = self.checkArgument(
            self.count, f"number of how many of {self.product_name} will be sold"
        )
        self.check_count()
        self.price = self.checkArgument(self.price, "price")
        self.check_if_int(self.price)
        self.conformation("sell")

    def run(self):
        args = self.parser.parse_args()

        # collect the arguments
        self.choice = args.choice
        self.report_choice = args.report_choice
        self.product_name = args.product_name
        self.count = args.count
        self.price = args.price
        self.expiration_date = args.expiration_date
        self.set_date = args.set_date
        self.see_date = args.see_date
        self.reset_date = args.reset_date
        self.advance_time = args.advance_time
        self.today = args.today
        self.yesterday = args.yesterday
        self.choose_param = args.choose_parameter
        self.start_date = args.start_date
        self.end_date = args.end_date

        # work with the choice argument
        if self.choice == "buy":
            self.buy()
        elif self.choice == "sell":
            self.sell()
        elif self.choice == "default_argument":
            self.no_choice()
        elif self.choice == "report":
            self.report()

import argparse
import sys

from csv_class import SuperCsv
from datetime_class import SuperDatetime

from rich import print
from show_graph_class import SuperPlot


choice_help_message = """
[buy] buy product,
[sell] sell product,
[report] report on report_choice,
[] work with date
"""

# list to check if a string only contains numbers
# dots and dash in the check_if_int method
symbols = [
    chr(i)
    for i in range(32, 127)
    if not chr(i).isdigit() and chr(i) != "." and chr(i) != "-"
]


class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="super.py",
            description="a program to help a supermarket keep "
            "track of products bought and sold",
            epilog="for any questions contact me at raynauldminkema@gmail.com",
        )

        self.positionals = self.parser.add_argument_group("POSITIONAL ARGUMENTS")
        self.optionals = self.parser.add_argument_group("OPTIONAL ARGUMENTS")
        self.times = self.parser.add_argument_group(
            "arguments relating to WORKING DATE. Use without positional arguments"
        )

        # first positional argument, to be ommited to change the datetime
        self.positionals.add_argument(
            "choice",
            nargs="?",
            default="default_argument",
            help=choice_help_message,
        )

        # second positional argument, in case of first argument == 'report'
        self.positionals.add_argument(
            "report_choice",
            nargs="?",
            default="no_report_choice",
            help="[inventory], [revenue], [profit]",
        )

        # optional arguments

        self.times.add_argument(
            "-at",
            "--advance-time",
            default=0,
            type=int,
            help="advance current date by chosen number of days",
        )

        self.optionals.add_argument(
            "-c",
            "--count",
            help="use with [buy] or [sell] to set the amount of the product to buy",
        )

        self.optionals.add_argument(
            "-cp",
            "--choose_parameter",
            action="store_true",
            help="used with [report] [revenue] and [report] [profit], together with [-stard] and [-end] to choose a specific period between two dates",
        )

        self.optionals.add_argument(
            "-ed",
            "--expiration-date",
            help="use with [buy] to set the expiration date, in the format [yyyy] to set only year or [yyyy-mm] to set year and month",
        )

        self.optionals.add_argument(
            "-end",
            "--end_date",
            default="default",
            help="end date for choose_parameter argument",
        )

        self.optionals.add_argument(
            "-p",
            "--price",
            help="use with [buy] or [sell] to set the price for the product",
        )

        self.optionals.add_argument(
            "-pn",
            "--product-name",
            help="use with [buy] or [sell] to name the product",
        )

        self.times.add_argument(
            "-rd",
            "--reset_date",
            action="store_true",
            help="reset current working date to current date of machine",
        )

        self.times.add_argument(
            "-see",
            "--see_date",
            action="store_true",
            help="see the current working date",
        )

        self.optionals.add_argument(
            "-sg",
            "--show_graph",
            action="store_true",
            help="Show revenue in a visual form",
        )

        self.times.add_argument(
            "-set",
            "--set_date",
            default="default",
            help="set the date in format [yyy-mm-dd]",
        )

        self.optionals.add_argument(
            "-s",
            "--sold",
            action="store_true",
            help="Show the sold list instead of bought list",
        )

        self.optionals.add_argument(
            "-start",
            "--start_date",
            default="default",
            help="starting date for choose_parameter argument",
        )

        self.optionals.add_argument(
            "--today",
            action="store_true",
            help="use with [report] to use the current working date",
        )

        self.optionals.add_argument(
            "-yd",
            "--yesterday",
            action="store_true",
            help="use with [report] to use the day before the current working date",
        )

    # custom check to see if arguments are valid, a bit redundant probably
    def check_argument(self, var, string):
        if var is None or var == "":
            var = input(f"Please enter a {string}:\n")
        if var is None or var == "":
            self.default_error_message("could not compute, please try again")
        return var

    # check if count argument is posible
    def check_count(self):
        self.check_if_int(self.count)
        if len(self.id_list) > 1:
            if (float(self.id_list[2]) - float(self.count)) < 0:
                self.default_error_message("This will bring us out of stock!")
        else:
            if (float(self.id_list[0][2]) - float(self.count)) < 0:
                self.default_error_message("This will bring us out of stock!")
        return True

    # check if expiration date is possible
    def check_expiration_date(self):
        ex_list = list(self.expiration_date)
        expiration_year = ex_list[0] + ex_list[1] + ex_list[2] + ex_list[3]
        expiration_month = ex_list[5] + ex_list[6]
        this_year = SuperDatetime().get_year()
        this_month = SuperDatetime().get_month()
        if int(expiration_year) < int(this_year):
            self.default_error_message("expiration year has already passed")

        elif int(expiration_month) < int(this_month):
            self.default_error_message("expiration date has already passed")

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
        return True

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
                print(
                    f"found multiple [bold underline]{self.product_name}[/bold underline]"
                )
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
        return True

    def getInput(self, text):
        return input(text)

    # will ask the user one last confirmation before writing to csv file
    def conformation(self, buy_or_sell):
        if buy_or_sell == "buy":
            yes_input = self.getInput(
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
                print("[green]ok, written to the harddrive[/green]")
            else:
                print("[red]No data saved.[/red] \nPress enter to exit")

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
                print("[green]ok, written to the harddrive.[/green]")
            else:
                print("[red]No data saved.[/red] \nPress enter to exit")

    def default_error_message(self, text="[red]Error[/red], something went wrong"):
        print(f"[bold red]{text}[/bold red]" + "\nplease try again")
        sys.exit()

    def print_working_date(self):
        print(
            f"the working date is: [underline]{SuperDatetime().get_date()}[/underline]"
        )

    # designated print, shows expiration date in red if it exceeds the working date
    def super_print(self, list):
        today = SuperDatetime().get_date()
        for item in list:
            if item[5] < today:
                print(
                    f"\nid: {item[0]}\nproduct: [bold underline]{item[1]}[/bold underline]\ncount: {item[2]}\nbuy date: {item[3]}\nbuy price: {item[4]}\n[red bold]expiration: {item[5]}[/red bold]\n \n"
                )
            else:
                print(
                    f"\nid: {item[0]}\nproduct: [bold underline]{item[1]}[/bold underline]\ncount: {item[2]}\nbuy date: {item[3]}\nbuy price: {item[4]}\nexpiration: {item[5]}\n \n"
                )

    # methods for the choice argument

    def buy(self):
        self.product_name = self.check_argument(
            self.product_name, "product name with underscore between words"
        )
        self.check_product_name()
        self.count = self.check_argument(
            self.count, f"number of how many of {self.product_name} will be bought"
        )
        self.check_if_int(self.count)
        self.price = self.check_argument(self.price, "price")
        self.check_if_int(self.price)
        self.expiration_date = self.check_argument(
            self.expiration_date, "expiration date [yyyy] or [yyyy-mm]"
        )

        self.check_if_int(self.expiration_date)
        self.check_expiration_date()
        self.conformation("buy")

    def no_choice(self):
        if self.see_date is True:
            self.print_working_date()

        if self.reset_date is True:
            SuperDatetime().set_date()
            print(f"[blue]Changed date to [/blue]{SuperDatetime().get_datetime()}")

        if self.advance_time > 0:
            SuperDatetime().advance_date(self.advance_time)
            print("[blue]Advanced the date![/blue]")

        if self.set_date != "default":
            if self.check_if_int(self.set_date):
                SuperDatetime().set_date(self.set_date)
                print("[blue]updated the date![/blue]")

            else:
                self.default_error_message("invalid input for setting the date")

    def report(self):
        if self.report_choice == "no_report_choice":
            self.default_error_message(
                "Please provide a second argument after report.\nThe arguments you can choose are inventory, revenue or profit."
            )
        elif self.report_choice == "inventory":
            if self.sold:
                sold_list = SuperCsv().get_sold_list()
                bought_list = SuperCsv().get_inventory()
                for sold_item in sold_list:
                    bought_id = sold_item[1]

                    product_name = None
                    for bought_item in bought_list:
                        if bought_item[0] == bought_id:
                            product_name = bought_item[1]
                            break

                    if product_name is not None:
                        print(
                            f"{sold_item[2]} {product_name} was sold on {sold_item[-2]} for {sold_item[-1]} dollars"
                        )

            if self.today:
                inventory = SuperCsv().get_inventory()
                if len(inventory) == 0:
                    self.default_error_message("Empty inventory for this day")
                else:
                    self.super_print(inventory)
            if self.yesterday:
                inventory = SuperCsv().get_inventory_yesterday()
                if len(inventory) == 0:
                    self.default_error_message("Empty inventory for this day")
                else:
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
            if self.show_graph:
                sold_list = SuperCsv().sold_list
                if len(sold_list) <= 1:
                    self.default_error_message("Not enough data.")
                else:
                    sold_list = SuperCsv().get_ordered_list()
                    start_date = sold_list[0][3]
                    end_date = sold_list[-1][3]
                    values = [float(i[-1]) for i in sold_list]

                    visual = SuperPlot(values, start_date, end_date)
                    visual.plot()

            if self.today:
                today = SuperDatetime().working_date
                revenue = SuperCsv().get_revenue(today, today)
                print(f"Todays revenue: [bold green]{revenue}[/bold green]")
            if self.yesterday:
                yesterday = SuperDatetime().get_yesterday()
                revenue = SuperCsv().get_revenue(yesterday, yesterday)
                print(f"Yesterdays revenue: [bold green]{revenue}[/bold green]")
            if self.set_date != "default":
                try:
                    setted_date = self.set_date
                    print(
                        f"Profit for date {setted_date}: [bold green]{SuperCsv().get_profit(setted_date,setted_date)}[/bold green]"
                    )
                except ValueError:
                    self.default_error_message(
                        "Input date with format [yyyy-mm-dd] and make sure the date is posible"
                    )
            if self.choose_param:
                print(
                    f"For the period {self.start_date} through {self.end_date}\nrevenue: [bold green]{SuperCsv().get_revenue(self.start_date, self.end_date)}[/bold green]\n"
                )
        elif self.report_choice == "profit":
            if self.today:
                today = SuperDatetime().working_date
                profit = SuperCsv().get_profit(today, today)
                print(f"Todays profit is: [bold green][{profit}[/bold green]")
            if self.yesterday:
                yesterday = SuperDatetime().get_yesterday()
                profit = SuperCsv().get_profit(yesterday, yesterday)
                print(f"Yesterdays profit is: [bold green]{profit}[/bold green]")
            if self.set_date != "default":
                try:
                    setted_date = self.set_date
                    print(
                        f"Profit for date {setted_date}: [bold green]{SuperCsv().get_profit(setted_date,setted_date)}[/bold green]"
                    )
                except ValueError:
                    self.default_error_message(
                        "Input date with format [yyyy-mm-dd] and make sure the date is posible"
                    )
            if self.choose_param:
                print(
                    f"For the period {self.start_date} through {self.end_date}\nprofit: [bold green]{SuperCsv().get_profit(self.start_date, self.end_date)}[/bold green]"
                )

    def sell(self):
        self.product_name = self.check_argument(
            self.product_name, "product name with underscore between words"
        )
        self.check_product_name()
        self.count = self.check_argument(
            self.count, f"number of how many of {self.product_name} will be sold"
        )
        self.check_count()
        self.price = self.check_argument(self.price, "price")
        self.check_if_int(self.price)
        if self.choice == "test":
            return True
        self.conformation("sell")

    def run(self):
        args = self.parser.parse_args()

        # collect the arguments
        self.advance_time = args.advance_time
        self.choice = args.choice
        self.choose_param = args.choose_parameter
        self.count = args.count
        self.end_date = args.end_date
        self.expiration_date = args.expiration_date
        self.price = args.price
        self.product_name = args.product_name
        self.report_choice = args.report_choice
        self.reset_date = args.reset_date
        self.see_date = args.see_date
        self.set_date = args.set_date
        self.show_graph = args.show_graph
        self.sold = args.sold
        self.start_date = args.start_date
        self.today = args.today
        self.yesterday = args.yesterday

        # work with the choice argument
        if self.choice == "buy":
            self.buy()
        elif self.choice == "sell":
            self.sell()
        elif self.choice == "default_argument":
            self.no_choice()
        elif self.choice == "report":
            self.report()

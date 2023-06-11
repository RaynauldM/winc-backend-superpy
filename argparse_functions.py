import argparse

choice_help_message = """
[buy] buy produce,\n
[sell] sell produce,\n
[report] show inventory\n
"""


def startArg():
    parser = argparse.ArgumentParser(
        description="A program to help a supermarket keep track of produce bought and sold"
    )
    # first positional argument, to be ommited to change the datetime
    parser.add_argument(
        "choice",
        nargs="?",
        default="default_argument",
        help=choice_help_message,
    )

    # second positional argument, in case of first argument == 'report'
    parser.add_argument(
        "report_choice",
        nargs="?",
        default="no_report_choice",
    )

    # optional arguments
    parser.add_argument(
        "-pn",
        "--product-name",
        type=str,
        help="name of the product to be bought in single form",
    )
    parser.add_argument(
        "-p", "--price", help="set the price for the product to buy", type=int
    )

    parser.add_argument(
        "-ed",
        "--expiration_date",
        help="set the expiration date for the product to buy",
    )

    parser.add_argument("--now", action="store_true")

    parser.add_argument("--today", action="store_true")

    parser.add_argument("-yd", "--yesterday", action="store_true")

    parser.add_argument(
        "--date",
        help="type a date in [yyyy-mm] format to get the information of the chosen month",
    )

    parser.add_argument("-at", "--advance_time", type=int)

    args = parser.parse_args()

    # collect the arguments
    choice = args.choice
    report_choice = args.report_choice
    product_name = args.product_name
    price = args.price
    expiration_date = args.expiration_date
    advance_time = args.advance_time

    if choice == "buy":
        print("dit werkt")

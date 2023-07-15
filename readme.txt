Super.py  -- ReadMe

This program is designed to help a supermarket keep track of products bought and sold. It provides functionality for buying products, selling products, generating reports and managing the working date.

USAGE
Run the program using the following command in the CLI:
python super.py [arguments]

When buyin or selling not all arguments are needed. The program will ask you for the missing arguments.
Example: python super.py buy

ARGUMENTS
[buy]: Buy a product. 
Example: python super.py buy -pn apples -c 10 -p 1.99 -ed 2023-08

[sell]: Sell a product. 
Example: python super.py sell -pn apples -c 5 -p 2.49

[report]: Generate a report. 
Example: python super.py report inventory --today

OPTIONAL ARGUMENTS
[-at], [--advance-time]: Advance the current date by a specified number of days. 
Example: python super.py -at 7

[-c], [--count]: Set the quantity of a product to buy or sell. 
Example: python super.py buy -pn apples -c 10

[-cp], [--choose_parameter]: Choose a specific date range for generating reports. 
Example: python super.py report revenue -cp -start 2023-01-01 -end 2023-12-31

[-ed], [--expiration-date]: Set the expiration date for a product. 
Example: python super.py buy -pn apples -ed 2023-08

[-h], [--help]: Show help screen.
Example: python super.py -h

[-p], [--price]: Set the price of a product. 
Example: python super.py buy -pn apples -p 1.99

[-pn], [--product-name]: Specify the name of a product. 
Example: python super.py buy -pn apples

[-rd], [--reset-date]: Reset the current working date to the current date of the machine. 
Example: python super.py -rd

[-see], [--see-date]: View the current working date. 
Example: python super.py -see

[-set], [--set_date]: Set the working date in format yyyy-mm-dd.
Example: python super.py -set 2024-05-01

[-sg], [--show-graph]: Show revenue in a visual form. 
Example: python super.py report revenue -sg

[-s], [--sold]: Show the sold list instead of the bought list. 
Example: python super.py report inventory -s

[-start], [--start-date]: Specify the start date for choosing a specific date range. 
Example: python super.py report revenue -cp -start 2023-01-01 -end 2023-12-31

[--today]: Use the current working date for generating reports. 
Example: python super.py report revenue --today

[-yd], [--yesterday]: Use the day before the current working date for generating reports. 
Example: python super.py report revenue -yd

EXAMPLES
Buy 10 apples with a price of $1.99 and an expiration date of August 2023:
python super.py buy -pn apples -c 10 -p 1.99 -ed 2023-08

Sell 5 apples for $2.49:
python super.py sell -pn apples -c 5 -p 2.49

Generate an inventory report for today:
python super.py report inventory --today

Generate a revenue report for a specific date range and show it as a graph:
python super.py report revenue -cp -start 2023-01-01 -end 2023-12-31 -sg

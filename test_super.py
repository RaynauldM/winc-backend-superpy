from argparse_class import ArgParse
from csv_class import SuperCsv

# some variables to be used in the tests

product_name = "test"
id_list = SuperCsv().find_bought_id(product_name)
count = "1"
date = "2023-06-28"
price = "10"
exp_date = "2060-11"


# tests for global testing purpose
# skipped methods which do something small, like printing date
# skipped methods which were dependent on user input
# these methods were tested manually
# these tests are to make sure that after a change the program still works as intended


def test_check_argument():
    assert ArgParse().check_argument("choice", "hello") == "choice"


def test_check_count():
    testObj = ArgParse()
    testObj.count = "5"
    testObj.id_list = id_list
    assert testObj.check_count() is True


def test_check_expiration_date():
    testObj = ArgParse()
    testObj.expiration_date = "2040-09"
    assert testObj.check_expiration_date() is True


def test_check_if_int():
    assert ArgParse().check_if_int("2040-12-01") is True


def test_check_product_name():
    testObj = ArgParse()
    testObj.choice = "sell"
    testObj.product_name = "test"
    assert testObj.check_product_name() is True


def test_buy():
    testObj = ArgParse()
    testObj.product_name = product_name
    testObj.count = count
    testObj.price = price
    testObj.expiration_date = exp_date
    testObj.choice = "test"
    assert testObj.buy() is True


def test_sell():
    testObj = ArgParse()
    testObj.product_name = product_name
    testObj.count = count
    testObj.price = price
    testObj.choice = "test"
    testObj.id_list = id_list
    assert testObj.sell() is True

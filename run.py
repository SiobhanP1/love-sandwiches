"""module docstring"""

import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Collect sales data as input from user.
    """
    while True:
        print("Please enter sales data from the most recent market.")
        print("The data should be six numbers, separated by commas")
        print("Example: 10,20,30,40,50,60\n")
        data_str = input("Enter data here: ")
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there are not exactly six values.
    """
    try:
        values = [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"You entered {len(values)} numbers. Please enter six."
            )
    except ValueError as error:
        print(f"Invalid data:{error} Try again.\n")
        return False
    return True


def update_sales_worksheet(data):
    """
    Update sales data in sales worksheet.
    """
    print("updating sales worksheet with new sales data...\n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('Sales worksheet updated successfully\n')


def calculate_surplus_data(sales_data):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock.
    Positive surplus indicates waste.
    Negative surplus indicates extra made when stock ran out.
    """
    print("Calculating surplus data...")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    print(stock_row)
    pprint(stock)
    surplus = SHEET.worksheet('surplus').get_all_values()
    for x in len(stock[0]):
        surplus[len(stock)][x] = stock[len(stock)][x] - sales_data[len(stock)][x]
    pprint(f"surplus: {surplus[len(stock)]}")


def main():
    """Run all program functions"""
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)


print("Welcome to Love Sandwiches Data Automation\n")
main()



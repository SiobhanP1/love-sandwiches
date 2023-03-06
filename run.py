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


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock.
    Positive surplus indicates waste.
    Negative surplus indicates extra made when stock ran out.
    """
    print("Calculating surplus data...")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    print(f"Stock row: {stock_row}")
    int_stock_row = [int(num) for num in stock_row]
    print(f"Int Stock row: {int_stock_row}")

    surplus_data = []
    for stock,sales in zip(int_stock_row,sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)
    print(f"Surplus Data: {surplus_data}")
    update_worksheet(surplus_data,'surplus')


def update_worksheet(data,worksheet_name):
    """
    Update any worksheet with new row of data
    """
    print(f"Updating {worksheet_name} worksheet...")
    worksheet = SHEET.worksheet(worksheet_name)
    worksheet.append_row(data)
    print(f"Successfully updated {worksheet_name} worksheet")


def get_last_five_sales_entries():
    """
    Get last five entries, add and divide by 5 to get the mean. 
    Increase mean for each by 10% and round up to the nearest integer.
    """
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns


def main():
    """Run all program functions"""
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,'sales')
    calculate_surplus_data(sales_data)
    get_last_five_sales_entries()
    



print("Welcome to Love Sandwiches Data Automation\n")
main()

sales_columns = get_last_five_sales_entries()



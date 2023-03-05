"""module docstring"""

import gspread
from google.oauth2.service_account import Credentials

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
        print(sales_data)
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


data = get_sales_data()

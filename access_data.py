import pandas as pd
import numpy as np


# Function to convert non-serializable data types to serializable formats
def convert_to_serializable(obj):
    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    if isinstance(obj, pd.Timedelta):
        return str(obj)
    if isinstance(obj, pd.Series):
        return obj.tolist()
    if isinstance(obj, pd.DataFrame):
        return obj.to_dict()
    return obj


# Load the Excel workbook
file_path = 'static/media/assets/finances.xlsx'
excel_data = pd.ExcelFile(file_path)

# Dictionary to hold the data
DATA_JSON = {}

# Iterate over each sheet in the workbook
for sheet_name in excel_data.sheet_names:
    # Read the sheet into a DataFrame
    sheet_data = excel_data.parse(sheet_name)

    # Apply the conversion function to each element in the DataFrame
    sheet_data = sheet_data.applymap(convert_to_serializable)

    # Convert the DataFrame to a dictionary and add it to the data dictionary
    DATA_JSON[sheet_name] = sheet_data.to_dict(orient='records')

# Initialize the filtered_data dictionary
filtered_data = {}
total_i_owe_all = 0

# Iterate through the DATA_JSON to calculate the required values
for person, transactions in DATA_JSON.items():
    total_i_paid = 0
    total_he_paid = 0
    payment_methods = {}

    for transaction in transactions:
        i_paid = transaction.get(
            "I paid", 0) if not np.isnan(transaction.get("I paid", 0)) else 0
        he_paid = transaction.get(
            "He/She Paid",
            0) if not np.isnan(transaction.get("He/She Paid", 0)) else 0

        total_i_paid += i_paid
        total_he_paid += he_paid

        payment_method = transaction.get("Payment Method", "")
        if payment_method not in payment_methods:
            payment_methods[payment_method] = {"count": 0, "total": 0}

        payment_methods[payment_method]["count"] += 1
        payment_methods[payment_method]["total"] += i_paid + he_paid

    total_i_owe = total_i_paid - total_he_paid
    total_i_owe_all += total_i_owe

    # Format totals to two decimal places
    filtered_data[person] = {
        "Total I Paid": round(total_i_paid, 2),
        "Total He/She Paid": round(total_he_paid, 2),
        "Total I Owe": round(total_i_owe, 2),
        "Payment Methods": {
            method: {
                "Count": info["count"],
                "Total": round(info["total"], 2)
            }
            for method, info in payment_methods.items()
        }
    }

total_i_owe_all = round(total_i_owe_all, 2)


import pandas as pd


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

import pandas as pd
from .models import Click  # Import your Django model to store coordinates

def load_excel_data(file_path):
    # Load the Excel file and the relevant sheet
    excel_data = pd.ExcelFile(file_path)
    box_data = excel_data.parse('Box Information')  # Load the 'Box Information' sheet

    # Iterate through the data and store X, Y coordinates and other relevant information in the model
    for index, row in box_data.iterrows():
        # Assuming you have columns such as 'Stall Number', 'X Coordinate', 'Y Coordinate', 'Width', 'Height'
        stall_number = row['Stall Number']
        x_coordinate = row['X Coordinate']
        y_coordinate = row['Y Coordinate']
        width = row['Width']
        height = row['Height']
        events = row['Events']  # Assuming Events column exists in the sheet

        # Store the data in the Click model
        Click.objects.create(
            stall_number=stall_number,
            x_coordinate=x_coordinate,
            y_coordinate=y_coordinate,
            width=width,
            height=height,
            events=events  # Store the events data here
        )
    print(f"Data from {file_path} loaded successfully.")

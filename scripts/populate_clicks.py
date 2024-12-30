import os
import sys
import pandas as pd

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstall.settings')
import django
django.setup()

# Import the Click model after Django setup
from book.models import Click

# Absolute file path
file_path_clicks = r'D:\Book-fair\bookstall\book\book_fair-name.xlsx'

def populate_clicks():
    print(f"Looking for file at: {file_path_clicks}")
    if not os.path.exists(file_path_clicks):
        raise FileNotFoundError(f"File not found: {file_path_clicks}")
    data_clicks = pd.read_excel(file_path_clicks, sheet_name="Box Information")

    for _, row in data_clicks.iterrows():
        stall_number = row["Name (stall_number)"]  # Assuming "Name" is the stall identifier
        events = row["Events"]  # Get the events from the "Events" column

        if pd.isna(stall_number):
            print(f"Skipping row with missing stall_number in book_fair-name.xlsx")
            continue

        if not Click.objects.filter(stall_number=stall_number).exists():
            Click.objects.create(
                stall_number=stall_number,
                x_coordinate=row["X"],
                y_coordinate=row["Y"],
                width=row["Width"],
                height=row["Height"],
                # description=f"Area: {row['Area']}",
                events=events  # Save the events data
            )
        else:
            print(f"Skipping duplicate entry for stall_number: {stall_number},{events} in book_fair-name.xlsx")

    print("Data imported successfully.")

if __name__ == "__main__":
    populate_clicks()

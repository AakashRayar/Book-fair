import pandas as pd
from django.core.management.base import BaseCommand
from book.models import Rectangle

class Command(BaseCommand):
    help = 'Import rectangles from an Excel file'
    file_path = r"M:\gitbook\Book-fair\book\box_5_information.xlsx"


    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        self.stdout.write(f"Reading data from {file_path}...")
        data = pd.read_excel(file_path)

        for _, row in data.iterrows():
            Rectangle.objects.create(
                index=row['Index'],
                x=row['X'],
                y=row['Y'],
                width=row['Width'],
                height=row['Height'],
            )
        self.stdout.write(self.style.SUCCESS("Data imported successfully!"))

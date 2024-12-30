# book/management/commands/upload_events_from_excel.py

import openpyxl
from django.core.management.base import BaseCommand
from book.models import Click

class Command(BaseCommand):
    help = 'Upload events to Click model from an Excel file'

    def add_arguments(self, parser):
        # Argument for providing the Excel file path
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        excel_file = kwargs['excel_file']

        try:
            # Load the Excel file
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active

            # Iterate over rows in the Excel sheet
            for row in sheet.iter_rows(min_row=0, values_only=True):  # Assuming the first row is headers
                stall_number = row[6]  # 'Name' column is the first column
                event = row[7]  # 'Events' column is the second column

                # Update the events for the corresponding stall_number
                try:
                    click = Click.objects.get(stall_number=stall_number)
                    click.events = event  # Update the events field
                    click.save()  # Save the changes
                    self.stdout.write(self.style.SUCCESS(f'Updated events for stall {stall_number}'))
                except Click.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Click with stall_number {stall_number} does not exist'))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error processing file: {e}'))

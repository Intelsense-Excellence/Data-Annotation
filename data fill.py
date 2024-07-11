import csv
import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'annotation.settings')  # Replace 'your_project' with your project name
django.setup()

# Import your Django model
from app_main.models import DataAnnotation  # Replace 'your_app' with your app name and 'MyModel' with your model name

# Define the path to the CSV file
csv_file_path = 'audio_transcriptions.csv'  # Replace with your CSV file path


def import_csv(file_path):
    with open(file_path, encoding="utf8", newline='') as file:
        reader = csv.DictReader(file)
        instances = [
            DataAnnotation(
                audio=row['audio_path'],
                transcript=row['transcription']
            )
            for row in reader
        ]
        DataAnnotation.objects.bulk_create(instances)
    print(f'Successfully imported data from "{file_path}"')


if __name__ == '__main__':
    import_csv(csv_file_path)

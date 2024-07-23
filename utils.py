"""Utils for project."""
import os
from datetime import datetime
from zipfile import ZipFile


def create_zip_archive(files):
    """Create a ZIP archive from a list of files."""
    zip_file_name = f'result_{datetime.now().strftime("%d-%m-%Y")}.zip'
    with ZipFile(zip_file_name, 'w') as zipf:
        for file in files:
            zipf.write(file, os.path.basename(file))
    return zip_file_name


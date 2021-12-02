import sys
import dropbox
import os
from dropbox.files import WriteMode

# Access token
token = 'KjuflX1NCx4AAAAAAAAAAZC_0k_v9uPmWOQgRbWiuT1vaQBL8f7Zmmr38MQgCvk0'

def upload_file_to_dropbox(token: str, locafile_path: str, cloud_path: str):
    dbx = dropbox.Dropbox(token)
    print(f"Uploading '{os.path.basename(locafile_path)}'")
    with open(locafile_path, "rb") as file:
        dbx.files_upload(file.read(), cloud_path, mode=WriteMode('overwrite'))
    print("Upload completed!")

upload_file_to_dropbox(token, "car_data.xlsx", "/car_database/car_data.xlsx")


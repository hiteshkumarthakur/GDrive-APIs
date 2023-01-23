from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import pkg_resources
from datetime import date
import sys
import os


def upload_file_to_gdrive():
    gauth = GoogleAuth()
    # NOTE: if you are getting storage quota exceeded error, create a new service account, and give that service account permission to access the folder and replace the google_credentials.
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        pkg_resources.resource_filename(__name__, "credentials.json"), scopes=['https://www.googleapis.com/auth/drive'])

    drive = GoogleDrive(gauth)
    today = date.today().strftime("%m/%d/%y")

    folder_name = "New Folder"
    parent_directory_id = '1KSWrfio_8n8uyvHoAWqu7xhHdKkQ8GvR'

    folder_meta = {
        "title":  folder_name,
        "parents": [{'id': parent_directory_id}],
        'mimeType': 'application/vnd.google-apps.folder'
    }

    # check if folder already exist or not
    folder_id = None
    foldered_list = drive.ListFile(
        {'q':  "'"+parent_directory_id+"' in parents and trashed=false"}).GetList()

    for file in foldered_list:
        if (file['title'] == folder_name):
            folder_id = file['id']

    if folder_id == None:
        folder = drive.CreateFile(folder_meta)
        folder.Upload()
        folder_id = folder.get("id")

    file1 = drive.CreateFile(
        {'parents': [{"id": folder_id}], 'title': 'file.txt'})
    
    file1.SetContentFile('file.txt')
    file1.Upload()
    print("\n--------- File is Uploaded ----------")
    
upload_file_to_gdrive()

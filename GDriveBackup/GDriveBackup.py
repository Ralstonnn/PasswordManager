from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

FOLDER_WITH_TOKEN_AND_CREDENTIAL = 'GDriveBackup\\'

SCOPES = ['https://www.googleapis.com/auth/drive']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists(f'{FOLDER_WITH_TOKEN_AND_CREDENTIAL}token.pickle'):
    with open(f'{FOLDER_WITH_TOKEN_AND_CREDENTIAL}token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            f'{FOLDER_WITH_TOKEN_AND_CREDENTIAL}credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
# Save the credentials for the next run
    with open(f'{FOLDER_WITH_TOKEN_AND_CREDENTIAL}token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('drive', 'v3', credentials=creds)


def google_drive_upload_file(path: str):

    file_name_with_extention = str(path.split('\\')[-1])
    file_extention = str(file_name_with_extention.split('.')[-1])

    results = service.files().list(q=f"name = '{file_name_with_extention}'",
                                   spaces='drive',
                                   fields='nextPageToken, files(id, name)',
                                   pageToken=None).execute()

    try:
        found_file_id = results['files'][0]['id']
        found_file_name = results['files'][0]['name']

        print(f'\nFile on Google Drive was updated, file ID: {found_file_id}')

        file_metadata = {'name': f'{file_name_with_extention}'}
        media = MediaFileUpload(fr'{path}',
                                mimetype=f'text/{file_extention}')
        upload_new_created_file = service.files().update(body=file_metadata, media_body=media,
                                                         fileId=found_file_id).execute()
    except:

        print('\nNew file was created on google drive')

        file_metadata = {'name': f'{file_name_with_extention}'}
        media = MediaFileUpload(fr'{path}',
                                mimetype=f'text/{file_extention}')
        upload_new_created_file = service.files().create(body=file_metadata, media_body=media,
                                                         fields='id').execute()

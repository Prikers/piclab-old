import json
import os

from google.oauth2.service_account import Credentials
from google.cloud import secretmanager

from storages.backends.gcloud import GoogleCloudStorage

GOOGLE_CLOUD_PROJECT = os.environ.get('GOOGLE_CLOUD_PROJECT')


class StaticGoogleCloudStorage(GoogleCloudStorage):
    bucket_name = 'piclab-static'
    location = 'static/'
    file_overwrite = True
    default_acl = 'publicRead'


def get_secret(secret_id, project_id=GOOGLE_CLOUD_PROJECT, version_id=1):
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={
        'name': f'projects/{project_id}/secrets/{secret_id}/versions/{version_id}'
    })
    data = response.payload.data.decode('UTF-8')
    return data

def get_credentials(secret_id, project_id=GOOGLE_CLOUD_PROJECT, version_id=1): 
    data = get_secret(secret_id, project_id=project_id, version_id=version_id)
    data = json.loads(data)
    credentials = Credentials.from_service_account_info(data)
    return credentials

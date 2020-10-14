import json

from google.oauth2.service_account import Credentials
from google.cloud import secretmanager

from storages.backends.gcloud import GoogleCloudStorage


class StaticGoogleCloudStorage(GoogleCloudStorage):
    location = 'static/'
    file_overwrite = False


def get_credentials(project_id, secret_id, version_id): 
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={
        'name': f'projects/{project_id}/secrets/{secret_id}/versions/{version_id}'
    })
    data = json.loads(response.payload.data.decode('UTF-8'))
    credentials = Credentials.from_service_account_info(data)
    return credentials

from storages.backends.gcloud import GoogleCloudStorage


class StaticGoogleCloudStorage(GoogleCloudStorage):
    location = 'static/'
    file_overwrite = False

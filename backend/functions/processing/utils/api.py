from datetime import datetime
import os
import uuid

import requests


class API:

    def __init__(self, project, file):
        self.project = project
        self.file = file
        self.host = os.environ.get('GOOGLE_CLOUD_HOST_URL')
        self.base_url = f'https://{self.host}/api'
        self.token = self.obtain_token()
        self.headers = {'Authorization': f'Bearer {self.token}'}
        self.photo = self.get_photo()

    def obtain_token(self):
        response = requests.post(f'{self.base_url}/token/', {
            'email': os.environ.get('CLOUD_FUNCTION_EMAIL'),
            'password': os.environ.get('CLOUD_FUNCTION_PASSWORD'),
        })
        token = response.json()['access']
        return token

    def get_photo(self):
        url = f'{self.base_url}/photos/?project={self.project}&search={self.file}'
        photo = requests.get(url=url, headers=self.headers).json()
        if len(photo) == 0:
            raise ValueError(f'Failed retrieving {self.file.name} at url {url}')
        return photo[0]

    def post_thumbnail(self, thumb_file):
        url = f'{self.base_url}/photos/{self.photo["id"]}/?project={self.project}'
        files=[('thumbnail', (self.file.name, open(thumb_file, 'rb'), 'image/jpeg'))]
        response = requests.patch(url=url, headers=self.headers, files=files)
        print(f'Thumbnail for {self.file} has been posted', response)

    def post_photo_metadata(self, metadata):
        url = f'{self.base_url}/photos/{self.photo["id"]}/?project={self.project}'
        response = requests.patch(url=url, headers=self.headers, data=metadata)
        print(f'Exif data for {self.file} has been added', response)

    def post_hash_data(self, hash_value):
        # Create the Hash entry in database
        url = f'{self.base_url}/hash/?project={self.project}'
        data = {'photo': self.photo['id'], 'hash': hash_value}
        creation = requests.post(url=url, headers=self.headers, data=data)
        print(f'Hash creation for {self.file}: ID {creation.json()["id"]}')

        # Check for potential duplicates by searching hash value in database
        url = f'{self.base_url}/hash/?project={self.project}&hash={hash_value}'
        duplicates = requests.get(url=url, headers=self.headers).json()
        if len(duplicates) > 1:  # There are duplicates
            # Retrieve existing duplicate id if there is none - otherwise create it
            # Duplicate id needs to be created the first time the hash appears as a duplicate
            duplicate_id = duplicates[0].get('duplicate_id')
            if duplicate_id is None:
                duplicate_id = str(uuid.uuid4())
            # Add duplicate information to the payload
            payload = {
                'duplicate_id': duplicate_id,
                'is_duplicated': True,
                'status': 1,
                'date_status': datetime.now().isoformat(),
            }
            # Patch all hash ids
            ids = [d['id'] for d in duplicates]
            for id_ in [d['id'] for d in duplicates]:
                url=f'{self.base_url}/hash/{id_}/?project={self.project}'
                requests.patch(url=url, headers=self.headers, data=payload)
            print(f'Duplicates identified for {self.file.name} - IDs: {ids}')

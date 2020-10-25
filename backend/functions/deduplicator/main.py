import os
from pathlib import Path
import tempfile

from google.cloud import storage
from PIL import Image
import requests


def main(event, context):
    '''https://cloud.google.com/storage/docs/json_api/v1/objects#resource'''
    # Prevent processing when saving other images (thumbnails, etc.) to the bucket
    file = Path(event['name'])
    if file.parent.name != 'originals':
        return

    storage_client = storage.Client()
    bucket = storage_client.bucket(event['bucket'])
    blob = bucket.get_blob(str(file))

    # Download image to a temporary file
    _, tmp_file = tempfile.mkstemp()
    tmp_file = tmp_file + file.suffix
    blob.download_to_filename(tmp_file)
    print(f'Image {file} was downloaded to {tmp_file}.')

    # Processing chain
    image = Image.open(tmp_file)
    generate_thumbnail(image, file, bucket)

    # Delete the temporary file.
    os.remove(tmp_file)

    # Test a request
    test_request()


def generate_thumbnail(image, file, bucket):
    # Create the thumbnail
    thumbnail_size = 128, 128
    # image = Image.open(tmp_file)
    image.thumbnail(thumbnail_size)
    image.save(image.filename)
    # Save the thumbnail in the bucket
    thumbnail = str(file.parent.parent / 'thumbnails' / file.name)
    new_blob = bucket.blob(thumbnail)
    new_blob.upload_from_filename(image.filename)
    print(f'Thumbnail uploaded to: {thumbnail}')


def test_request():
    host = os.environ.get('GOOGLE_CLOUD_HOST_URL')
    response = requests.post(f'https://{host}/api/token/', {
        'email': os.environ.get('CLOUD_FUNCTION_EMAIL'),
        'password': os.environ.get('CLOUD_FUNCTION_PASSWORD'),
    })
    token = response.json()['access']
    project = 2
    requests.patch(
        url=f'https://{host}/api/photos/31/?project={project}',
        data={'is_liked': 'true'},
        headers={'Authorization': f'Bearer {token}'},
    )

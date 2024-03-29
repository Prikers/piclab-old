import os
from pathlib import Path
import tempfile

from google.cloud import storage
from PIL import Image

from utils.api import API
from utils.deduplicator import generate_hash
from utils.metadata import get_metadata
from utils.thumbnails import generate_thumbnail

def main(event, context):
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
    project = int(file.parent.parent.name.split('.')[0])
    image = Image.open(tmp_file)
    metadata = get_metadata(image, tmp_file)
    hash_ = generate_hash(image)
    thumb_file = generate_thumbnail(image.copy(), tmp_file)

    # Save results
    api = API(project, file)
    api.post_hash_data(hash_)
    api.post_photo_metadata(metadata)
    api.post_thumbnail(thumb_file)

    # Delete the temporary files
    os.remove(tmp_file)
    os.remove(thumb_file)

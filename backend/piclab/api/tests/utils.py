from io import BytesIO
from pathlib import Path
import shutil

from django.conf import settings
from django.core.files import File
from PIL import Image

def remove_test_images():
    # Make sure to delete the tmp files after running tests    
    tmp_folder = settings.MEDIA_ROOT
    # Ensure the deleted folder is the expected one
    assert tmp_folder == './tmp-tests'
    # Ensure the tmp folder only contains tmp test images
    tmp_files = [(f.stem, f.suffix) for f in Path(tmp_folder).rglob('*') if f.is_file()]
    assert all([stem.startswith('test') and suffix in ('.jpg', '.jpeg', '.png') for (stem, suffix) in tmp_files])
    # Clean up all files
    shutil.rmtree(tmp_folder, ignore_errors=True)

def get_image_file(name='test.jpg', ext='jpeg', size=(50, 50), color=(256, 0, 0)):
    file = BytesIO()
    image = Image.new('RGB', size=size, color=color)
    image.save(file, ext)
    file.seek(0)
    return File(file=file, name=name)

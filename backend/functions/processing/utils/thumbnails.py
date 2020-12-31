from pathlib import Path

from PIL import ImageOps

def generate_thumbnail(image, tmp_file, thumbnail_size=(400, 400)):
    tmp_file = Path(tmp_file)
    thumb_file = str(tmp_file).replace(tmp_file.stem, tmp_file.stem + '_thumbnail')
    image.thumbnail(thumbnail_size)
    image = ImageOps.exif_transpose(image)  # Apply EXIF orientation, otherwise initial orientation is lost
    image.save(thumb_file)
    return thumb_file

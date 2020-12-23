import json
import os
from datetime import datetime

from PIL import ExifTags
from PIL.TiffImagePlugin import IFDRational

def get_metadata(image, file):
    # Extract exif information
    stat = os.stat(file)
    raw_exif = dict(image.getexif())
    # Retrieve exif info but without comments
    # TODO - improve the parsing of unicode strings instead of deleting
    exclude_exif_keys = ['UserComment', 'MakerNote', 'GPSInfo', 'ComponentsConfiguration', 'SceneType']
    exif = {}
    for key, val in raw_exif.items():
        if key in ExifTags.TAGS and ExifTags.TAGS[key] not in exclude_exif_keys:
            if isinstance(val, bytes):
                exif[ExifTags.TAGS[key]] = val.decode('utf-8')
            elif isinstance(val, IFDRational):
                exif[ExifTags.TAGS[key]] = float(val)
            else:
                exif[ExifTags.TAGS[key]] = val
    # Construct Metadata dict
    metadata = {
        'width': image.width,
        'height': image.height,
        'file_size': stat.st_size,
        'exif': json.dumps(exif),
    }
    if 'DateTimeOriginal' in exif.keys():
        metadata['datetime_photo'] = datetime.strptime(
            exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
    if 'XResolution' and 'YResolution' in exif.keys():
        metadata['dpi'] = f'({exif["XResolution"]}, {exif["YResolution"]})'
    if 'Make' and 'Model' in exif.keys():
        metadata['camera'] = f'{exif["Make"]} {exif["Model"]}'
    # GPS Metadata
    if 'GPSInfo' in raw_exif.items():
        gps = {
            ExifTags.GPSTAGS.get(key): val for key, val in raw_exif['GPSInfo']
            if key in ExifTags.TAGS
        }
        if 'GPSLatitude' and 'GPSLongitude' in gps.keys():
            metadata['longitude'] = gps['GPSLongitude']
            metadata['latitude'] = gps['GPSLatitude']

    return metadata

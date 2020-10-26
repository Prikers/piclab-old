def generate_thumbnail(image, file, bucket,
                       thumbnail_size=(128, 128)):
    # Create the thumbnail
    image.thumbnail(thumbnail_size)
    image.save(image.filename)
    # Save the thumbnail in the bucket
    thumbnail = str(file.parent.parent / 'thumbnails' / file.name)
    new_blob = bucket.blob(thumbnail)
    new_blob.upload_from_filename(image.filename)
    print(f'Thumbnail uploaded to: {thumbnail}')

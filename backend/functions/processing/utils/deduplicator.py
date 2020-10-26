import numpy as np
from PIL import Image

def generate_hash(image, hash_size=8):
    images, hashes = [image], []
    for angle in (90, 180, 270):
        images.append(image.rotate(angle, expand=True))
    for im in images:
        small_array = np.array(
            im.convert(mode='L')
            .resize((hash_size, hash_size), Image.LANCZOS)
        )
        barcode = small_array > small_array.mean()
        hashes.append(
            sum([2 ** i for (i, v) in enumerate(barcode.flatten()) if v])
        )
    return ''.join([str(h) for h in sorted(hashes)])

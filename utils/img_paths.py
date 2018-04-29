import os.path
import hashlib

HASH_CHUNK_SIZE = 65536


def get_img_path(instance, filename):
    parts = os.path.splitext(filename)
    ctx = hashlib.sha256()
    if instance.img.multiple_chunks():
        for data in instance.img.chunks(HASH_CHUNK_SIZE):
            ctx.update(data)
    else:
        ctx.update(instance.img.read())
    hex_path = ctx.hexdigest()
    return '{0}/{1}/{2}/{3}{4}'.format(
        instance._meta.model_name,
        hex_path[0:2],
        hex_path[2:18],
        hex_path[18:34],
        parts[1]
    )

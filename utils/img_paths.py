HASH_CHUNK_SIZE = 65536

def get_img_path(base_path):
    def get_path(instance, filename):
        import os.path
        import hashlib
        parts = os.path.splitext(filename)
        ctx = hashlib.sha256()
        if instance.img.multiple_chunks():
            for data in instance.avatar.chunks(HASH_CHUNK_SIZE):
                ctx.update(data)
        else:
            ctx.update(instance.avatar.read())
        hex_path = ctx.hexdigest()
        return '{0}/{1}/{2}/{3}{4}'.format(
            base_path,
            hex_path[0:2],
            hex_path[2:18],
            hex_path[18:34],
            parts[1]
        )

    return get_path

import hashlib
from fastapi import UploadFile

async def calculate_file_md5(file: UploadFile, content: bytes = None):
    md5 = hashlib.md5()
    if content is not None:
        md5.update(content)
        return md5.hexdigest()

    chunk_size = 4096
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        md5.update(chunk)

    await file.seek(0)
    return md5.hexdigest()
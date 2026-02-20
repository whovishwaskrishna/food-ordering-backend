import os
import uuid

UPLOAD_DIR = "app/uploads"

def save_file(file):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return f"/uploads/{filename}"
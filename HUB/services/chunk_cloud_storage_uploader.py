import hashlib
import logging
import os
from io import BytesIO

from google.cloud import storage

from HUB import settings

logger = logging.getLogger(__name__)


class ChunkCloudStorageUploader:
    TEMP_STORAGE = storage.Client(project=None, credentials=settings.GS_CREDENTIALS)
    TEMP_BUCKET = TEMP_STORAGE.get_bucket(settings.GS_TEMP_BUCKET_NAME)
    TEMP_DIR = settings.GS_TEMP_UPLOAD_DIR

    @classmethod
    def get_temp_path(cls, name):
        return os.path.join(cls.TEMP_DIR, name)

    @classmethod
    def save_temp(cls, resumable_file_name, resumable_chunk_number, file_data):
        temp_path = cls.get_temp_path(cls.get_chunk_name(resumable_file_name, resumable_chunk_number))
        blob = cls.TEMP_BUCKET.blob(temp_path)
        if not blob.exists():
            blob.upload_from_file(file_data)

    @classmethod
    def all_uploaded(cls, resumable_file_name, resumable_total_chunks):
        chunk_paths = cls.get_chunk_paths(resumable_file_name, resumable_total_chunks)
        return all([cls.TEMP_BUCKET.blob(cls.get_temp_path(p)).exists() for p in chunk_paths])

    @classmethod
    def merge_chunks(cls, resumable_file_name, resumable_total_chunks):
        chunk_paths = cls.get_chunk_paths(resumable_file_name, resumable_total_chunks)
        merged_file = BytesIO()
        for chunk_path in chunk_paths:
            temp_chunk_path = cls.get_temp_path(chunk_path)
            cloud_chunk_file = cls.TEMP_BUCKET.blob(temp_chunk_path)
            with BytesIO() as temp_chunk_file:
                cloud_chunk_file.download_to_file(temp_chunk_file)
                temp_chunk_file.seek(0)
                merged_file.write(temp_chunk_file.read())
        merged_file.seek(0)
        return merged_file

    @classmethod
    def get_chunk_paths(cls, resumable_file_name, resumable_total_chunks):
        return [cls.get_chunk_name(resumable_file_name, x) for x in range(1, resumable_total_chunks + 1)]

    @classmethod
    def get_chunk_name(cls, uploaded_filename, chunk_number):
        return hashlib.sha256(uploaded_filename.encode("UTF-8")).hexdigest() + "_part_" + str(chunk_number)

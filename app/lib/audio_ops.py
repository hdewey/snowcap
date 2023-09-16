import os
import uuid
from pydub import AudioSegment
import tempfile

from fastapi import UploadFile

class AudioOperations:
    UPLOAD_FOLDER = None # Shared across instances
    ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm'}

    def __init__(self):
        if AudioOperations.UPLOAD_FOLDER is None:
            AudioOperations.UPLOAD_FOLDER = tempfile.mkdtemp()
            os.makedirs(os.path.join(AudioOperations.UPLOAD_FOLDER, 'tmp_uploads'), exist_ok=True)

    def allowed_file(self, file_extension):
        return file_extension in self.ALLOWED_EXTENSIONS

    def save_file(self, file: UploadFile):
        file_extension = file.filename.split('.')[-1].lower()
        if file and self.allowed_file(file_extension):
            generated_filename = f"{uuid.uuid4()}.{file_extension}"
            directory = os.path.join(self.UPLOAD_FOLDER, "tmp_uploads")
            if not os.path.exists(directory):
                os.makedirs(directory)
            file_path = os.path.join(directory, generated_filename)
            
            # file.file is a spoofed temporary file!
            with open(file_path, "wb") as buffer:
                contents = file.file.read()
                buffer.write(contents)
            
            return generated_filename
        else:
            raise ValueError("Invalid file type or no file provided.")

    def load_file(self, generated_filename):
        file_path = os.path.join(self.UPLOAD_FOLDER, 'tmp_uploads', generated_filename)
        if os.path.exists(file_path):
            return file_path
        else:
            raise FileNotFoundError("File with given generated filename not found.")
        
    def remove_file(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)
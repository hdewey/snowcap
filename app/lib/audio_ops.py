import os
import uuid
from pydub import AudioSegment
import tempfile

from fastapi import UploadFile

class AudioOperations:
    UPLOAD_FOLDER = "/tmp/recordings"  # Shared across instances
    ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm'}

    def allowed_file(self, file_extension):
        return file_extension in self.ALLOWED_EXTENSIONS

    def save_file(self, file: UploadFile):
        file_extension = file.filename.split('.')[-1].lower()
        if file and self.allowed_file(file_extension):
            generated_filename = f"{uuid.uuid4()}.{file_extension}"
            if not os.path.exists(self.UPLOAD_FOLDER):
                os.makedirs(self.UPLOAD_FOLDER)
            file_path = os.path.join(self.UPLOAD_FOLDER, generated_filename)
            
            # file.file is a spoofed temporary file!
            with open(file_path, "wb") as buffer:
                contents = file.file.read()
                buffer.write(contents)
            
            return file_path
        else:
            raise ValueError("Invalid file type or no file provided.")
        
    def remove_file(self, filepath):
        if os.path.exists(filepath):
            # os.remove(filepath)
            return
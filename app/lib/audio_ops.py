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
        print(f"Saving a {file_extension} file.")
        if file and self.allowed_file(file_extension):
            generated_filename = f"{uuid.uuid4()}.{file_extension}"
            if not os.path.exists(self.UPLOAD_FOLDER):
                os.makedirs(self.UPLOAD_FOLDER)
            file_path = os.path.join(self.UPLOAD_FOLDER, generated_filename)
            
            # file.file is a spoofed temporary file!
            with open(file_path, "wb") as buffer:
                contents = file.file.read()
                buffer.write(contents)
            
            # Convert MP4 files to WAV
            if file_extension == "mp4":
                file_path = self.convert_to_wav(file_path)
            
            return file_path
        else:
            raise ValueError("Invalid file type or no file provided.")
        
    def convert_to_wav(self, file_path):
        """Converts the given file to WAV format."""
        audio = AudioSegment.from_file(file_path, format="mp4")  # load mp4
        wav_file_path = file_path.rsplit('.', 1)[0] + ".wav"
        audio.export(wav_file_path, format="wav")  # export as WAV
        
        # Optional: Remove the original .mp4 file after conversion
        os.remove(file_path)
        
        return wav_file_path
        
    def remove_file(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)
            return
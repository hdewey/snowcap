import os
import uuid
from pydub import AudioSegment
import tempfile

from fastapi import UploadFile

class AudioOperations:
    UPLOAD_FOLDER = "/tmp/recordings"  # shared file system
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

            print(f"Before Changing File Type:")
            print(self.get_audio_info(file_path))
            
            if file_extension == "mp4":
                file_path = self.convert_to_wav(file_path)

                print(f"After Changing File Type:")
                print(self.get_audio_info(file_path))
            
            return file_path
        else:
            raise ValueError("Invalid file type or no file provided.")
        
    def convert_to_wav(self, file_path):
        """Converts the given file to WAV format."""
        audio = AudioSegment.from_file(file_path, format="mp4")
        wav_file_path = file_path.rsplit('.', 1)[0] + ".wav"
        audio.export(wav_file_path, format="wav")
        
        os.remove(file_path)
        
        return wav_file_path
        
    def remove_file(self, filepath):
        if os.path.exists(filepath):
            os.remove(filepath)
            return
    def get_audio_info(self, file_path):
        audio = AudioSegment.from_file(file_path)
        
        file_size = os.path.getsize(file_path)
        
        info = {
            "length_ms": len(audio),
            "length_seconds": len(audio) / 1000, 
            "channels": audio.channels,  # int
            "frame_rate": audio.frame_rate,
            "frame_width": audio.frame_width,  # bytes
            "sample_width": audio.sample_width * 8,  # bits
            "file_size_bytes": file_size,
            "file_size_kb": file_size / 1024, 
            "file_size_mb": file_size / (1024 * 1024)
        }

        return info
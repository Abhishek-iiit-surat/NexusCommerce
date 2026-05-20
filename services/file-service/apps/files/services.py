from .models import UploadedFile
from .exceptions import FileNotFoundException, FileUploadError, UnsupportedFileFormatError
import cloudinary
import cloudinary.uploader
from django.conf import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

class FileService:

    def cloudinary_upload(self, file):
        if file.content_type not in ['image/jpeg', 'image/png', 'image/webp', 'image/gif']:
            raise UnsupportedFileFormatError("Unsupported file format for Product Image. Allowed formats: JPEG, PNG, WEBP, GIF.")
        
        try:
            result = cloudinary.uploader.upload(
                        file,
                        quality="auto",
                        fetch_format="auto",
                    )
        except Exception as e:
            raise FileUploadError("Error occurred while uploading file to Cloudinary.")
        return result.get('secure_url'), result.get('public_id')
    
    def upload_file(self, file, uploaded_by):
        url , public_id = self.cloudinary_upload(file)

        new_file = UploadedFile.objects.create(
            cloudinary_url=url,
            public_id=public_id,
            original_name=file.name,
            mime_type=file.content_type,
            size=file.size,
            uploaded_by=uploaded_by
        )
        return new_file
    
    def get_file(self, file_id):
        try:
            file = UploadedFile.objects.get(id=file_id)
            return file
        except UploadedFile.DoesNotExist:
            raise FileNotFoundException("File not found.")
        
    def delete_file(self, file_id, user_id):
        file = UploadedFile.objects.filter(id=file_id, uploaded_by=user_id).first()
        if not file:
            raise FileNotFoundException("File not found.")
        public_id = file.public_id
        cloudinary.uploader.destroy(public_id)
        file.delete()  
        return True
    

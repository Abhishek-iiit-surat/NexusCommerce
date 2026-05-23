from .models import UploadedFile
from .exceptions import FileNotFoundException, FileUploadError, UnsupportedFileFormatError
import cloudinary
import cloudinary.uploader
class FileService:

    def cloudinary_upload(self, file, resource_type, resource_id, slot):
        if file.content_type not in ['image/jpeg', 'image/png', 'image/webp', 'image/gif']:
            raise UnsupportedFileFormatError("Unsupported file format for Product Image. Allowed formats: JPEG, PNG, WEBP, GIF.")

        if resource_type and resource_id and slot:
            public_id = f"nexuscommerce/{resource_type}/{resource_id}/{slot}"
        else:
            public_id = f"nexuscommerce/misc/{file.name}"

        try:
            result = cloudinary.uploader.upload(
                        file,
                        quality="auto",
                        public_id=public_id,
                        fetch_format="auto",
                        overwrite=True
                    )
        except Exception as e:
            print(f"Cloudinary error: {e}")
            raise FileUploadError("Error occurred while uploading file to Cloudinary.")
        return result.get('secure_url'), result.get('public_id')

    def upload_file(self, uploaded_by, **resource_info):
        resource_type = resource_info.get('resource_type')
        resource_id = resource_info.get('resource_id')
        slot = resource_info.get('slot')
        file = resource_info.get('file')
        url, public_id = self.cloudinary_upload(file, resource_type, resource_id, slot)

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
        result = cloudinary.uploader.destroy(public_id)
        if result.get('result') not in ['ok', 'not found']:
            raise FileUploadError("Error occurred while deleting file from Cloudinary.")
        file.delete()  
        return True
    

from django.db import models

class UploadedFile(models.Model):
    cloudinary_url  = models.URLField(max_length = 500)
    public_id = models.CharField(max_length=255, unique=True)
    original_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    size = models.PositiveIntegerField()
    uploaded_by = models.IntegerField()  # Store user ID who uploaded the file
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
          return self.cloudinary_url

    class Meta:
        ordering = ['-created_at']
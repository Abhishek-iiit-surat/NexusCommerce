from django.db import models

class UploadedFile(models.Model):
    cloudinary_url  = models.URLField(max_length = 500)
    resource_type = models.CharField(max_length=50, null=True, blank=True)
    resource_id = models.IntegerField(null=True, blank=True)
    slot = models.CharField(max_length=50, null=True, blank=True)
    public_id = models.CharField(max_length=255, unique=True)
    original_name = models.CharField(max_length=255, null=True, blank=True)
    mime_type = models.CharField(max_length=100, null=True, blank=True)
    size = models.PositiveIntegerField()
    uploaded_by = models.IntegerField()  # Store user ID who uploaded the file
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
          return self.cloudinary_url

    class Meta:
        ordering = ['-created_at']
        indexes = [
             models.Index(fields=['resource_type', 'resource_id']),
        ]
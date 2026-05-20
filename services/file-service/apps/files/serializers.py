from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import UploadedFile

class FileResponseSerializer(ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'cloudinary_url',  'original_name', 'mime_type', 'size', 'uploaded_by', 'created_at']
        read_only_fields = ['id','created_at','uploaded_by']

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
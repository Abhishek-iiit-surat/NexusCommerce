from django.db import models
class GenderChoices(models.TextChoices):
    MALE = 'male' , 'MALE'
    FEMALE = 'female', 'FEMALE'
    PREFER_NOT_TO_SAY = 'prefer_not_to_say', 'PREFER_NOT_TO_SAY'
    
class UserProfile(models.Model):
    user_id = models.IntegerField(unique=True)
    avatar = models.URLField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True, choices=GenderChoices.choices)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Address(models.Model):
    user_id = models.IntegerField()
    label = models.CharField(max_length=50)  # e.g., 'home', 'work'
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=20)
    is_default_shipping = models.BooleanField(default=False)
    is_default_billing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']

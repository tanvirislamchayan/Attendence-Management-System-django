from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from departments.models import Department
from base.models import BaseModel
import os
from django.dispatch import receiver
# Create your models here.

MOBILE_REGEX = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)



class Designation(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Designation, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name



class Teacher(BaseModel):
    is_active = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher')
    mobile_number = models.CharField(max_length=15, unique=True, validators=[MOBILE_REGEX])
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='teacher_images/', null=True, blank=True)


    def save(self, *args, **kwargs):
        # Check if the instance is being updated (not created)
        if self.pk:
            try:
                old_instance = Teacher.objects.get(pk=self.pk)
                # If the image is being updated, delete the old image
                if old_instance.image and old_instance.image != self.image:
                    old_instance.image.delete(save=False)
            except Teacher.DoesNotExist:
                # If the instance does not exist, skip the old image deletion
                pass
        return super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Delete the associated image file when the instance is deleted
        if self.image:
            self.image.delete(save=False)
        return super().delete(*args, **kwargs)
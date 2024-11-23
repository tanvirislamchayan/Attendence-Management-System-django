from django.db import models
from django.utils.text import slugify

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True) #slug will help to get linking like this "Poduct Image => product-image"
    details = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='department_images/', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.pk:
            print(self.pk)
            old_instance = Department.objects.get(pk=self.pk)
            # If the image is being updated, delete the old image
            if old_instance.image and old_instance.image != self.image:
                old_instance.image.delete(save=False)

        return super(Department, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Delete the associated image file when the instance is deleted
        if self.image:
            self.image.delete(save=False)
        return super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

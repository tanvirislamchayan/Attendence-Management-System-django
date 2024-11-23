from django.db import models
from django.utils.text import slugify

# Create your models here.

class Semester(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Semester, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
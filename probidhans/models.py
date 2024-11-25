from django.db import models
from django.utils.text import slugify

# Create your models here.
class Probidhan(models.Model):
    name = models.PositiveIntegerField(null=True, blank=True)  # Only allows integers
    slug = models.SlugField(unique=True, null=True, blank=True)
    starting_year = models.PositiveIntegerField(null=True, blank=True)  # Only positive integers

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.name)  # Cast to string for representation

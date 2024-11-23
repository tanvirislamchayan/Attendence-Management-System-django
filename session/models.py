from django.db import models
from django.utils.text import slugify

# Create your models here.

class Session(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    starting_year = models.CharField(max_length=10, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Session, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
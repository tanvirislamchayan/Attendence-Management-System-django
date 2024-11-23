from django.db import models
from django.utils.text import slugify
from semesters.models import Semester
from departments.models import Department
from probidhans.models import Probidhan
from django.core.exceptions import ValidationError
# Create your models here.

def validate_numeric(value):
    if not value.replace('.', '', 1).isdigit():  # Allows decimals like "3.5"
        raise ValidationError(f"{value} is not a valid number.")

class Subject(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=8, null=True, blank=True, validators=[validate_numeric])
    slug = models.SlugField(unique=True, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True, related_name='subjects')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True, related_name='subjects')
    probidhan = models.ForeignKey(Probidhan, on_delete=models.CASCADE, null=True, blank=True, related_name='subjects')
    theory = models.CharField(max_length=5, null=True, blank=True, validators=[validate_numeric])
    practical = models.CharField(max_length=5, null=True, blank=True, validators=[validate_numeric])
    credit = models.CharField(max_length=5, null=True, blank=True, validators=[validate_numeric])

    def save(self, *args, **kwargs):
        line = f'{self.name} {self.code}'
        self.slug = slugify(line)
        return super(Subject, self).save(*args, **kwargs)
    
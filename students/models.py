from django.db import models
from base.models import BaseModel
from django.core.exceptions import ValidationError
from departments.models import Department
from semesters.models import Semester
from session.models import Session
from probidhans.models import Probidhan
from groups.models import Group

# Create your models here.

def validate_numeric(value):
    # Convert the value to string if it's an integer or float
    value = str(value)
    if not value.replace('.', '', 1).isdigit():  # Allows decimals like "3.5"
        raise ValidationError(f"{value} is not a valid number.")



class Student(BaseModel):
    name = models.CharField(max_length=50)
    roll = models.PositiveIntegerField(null=True, blank=True, validators=[validate_numeric])
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    probidhan = models.ForeignKey(Probidhan, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.roll} - {self.name}"

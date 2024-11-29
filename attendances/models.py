from django.db import models
from teachers.models import Teacher
from students.models import Student
from subjects.models import Subject
from semesters.models import Semester
from departments.models import Department
from django.utils.dateformat import format

class Attendance(models.Model):
    date = models.DateField()
    month = models.CharField(max_length=20, null=True, blank=True)  # Auto-filled
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ManyToManyField(Student)

    def save(self, *args, **kwargs):
        # Automatically set the `month` field based on the `date`
        if self.date:
            self.month = format(self.date, "F - Y")  # E.g., "November - 2024"
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"Attendance for {self.date} ({self.semester}, {self.department})"

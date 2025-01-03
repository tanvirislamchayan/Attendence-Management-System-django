from django.db import models
from teachers.models import Teacher
from students.models import Student
from subjects.models import Subject
from semesters.models import Semester
from departments.models import Department
from groups.models import Group
from django.utils.dateformat import format
from datetime import datetime

class Attendance(models.Model):
    date = models.DateField()
    month = models.CharField(max_length=20, null=True, blank=True)  # Auto-filled
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    student_presents = models.ManyToManyField(Student, related_name="attendances_present", blank=True)
    student_absents = models.ManyToManyField(Student, related_name="attendances_absent", blank=True, )

    def save(self, *args, **kwargs):
        # Ensure `self.date` is a datetime.date object
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, "%Y-%m-%d").date()
        if self.date:
            self.month = format(self.date, "F - Y")  # Format month as "November - 2024"
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Attendance for {self.subject.name if self.subject else None}, {self.department.name if self.department else None}, {self.semester.name if self.semester else None} on {self.date if self.date else None}"


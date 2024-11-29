from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'month', 'teacher', 'subject', 'semester', 'department')
    list_filter = ('department', 'semester', 'month')
    search_fields = ('teacher__name', 'subject__name', 'student__name')

    def get_students(self, obj):
        return ", ".join([str(student) for student in obj.student.all()])
    get_students.short_description = 'Students'

from django.contrib import admin
from .models import Attendance
from students.models import Student

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'month', 'teacher', 'subject', 'semester', 'department')
    list_filter = ('department', 'semester', 'month')
    search_fields = ('teacher__name', 'subject__name')  # Removed student__name, as it's not directly accessible

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Filters `student_presents` and `student_absents` fields based on the selected `department` and `semester`.
        """
        if db_field.name in ['student_presents', 'student_absents']:
            obj_id = request.resolver_match.kwargs.get('object_id')  # Get the current object ID from the URL
            if obj_id:
                attendance = Attendance.objects.get(id=obj_id)
                if attendance.department and attendance.semester:
                    kwargs['queryset'] = Student.objects.filter(
                        department=attendance.department,
                        semester=attendance.semester
                    )
                else:
                    kwargs['queryset'] = Student.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_students_present(self, obj):
        """
        Returns a comma-separated list of students marked present.
        """
        return ", ".join([str(student) for student in obj.student_presents.all()])
    get_students_present.short_description = 'Present Students'

    def get_students_absent(self, obj):
        """
        Returns a comma-separated list of students marked absent.
        """
        return ", ".join([str(student) for student in obj.student_absents.all()])
    get_students_absent.short_description = 'Absent Students'

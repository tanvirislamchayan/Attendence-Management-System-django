from django.contrib import admin
from .models import Student  # Import your Student model


class StudentAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ( 'roll', 'name', 'department', 'semester', 'session')

    # Filters for department, probidhan, and session
    list_filter = ('department', 'probidhan', 'session')

    # Search functionality for roll, department, and name
    search_fields = ('roll', 'name', 'department__name')

    # Pagination for the admin list view
    list_per_page = 20

    # Optional: Organize fields in the form view
    fieldsets = (
        (None, {
            'fields': ('name', 'roll', 'department', 'probidhan', 'session')
        }),
    )

# Register the Student model with the customized admin class
admin.site.register(Student, StudentAdmin)

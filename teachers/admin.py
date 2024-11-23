from django.contrib import admin
from .models import Teacher, Designation

# Register the Designation model
admin.site.register(Designation)

class TeacherAdmin(admin.ModelAdmin):
    # Add fields to display in the list view
    list_display = ('user__first_name', 'designation', 'department', 'is_author', 'is_teacher', 'mobile_number')

    # Add filters for various fields
    list_filter = ('designation', 'department', 'is_active', 'is_teacher', 'is_author')

    # Add search functionality for email and name
    search_fields = ('user__email', 'user__first_name', 'user__last_name')

    # Optionally, you can make certain fields editable in the list view
    # list_editable = ('is_active', 'is_teacher', 'is_author')

    # Optional: Add pagination for large datasets
    list_per_page = 20  # Adjust based on your preference

    # Add a custom form or fieldsets if you want more control over the fields shown in the form
    fieldsets = (
        (None, {
            'fields': ('user', 'mobile_number', 'designation', 'department', 'is_active', 'is_teacher', 'is_author', 'details', 'image')
        }),
    )

# Register the Teacher model with the updated admin class
admin.site.register(Teacher, TeacherAdmin)

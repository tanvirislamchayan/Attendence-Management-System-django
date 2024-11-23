from django.contrib import admin
from .models import Subject

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'semester', 'department', 'credit') 
    list_filter = ('semester', 'department', 'probidhan')  
    search_fields = ('name', 'code') 
    ordering = ('semester', 'department', 'name')  

admin.site.register(Subject, SubjectAdmin)

from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list = ('title', 'description', 'visible')

# Register projects
admin.site.register(Project, ProjectAdmin)

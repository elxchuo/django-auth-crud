from django.contrib import admin
from .models import Task


# Ver elementos desde interaz de admin.

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created")

# Register your models here.

admin.site.register(Task)
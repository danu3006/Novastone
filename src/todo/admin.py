from django.contrib import admin

from . import models

admin.site.site_header = 'TODO Administration'


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'name', 'description', 'status', 'user', 'done_by',)
    list_filter = ('user', 'done_by', 'status',)
    search_fields = ('description', 'name',)


admin.site.register(models.Task, TaskAdmin)

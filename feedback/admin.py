
from django.contrib import admin
from .models import College,Course

class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name', 'place',]
class CourseAdmin(admin.ModelAdmin):
    list_display = ['college_n', 'name',]


admin.site.register(College, CollegeAdmin)
admin.site.register(Course, CourseAdmin)

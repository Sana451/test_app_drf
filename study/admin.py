from django.contrib import admin

from study.models import Lesson, LessonView


class StudyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Lesson, StudyAdmin)
admin.site.register(LessonView, StudyAdmin)

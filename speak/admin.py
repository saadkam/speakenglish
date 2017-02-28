from django.contrib import admin

# Register your models here.
from speak.models import MCQ, Question, Testing, UserInfo, Sitting, Audio, Lesson, Payments

admin.site.register(Payments)
admin.site.register(Audio)
admin.site.register(MCQ)
admin.site.register(Question)
admin.site.register(Testing)
admin.site.register(Sitting)
admin.site.register(UserInfo)
admin.site.register(Lesson)

#@admin.register(MCQ, Question, Testing, Sitting, UserInfo, Audio, Lesson)
#class AuthorAdmin(admin.ModelAdmin):
#    pass


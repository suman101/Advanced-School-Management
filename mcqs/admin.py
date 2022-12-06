from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Quiz)
admin.site.register(Questions)
admin.site.register(AnswerSheet)
admin.site.register(AttemptedQuiz)
admin.site.register(ShortQuestion)
admin.site.register(ShortAnswerSheet)
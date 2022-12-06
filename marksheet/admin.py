from django.contrib import admin
from .models import Exam, Marksheet, Marks
# Register your models here.
admin.site.register(Exam)
# admin.site.register(Marksheet)
# admin.site.register(Marks)

@admin.register(Marksheet)
class MarksheetAdmin(admin.ModelAdmin):
    list_display = ['id','exam','grade','file','created_at','updated_at']
    class Meta:
        model = Marksheet


@admin.register(Marks)
class MarksheetAdmin(admin.ModelAdmin):
    list_display = ['marksheet','sub','student','obtain_mark','full_mark']
    class Meta:
        model = Marksheet
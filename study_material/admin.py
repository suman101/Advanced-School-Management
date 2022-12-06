from django.contrib import admin
from .models import StudyMaterial
# Register your models here.


@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):

    list_display = ['title','school','publish','approved','slug']
    class Meta:
        model = StudyMaterial
from django.contrib import admin

from authentication.models import SchoolProfile,User
from .models import ResearchDetail,Category,Subjects
# Register your models here.

# admin.site.register(ResearchDetail)
admin.site.register(Category)
admin.site.register(Subjects)


@admin.register(ResearchDetail)
class ResearchAdmin(admin.ModelAdmin):

    list_display = ['title','category','school','publish','approved','slug']
    class Meta:
        model = ResearchDetail

from django.contrib import admin
from .models import (
                    HomePageNagarAdmin,
                    #HomePageSchoolAdmin,
                    PrivacyPolicy,
                    TermsAndCondition,
                    SMTPSetting,
                    MailTemplate,
                    CMS,
                    ContactUsForm,
                    AboutUs,
                    Faq,
)

# Register your models here.


admin.site.register(PrivacyPolicy)
admin.site.register(TermsAndCondition)
admin.site.register(CMS)
admin.site.register(AboutUs)
admin.site.register(ContactUsForm)
admin.site.register(HomePageNagarAdmin)

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ['id','title','description']
    
    class Meta:
        model = Faq


@admin.register(SMTPSetting)
class SMTPSettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'email_port', 'email_host_user', 'email_host_password']
    list_editable = ['email_port', 'email_host_user', 'email_host_password']

    class Meta:
        model = SMTPSetting

    def has_add_permission(self, request):
        if SMTPSetting.objects.exists():
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.site_header = "School Management System"
admin.site.site_title = "School Management System  Admin Portal"
admin.site.index_title = "Welcome to School Management System"


class MailTemplateModel(admin.ModelAdmin):
    class Meta:
        model = MailTemplate

    def has_add_permission(self, request):
        if MailTemplate.objects.exists():
            return False
        else:
            return True

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(MailTemplate, MailTemplateModel)
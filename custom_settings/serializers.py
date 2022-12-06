from authentication.models import HomePageSchoolAdmin
from rest_framework import serializers
from .models import AboutUs , CMS, ContactUsForm, Faq, HomePageNagarAdmin, PrivacyPolicy, SMTPSetting, TermsAndCondition  
from django.contrib.contenttypes.models import ContentType


class PrivacySerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['id','content']
        

class TermSerializers(serializers.ModelSerializer):
    class Meta:
        model = TermsAndCondition
        fields = ['id','content']


class CMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMS
        fields = '__all__'


class CMSListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMS
        fields = ('title','slug','image','description' )


class CMSUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMS
        fields = ('title','slug','image','description','image','m_title', 'm_keyword', 'm_description')


class AboutUsSerializers(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['id','title', 'description']


class ContactUsFormSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactUsForm
        fields = ['id','f_name', 'phone_code','phone','email','country','message','created']


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = ['id','title','description']


class SmtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPSetting
        fields = ['id','email_host_user','email_host_password','email_port']


class HomePageNagarAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = HomePageNagarAdmin
        fields = ['id','title', 'image', 'description']


class HomePageSchoolAdminSerializers(serializers.ModelSerializer):
    class Meta:
        model = HomePageSchoolAdmin
        fields = ['id','title', 'school','image', 'description']

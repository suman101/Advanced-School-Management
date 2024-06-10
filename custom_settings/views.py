from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.db.models import query
from django.contrib.auth import get_user_model
from authentication.models import HomePageSchoolAdmin
from custom_settings.paginations import MyPageNumberPagination
User =get_user_model
from rest_framework import generics,status
from rest_framework.response import Response
from .models import (CMS, AboutUs, ContactUsForm, Faq, HomePageNagarAdmin, PrivacyPolicy, SMTPSetting,TermsAndCondition)#HomePageSchoolAdmin
from .serializers import (AboutUsSerializers, CMSListSerializer, CMSSerializer, CMSUpdateSerializer, ContactUsFormSerializers, FaqSerializer, HomePageNagarAdminSerializers, PrivacySerializers, SmtpSerializer, TermSerializers,HomePageSchoolAdminSerializers)
from .permissions import IsNagarAdmin, IsSchoolAdmin
from django.core.mail import send_mail, send_mass_mail
from rest_framework.filters import SearchFilter
# Create your views here.


class CreateCMSView(generics.CreateAPIView):
    serializer_class = CMSSerializer
    permission_classes = [IsNagarAdmin,]


class ListCMSView(generics.ListAPIView):
    serializer_class = CMSListSerializer
    queryset = CMS.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ['title']


class DetailCMSView(generics.RetrieveAPIView):
    serializer_class = CMSSerializer
    permission_classes = [IsNagarAdmin,]
    queryset = CMS.objects.all()
    lookup_field = 'slug'


class UpdateCMSView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsNagarAdmin,]

    serializer_class = CMSUpdateSerializer
    queryset = CMS.objects.all()
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        print(request.data)
        return self.partial_update(request, *args, **kwargs)



class CreatePrivacyApiView(generics.CreateAPIView):
    """views"""
    serializer_class = PrivacySerializers
    queryset = PrivacyPolicy.objects.all()
    permission_classes = [IsNagarAdmin,]

    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = self.serializer_class(data = data)
        try:
            user = User.objects.get(id=request.user.id)
            if user.user_type == "NA":
                serializer.is_valid(raise_exception = True)
                serializer.save()
                return Response(status = status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error':e},status = status.HTTP_400_BAD_REQUEST)


class ListPrivacyApiView(generics.ListAPIView):
    """views"""
    serializer_class = PrivacySerializers
    queryset = PrivacyPolicy.objects.all()


class UpdatePrivacyApiView(generics.RetrieveUpdateDestroyAPIView):
    """views"""
    serializer_class = PrivacySerializers
    queryset = PrivacyPolicy.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsNagarAdmin,]


class CreateTermApiView(generics.CreateAPIView):
    """views"""
    serializer_class = TermSerializers
    queryset = TermsAndCondition.objects.all()
    permission_classes = [IsNagarAdmin,]

    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = self.serializer_class(data = data)
        try:
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error':e},status = status.HTTP_400_BAD_REQUEST)


class ListTermApiView(generics.ListAPIView):
    """views"""
    serializer_class = TermSerializers
    queryset = TermsAndCondition.objects.all()


class UpdateTermApiView(generics.RetrieveUpdateDestroyAPIView):
    """views"""
    serializer_class = TermSerializers
    queryset = TermsAndCondition.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsNagarAdmin,]


class CreateAboutUsApiView(generics.CreateAPIView):
    serializer_class = AboutUsSerializers
    queryset = AboutUs.objects.all()
    permission_classes = [IsNagarAdmin,]

    def post(self,request,*args,**kwargs):
        data = request.data
        serializer = self.serializer_class(data = data)
        try:
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response(status = status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error':e},status = status.HTTP_400_BAD_REQUEST)


class AboutUsApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AboutUsSerializers
    queryset = AboutUs.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsNagarAdmin,]


class AboutUsListApiView(generics.ListAPIView):
    serializer_class = AboutUsSerializers
    queryset = AboutUs.objects.all()
    #pagination_class = MyPageNumberPagination


class CreateContactUsApiView(generics.CreateAPIView):
    serializer_class = ContactUsFormSerializers
    queryset = ContactUsForm.objects.all()


class ContactListUsApiView(generics.ListAPIView):
    serializer_class = ContactUsFormSerializers
    queryset = ContactUsForm.objects.all()
    permission_classes = [IsNagarAdmin,]
    pagination_class = MyPageNumberPagination


class ContactUsApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContactUsFormSerializers
    queryset = ContactUsForm.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsNagarAdmin,]


class FaqCreateView(generics.ListCreateAPIView):
    serializer_class = FaqSerializer
    queryset = Faq.objects.all()


class FaqDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FaqSerializer
    queryset = Faq.objects.all()
    lookup_field = 'id'
    

class SmtpDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SmtpSerializer
    queryset = SMTPSetting.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsNagarAdmin,]

    
class SmtpView(generics.ListCreateAPIView):
    serializer_class = SmtpSerializer
    queryset = SMTPSetting.objects.all()
    permission_classes = [IsNagarAdmin,]


class HomePageNagarAdminApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HomePageNagarAdminSerializers
    queryset = HomePageNagarAdmin.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsNagarAdmin,]


class HomePageNagarAdminListApiView(generics.ListAPIView):
    serializer_class = HomePageNagarAdminSerializers
    queryset = HomePageNagarAdmin.objects.all()
    #pagination_class = MyPageNumberPagination


class HomePageSchoolAdminCreateView(generics.ListCreateAPIView):
    serializer_class = HomePageSchoolAdminSerializers
    queryset = HomePageSchoolAdmin.objects.all()


class HomePageSchoolAdminApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HomePageSchoolAdminSerializers
    queryset = HomePageSchoolAdmin.objects.all()
    lookup_field = 'pk'
    permission_classes = [IsSchoolAdmin,]


class HomePageSchoolAdminListApiView(generics.ListAPIView):
    serializer_class = HomePageSchoolAdminSerializers
    queryset = HomePageSchoolAdmin.objects.all()
    #pagination_class = MyPageNumberPagination

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        if school_id is not None:
            header_content= HomePageSchoolAdmin.objects.filter(school=school_id).order_by('-id')
            return header_content
        else:
            return None

from django.core.mail.backends.smtp import EmailBackend

class MailSendView(generics.GenericAPIView):
    permission_classes = [IsSchoolAdmin|IsNagarAdmin,]
    '''to send same message to user or multiple user at a same time'''
    def post(self, request):
        mail_data = request.data
        email_body = mail_data['mail_body']
        smtpsetting = SMTPSetting.objects.last()
        backend = EmailBackend(
                            port=smtpsetting.email_port,
                            username=smtpsetting.email_host_user,
                            password=smtpsetting.email_host_password
                            )
        data = {
            'email_subject': mail_data['mail_subject'],
            'email_body': email_body,
            'email_receiver': mail_data['user'],
            #'email_user': SMTPSetting.objects.last().email_host_user
            'email_user':mail_data['by']
        }
        send_mail(subject=data['email_subject'],from_email=data['email_user'],recipient_list=data['email_receiver'],message=data['email_body'] ,fail_silently=False, connection=backend)        
        return Response(data, status=status.HTTP_201_CREATED)


class BulkMailSendView(generics.GenericAPIView):
    permission_classes = [IsNagarAdmin,]
    '''to send multiple email to multiple users in a same time'''
    def post(self, request):
        mail_data = request.data
        print(mail_data)
        mail = []
        for i in mail_data:
            message = []
            messages = i['mail_body']
            message.append(messages)
            subject = i['mail_subject']
            message.append(subject)
            email_user = i['host']
            message.append(email_user)

            receiver_to = i['recipient']
            message.append(receiver_to)
            mail.append(message)
        send_mass_mail(mail, fail_silently=False)       
        return Response(mail, status=status.HTTP_201_CREATED)
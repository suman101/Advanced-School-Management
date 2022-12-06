from django.shortcuts import render
from custom_settings.utils import send_mail_notification
from rest_framework.generics import (GenericAPIView, RetrieveUpdateAPIView,ListAPIView,DestroyAPIView)
from custom_settings.paginations import SchoolPagination
from custom_settings.permissions import IsSchoolAdmin, IsNagarAdmin
from rest_framework.response import Response
from rest_framework import status, serializers
from django.http import QueryDict
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter,OrderingFilter
from .models import Mailboxes
from .serializers import MailImportantSerializer, MailboxSerializer, MailboxListSerializer, MailboxUpdateSerializer, MailboxDetailSerializer, MailSeenSerializer
from authentication.models import SchoolProfile, User
# Create your views here.


class MailboxAddView(GenericAPIView):
    serializer_class = MailboxSerializer
    #permission_classes =(IsSchoolAdmin,IsNagarAdmin)

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            print(user.username)
            if user.user_type=="NA":
                data = {
                    'sender': user.username,                
                    'subject': request.data['subject'], 
                    'send_to':request.data['send_to'],
                    'body':request.data['body'],
                    'file':request.data['file'],
                    'draft':request.data['draft'],
                }
                print(data)
                query_dict = QueryDict('', mutable=True)
                query_dict.update(data)
                serializer = MailboxSerializer(data=query_dict)
                valid = serializer.is_valid(raise_exception=True)
                if valid:
                    serializer.save()
                    if serializer.data['draft']==False:
                        data1 = {
                            'email_subject': serializer.data['subject'],
                            'email_body': serializer.data['body'],
                            'email_receiver': serializer.data['send_to']
                        }
                        send_mail_notification(subject = data1['email_subject'],body = data1['email_body'],receiver = data1['email_receiver'])
                        status_code = status.HTTP_201_CREATED
                        response = {
                            'success': True,
                            'statusCode': status_code,
                            'message': 'Mail sent Successfully',
                            'mail': serializer.data
                        }
                        return Response(response, status=status_code)
                    status_code = status.HTTP_201_CREATED
                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'mail Stored to Draft',
                        'mail': serializer.data
                    }
                    return Response(response, status=status_code)
                else:
                    response = serializer.errors
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(response, status=status_code)
            else:
                user = SchoolProfile.objects.get(user_school=self.request.user.id)
                user_id = user.id
                data = {
                    'sender': user.school_name,         
                    'subject': request.data['subject'], 
                    'send_to':request.data['send_to'],
                    'body':request.data['body'],
                    'file':request.data['file'],   
                    'draft':request.data['draft'],
                }
                print(data)
                query_dict = QueryDict('', mutable=True)
                query_dict.update(data)
                serializer = MailboxSerializer(data=query_dict)
                valid = serializer.is_valid(raise_exception=True)
                if valid:
                    serializer.save()
                    if serializer.data['draft']==False:
                        data1 = {
                            'email_subject': serializer.data['subject'],
                            'email_body': serializer.data['body'],
                            'email_receiver': serializer.data['send_to']
                        }
                        send_mail_notification(subject = data1['email_subject'],body = data1['email_body'],receiver = data1['email_receiver'])
                        status_code = status.HTTP_201_CREATED
                        response = {
                            'success': True,
                            'statusCode': status_code,
                            'message': 'mail sent Successfully',
                            'mail': serializer.data
                        }
                        return Response(response, status=status_code)
                    status_code = status.HTTP_201_CREATED
                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'mail Stored to Draft',
                        'mail': serializer.data
                    }
                    return Response(response, status=status_code)
                else:
                    response = serializer.errors
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(response, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with Authenticated Account")
   

class MailboxListView(ListAPIView):
    permission_classes=(IsSchoolAdmin|IsNagarAdmin,)
    queryset=Mailboxes.objects.all()
    pagination_class = SchoolPagination
    serializer_class=MailboxListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['subject','sender']
    ordering_fields = ['subject','sender',]

    def get_queryset(self):
        user = self.request.user
        print(user.email)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA" or user.user_type=="NA":
            schoool = Mailboxes.objects.filter(send_to=user.email, draft=False,trash=False).order_by("-created_at")
            return schoool
        # elif user.user_type=="NA":
        #     schoool = Mailboxes.objects.filter(send_to=user.email)
        #     return schoool


class SendListView(ListAPIView):
    permission_classes=(IsSchoolAdmin|IsNagarAdmin,)
    queryset=Mailboxes.objects.all()
    pagination_class = SchoolPagination
    serializer_class=MailboxListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['subject','send_to']
    ordering_fields = ['subject','send_to',]

    def get_queryset(self):
        user = self.request.user
        print(user.email)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Mailboxes.objects.filter(sender=user.school,draft=False, trash=False).order_by("-created_at")
            return schoool
        elif user.user_type=="NA":
            schoool = Mailboxes.objects.filter(sender=user.username,draft=False, trash=False).order_by("-created_at")
            return schoool


class MailsCountView(ListAPIView):
    permission_classes=(IsSchoolAdmin|IsNagarAdmin,)
    queryset=Mailboxes.objects.all()
    pagination_class = SchoolPagination
    serializer_class=MailboxListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['subject','sender']
    ordering_fields = ['subject','sender']

    def get(self,request,*args,**kwargs):
        data = {}
        user = self.request.user
        print(user.email)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA" or user.user_type=="NA":
            data['unseen_mail_count'] = Mailboxes.objects.filter(send_to=user.email, draft=False,is_seen=False,trash=False).count()
            data['important_mail_count'] = Mailboxes.objects.filter(send_to=user.email, draft=False,important=True, trash=False).count()
            if user.user_type=="NA":
                data['draft_mail_count_nagar'] = Mailboxes.objects.filter(sender=user.username, draft=True, trash=False).count()
            elif user.user_type=="SA":
                data['draft_mail_count_school'] = Mailboxes.objects.filter(sender=user.school, draft=True, trash=False).count()

            print(data)
            return Response (data)


class UnseenMailSeenView(GenericAPIView):
    serializer_class = MailSeenSerializer
    permission_class = [IsNagarAdmin|IsSchoolAdmin,]

    def get_object(self, pk):
        try:
            return Mailboxes.objects.get(id=pk)
        except Mailboxes.DoesNotExist:
            raise serializers.ValidationError(
                'Mail doesnot exist'
            )

    def get(self, request, pk):
        mail = self.get_object(pk)
        serializer = self.serializer_class(mail)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        mail = self.get_object(pk)
        serializer = self.serializer_class(mail, data=request.data, partial=True)
        valid = serializer.is_valid()
        if valid:
            if mail.is_seen == True:
                raise serializers.ValidationError(
                'Mail is already seen.'
                )
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'message': "Mail is seen.",
                'mail': serializer.data
            }
            return Response(response, status=status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': False,
                'message': "Please enter valid data."
            }
            return Response(response, status=status_code)


class UnseenMailListView(ListAPIView):
    """
    List of Unseen Mails.
    """
    permission_class = [IsNagarAdmin|IsSchoolAdmin,]
    serializer_class = MailboxListSerializer

    def get_queryset(self):
        user = self.request.user
        print(user.email)
        return Mailboxes.objects.filter(send_to=user.email, draft=False,trash=False).exclude(is_seen=True)


class ImportantMailView(GenericAPIView):
    serializer_class = MailImportantSerializer
    permission_class = [IsNagarAdmin|IsSchoolAdmin,]

    def get_object(self, pk):
        try:
            return Mailboxes.objects.get(id=pk)
        except Mailboxes.DoesNotExist:
            raise serializers.ValidationError(
                'Mail doesnot exist'
            )

    def get(self, request, pk):
        mail = self.get_object(pk)
        serializer = self.serializer_class(mail)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        mail = self.get_object(pk)
        serializer = self.serializer_class(mail, data=request.data, partial=True)
        valid = serializer.is_valid()
        if valid:
            if mail.important == True:
                mail.important=False
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'message': "Mail is removed from your important list.",
                    'mail': serializer.data
                }
                return Response(response, status=status_code)
            serializer.save()
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'message': "Mail is added to your important list.",
                'mail': serializer.data
            }
            return Response(response, status=status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': False,
                'message': "Please enter valid data."
            }
            return Response(response, status=status_code)


class ImportantMailListView(ListAPIView):
    """
    List of Important Mails.
    """
    permission_class = [IsNagarAdmin|IsSchoolAdmin,]
    serializer_class = MailboxListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['subject','sender']
    ordering_fields = ['subject','sender']

    def get_queryset(self):
        user = self.request.user
        return Mailboxes.objects.filter(send_to=user.email,draft=False, is_seen=True, trash=False).exclude(important=False).order_by("-created_at")


class TrashMailListView(ListAPIView):
    """
    List of Trash Mails.
    """
    permission_class = [IsNagarAdmin|IsSchoolAdmin,]
    serializer_class = MailboxListSerializer

    def get_queryset(self):
        user = self.request.user
        print(user)
        try:
            return Mailboxes.objects.filter(send_to=user.email).exclude(trash=False)
        except:
            if user.user_type=="NA":
                return Mailboxes.objects.filter(sender=user.username).exclude(trash=False)
            elif user.user_type=="SA":
                return Mailboxes.objects.filter(sender=user.school).exclude(trash=False)


class DraftMailListView(ListAPIView):
    """
    List of Draft Mails.
    """
    permission_class = [IsNagarAdmin|IsSchoolAdmin,]
    serializer_class = MailboxListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['subject','sender']
    ordering_fields = ['subject','sender']

    def get_queryset(self):
        user = self.request.user
        print(user.email)
        if user.user_type=="NA":
                return Mailboxes.objects.filter(sender=user.username, trash=False).exclude(draft=False).order_by("-created_at")
        elif user.user_type=="SA":
            return Mailboxes.objects.filter(sender=user.school, trash=False).exclude(draft=False).order_by("-created_at")


class MailboxUpdateView(RetrieveUpdateAPIView):
    permission_class = [IsSchoolAdmin|IsNagarAdmin,]
    queryset = Mailboxes.objects.all()
    serializer_class = MailboxUpdateSerializer
    lookup_field = 'pk'

    def get_object(self, pk):
        try:
            return Mailboxes.objects.get(id=pk)
        except Mailboxes.DoesNotExist:
            raise serializers.ValidationError(
                'Mail doesnot exist'
            )

    def get(self, request, pk):
        mail = self.get_object(pk)
        serializer = self.serializer_class(mail)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        mail = self.get_object(pk)
        serializer = self.serializer_class(mail, data=request.data, partial=True)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            if serializer.data['draft'] == False:
                email_body = serializer.data['body']
                data = {
                    'email_subject': serializer.data['subject'],
                    'email_body': email_body,
                    'email_receiver': serializer.data['send_to']
                }
                send_mail_notification(subject = data['email_subject'],body = data['email_body'],receiver = data['email_receiver'])
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'message': "Mail sent successfully.",
                    'mail': serializer.data
                }
                return Response(response, status=status_code)
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'message': "Mail stored to draft.",
                'mail': serializer.data
            }
            return Response(response, status=status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': False,
                'message': "Please enter valid data."
            }
            return Response(response, status=status_code)

class MailboxDeleteView(DestroyAPIView):
    queryset = Mailboxes.objects.all()
    serializer_class = MailboxListSerializer
    permission_class = [IsSchoolAdmin|IsNagarAdmin,]
    lookup_field = 'pk'
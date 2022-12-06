from django.shortcuts import render
from custom_settings.paginations import SchoolPagination
from custom_settings.permissions import IsSchoolAdmin, IsStudent, IsTeacher
from .serializers import NoteCreateSerializer,NoteListSerializer, NoteUpdateSerializer,NoteDetailSerializer
from .models import Notes
from authentication.models import StudentProfile, TeacherProfile
from rest_framework.generics import (GenericAPIView, RetrieveUpdateAPIView,
            ListAPIView,RetrieveAPIView,DestroyAPIView)
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.

class NoteCreateView(GenericAPIView):
    permission_classes = [IsTeacher,]
    serializer_class = NoteCreateSerializer

    def post(self, request):
        try:
            user = TeacherProfile.objects.get(user=self.request.user.id)
            print(user.id)
            user_id=user.id
            data = {
                'teacher': user_id,
                'title': request.data['title'],
                'grade': request.data['grade'],                 
                'sub': request.data['sub'],             
                'notes_pdf': request.data.get('notes_pdf'),                             

            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            serializer = NoteCreateSerializer(data=query_dict)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Note created successfully',
                    'user': serializer.data
                }
        
                return Response(response, status=status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(serializer.errors, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with Teacher Account")



class TeacherNoteListView(ListAPIView):
    permission_classes=(IsSchoolAdmin|IsTeacher,)
    queryset=Notes.objects.all()
    serializer_class=NoteListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['grade__grade_name','sub__subject','title',]
    ordering_fields = ['grade__grade_name','sub__subject','title',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Notes.objects.filter(teacher__user__school=user.school.id)
            return schoool
        elif user.user_type=="TE":
            teacher = TeacherProfile.objects.get(user=self.request.user)
            teach = Notes.objects.filter(teacher=teacher.id)
            return teach


class NoteCardListView(ListAPIView):
    permission_classes=(IsTeacher|IsStudent,)
    queryset=Notes.objects.all()
    serializer_class=NoteListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['grade__grade_name','sub__subject','title',]
    ordering_fields = ['grade__grade_name','-sub__subject','title',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif user.user_type=="TE":
            teacher = TeacherProfile.objects.get(user=self.request.user)
            teach = Notes.objects.filter(teacher=teacher.id).order_by('-created_at')
            return teach
        elif user.user_type=="ST":
            student = StudentProfile.objects.get(user=self.request.user)
            schoool = Notes.objects.filter(teacher__user__school=user.school,grade__grade_name=student.grade).order_by('-created_at')#,grade=user.grade[0]
            print(schoool)
            return schoool


class StudentNoteListView(ListAPIView):
    permission_classes=(IsStudent,)
    queryset=Notes.objects.all()
    serializer_class=NoteListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['sub__subject','title',]
    ordering_fields = ['sub__subject','title',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        student = StudentProfile.objects.get(user=self.request.user)
        schoool = Notes.objects.filter(teacher__user__school=user.school,grade__grade_name=student.grade)
        return schoool

class StudentNoteDetailView(RetrieveAPIView):
    permission_classes=(IsStudent,)
    queryset=Notes.objects.all()
    serializer_class=NoteDetailSerializer

    def get(self, request,*args,**kwargs):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        student = StudentProfile.objects.get(user=self.request.user)
        schoool = Notes.objects.filter(id=kwargs['pk'],teacher__user__school=user.school,grade__grade_name=student.grade)
        serializer =  NoteDetailSerializer(schoool ,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NoteUpdateView(RetrieveUpdateAPIView):
    serializer_class=NoteUpdateSerializer
    permission_classes=(IsTeacher,)
    queryset=Notes.objects.all()
    lookup_field='pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        teacher = TeacherProfile.objects.get(user=self.request.user)
        schoool = Notes.objects.filter(teacher=teacher.id)
        print(schoool)
        return schoool


class NoteDeleteView(DestroyAPIView):
    serializer_class=NoteCreateSerializer
    permission_classes=(IsTeacher,)
    queryset=Notes.objects.all()
    lookup_field='pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        teacher = TeacherProfile.objects.get(user=self.request.user)
        schoool = Notes.objects.filter(teacher=teacher.id)#,grade=user.grade[0]
        print(schoool)
        return schoool
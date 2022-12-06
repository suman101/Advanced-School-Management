from django.shortcuts import render
from authentication.models import SchoolProfile, StudentProfile, TeacherProfile
from custom_settings.paginations import SchoolPagination
from custom_settings.permissions import IsSchoolAdmin, IsStudent, IsTeacher, IsNagarAdmin
from grade_and_subject.models import ClassRoutine, Grade, Subjects
from grade_and_subject.serializers import ClassRoutineListSerializer, ClassRoutineSerializer, ClassRoutineUpdateSerializer, GradeSerializer, GradeSubjectListSerializer, GradeUpdateSerializer, SubjectDetailSerializer,  SubjectsSerializer,GradeDetailSerializer, GradeListSerializer, SubjectsListSerializer, SubjectsUpdateSerializer
from rest_framework.generics import (GenericAPIView, RetrieveUpdateAPIView,ListAPIView,DestroyAPIView)
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.exceptions import ValidationError, PermissionDenied,NotFound
# Create your views here.




class SubjectAddView(GenericAPIView):
    serializer_class = SubjectsSerializer
    permission_classes =(IsNagarAdmin,)

    def post(self, request):
        try:
            serializer = SubjectsSerializer(data=request.data)
            print(request.user)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Subject added successfully',
                    'user': serializer.data
                }
                return Response(response, status=status_code)
            else:
                response = serializer.errors
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with Nagaradmin Account")



class SubjectUpdateView(RetrieveUpdateAPIView):
    serializer_class=SubjectsUpdateSerializer
    permission_classes=(IsNagarAdmin,)
    queryset=Subjects.objects.all()
    lookup_field='pk'


class SubjectDeleteView(DestroyAPIView):
    serializer_class=SubjectsListSerializer
    permission_classes=(IsNagarAdmin,)
    queryset=Subjects.objects.all()
    lookup_field='pk'

class SubjectListView(ListAPIView):
    permission_classes=(IsNagarAdmin|IsSchoolAdmin|IsTeacher,)
    queryset=Subjects.objects.all()
    pagination_class = SchoolPagination
    serializer_class=SubjectsListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['subject',]
    ordering_fields = ['subject',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="NA" or user.user_type=="SA" or user.user_type=="TE":
            schoool = Subjects.objects.all()
            return schoool
            

class AllSubjectListView(ListAPIView):
    permission_classes=(IsNagarAdmin|IsSchoolAdmin | IsTeacher,)
    queryset=Subjects.objects.all()
    serializer_class=SubjectsListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['subject',]
    ordering_fields = ['subject',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="NA" or user.user_type=="SA" or user.user_type=="TE":
            subs = Subjects.objects.all()
            return subs


class AllSubjectTeacherListView(ListAPIView):
    permission_classes=(IsSchoolAdmin|IsTeacher,)
    queryset=Subjects.objects.all()
    serializer_class=SubjectsListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['subject',]
    ordering_fields = ['subject',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="NA" or user.user_type=="SA" or user.user_type=="TE":
            subs = Subjects.objects.all()
            return subs


class GradeAddView(GenericAPIView):
    serializer_class = GradeSerializer
    permission_class = [IsNagarAdmin,]

    def post(self, request):
        try:
            serializer = GradeSerializer(data=request.data)
            print(request.user)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Grade added successfully',
                    'user': serializer.data
                }
                return Response(response, status=status_code)
            else:
                response = serializer.errors
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with Nagaradmin Account")


class GradeUpdateView(RetrieveUpdateAPIView):
    serializer_class=GradeUpdateSerializer
    permission_classes=(IsNagarAdmin,)
    queryset=Grade.objects.all()
    lookup_field='pk'


class GradeDeleteView(DestroyAPIView):
    serializer_class=GradeListSerializer
    permission_classes=(IsNagarAdmin,)
    queryset=Grade.objects.all()
    lookup_field='pk'


class GradeListView(ListAPIView):
    permission_classes=(IsNagarAdmin|IsSchoolAdmin|IsTeacher,)
    queryset=Grade.objects.all()
    pagination_class = SchoolPagination
    serializer_class=GradeListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['grade_name',]
    ordering_fields = ['grade_name',]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA" or user.user_type=="NA" or user.user_type=="TE":
            schoool = Grade.objects.all()
            return schoool
        # if user.user_type=="TE":
        #     teacher = TeacherProfile.objects.get(user=self.request.user)
        #     teach = Grade.objects.filter(school=teacher.user.school.id)
            #a =teach.union(Grade.objects.filter(subject__subject_teacher=teacher.id))
        
            return teach


class AllGradeListView(ListAPIView):
    permission_classes=(IsNagarAdmin|IsSchoolAdmin|IsTeacher,)
    queryset=Grade.objects.all()
    serializer_class=GradeListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['grade_name',]
    ordering_fields = ['grade_name',]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA" or user.user_type=="NA" or user.user_type=="TE":
            schoool = Grade.objects.all()
            return schoool
        # if user.user_type=="TE":
        #     teacher = TeacherProfile.objects.get(user=self.request.user)
        #     teach = Grade.objects.filter(school=teacher.user.school)
        #     #a =teach.union(Grade.objects.filter(subject__subject_teacher=teacher.id))
        #     return teach


class StudentGradeListView(ListAPIView):
    permission_classes=(IsStudent,)
    queryset=Grade.objects.all()
    serializer_class=GradeListSerializer

    def get(self, request):
        user = self.request.user
        student = StudentProfile.objects.get(user=self.request.user)
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        schoool = Grade.objects.filter(grade_name=student.grade)
        print(schoool)
        serializer =  GradeListSerializer(schoool ,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubjectbyGradeListView(ListAPIView):
    permission_classes=(IsNagarAdmin|IsSchoolAdmin | IsTeacher,)
    queryset=Grade.objects.all()
    serializer_class=GradeSubjectListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['subject__subject',]
    ordering_fields = ['subject__subject',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        args = self.request.query_params.get('grade')
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="NA" or user.user_type=="SA" or user.user_type=="TE":
            schoool = Grade.objects.filter(grade_name=args)
            return schoool


class ClassRoutineAddView(GenericAPIView):
    serializer_class = ClassRoutineSerializer
    permission_classes =(IsSchoolAdmin,)

    def post(self, request):
        try:
            user = SchoolProfile.objects.get(id=self.request.user.school.id)
            print(user.id)
            user_id=user.id
            data = {
                'school': user_id,                 
                'sub': request.data['sub'],
                'teacher':request.data['teacher'],
                'grade':request.data['grade'],
                'time':request.data['time']

            }
            print(data)
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            serializer = ClassRoutineSerializer(data=query_dict)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Class Routine added successfully',
                    'user': serializer.data
                }
                return Response(response, status=status_code)
            else:
                response = serializer.errors
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with School Account")


class ClassRoutineUpdateView(RetrieveUpdateAPIView):
    serializer_class=ClassRoutineUpdateSerializer
    permission_classes=(IsSchoolAdmin,)
    queryset=ClassRoutine.objects.all()
    lookup_field='pk'


class ClassRoutineDeleteView(DestroyAPIView):
    serializer_class=ClassRoutineListSerializer
    permission_classes=(IsSchoolAdmin,)
    queryset=ClassRoutine.objects.all()
    lookup_field='pk'


class ClassRoutineListView(ListAPIView):
    permission_classes=(IsSchoolAdmin|IsTeacher|IsStudent,)
    queryset=ClassRoutine.objects.all()
    pagination_class = SchoolPagination
    serializer_class=ClassRoutineListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['grade__grade_name','sub__subject',]
    ordering_fields = ['grade__grade_name','sub__subject',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA" or user.user_type=="TE":
            schoool = ClassRoutine.objects.filter(school=user.school.id)
            return schoool
        if user.user_type=="ST":
            student = StudentProfile.objects.get(user=self.request.user)
            schoool = ClassRoutine.objects.filter(school=user.school,grade__grade_name=student.grade)#,grade=user.grade[0]
            print(schoool)
            return schoool


class ClassRoutinebyGradeListView(ListAPIView):
    permission_classes=(IsSchoolAdmin | IsTeacher,)
    queryset=ClassRoutine.objects.all()
    serializer_class=ClassRoutineListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['grade__grade_name','sub__subject',]
    ordering_fields = ['grade__grade_name','sub__subject',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        args = self.request.query_params.get('grade')
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA" or user.user_type=="TE":
            schoool = ClassRoutine.objects.filter(grade=args,school=user.school.id)
            return schoool
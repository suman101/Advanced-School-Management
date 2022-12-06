from django.forms import ValidationError
from django.shortcuts import render
from custom_settings.paginations import SchoolPagination
from custom_settings.permissions import IsOwner, IsSchoolAdmin, IsStudent, IsTeacher
from grade_and_subject.models import Subjects, Grade
from .serializers import (ExamCreateSerializer, ExamDetailSerializer, ExamListSerializer, ExamUpdateSerializer, FileUploadSerializer, MarkCreateSerializer, MarkDetailSerializer, MarkGradeListSerializer, MarkListSerializer, MarkUpdateSerializer, MarksheetCreateSerializer, MarksheetDetails, MarksheetDetailSerializer, 
                                        MarksheetListSerializer, MarksheetUpdateSerializer, OnlyMarkSerializer)
from .models import Exam, Marks, Marksheet
from authentication.models import SchoolProfile, StudentProfile, TeacherProfile
from rest_framework.generics import (GenericAPIView, RetrieveUpdateAPIView,
                                            ListAPIView,RetrieveAPIView,DestroyAPIView)
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter, OrderingFilter
import io, csv, pandas as pd
from rest_framework.exceptions import APIException
import datetime
today = datetime.datetime.now()
#created_at__year=today.year
from django.conf import settings
a = settings.BACKEND_API
# Create your views here.


class ExamCreateView(GenericAPIView):
    permission_classes = [IsSchoolAdmin,]
    serializer_class = ExamCreateSerializer

    def post(self, request):
        try:
            user = SchoolProfile.objects.get(id=self.request.user.school.id)
            print(user.id)
            user_id=user.id
            data = {
                'school': user_id,
                'title': request.data['title'],
                'routine': request.data['routine'],                 
                'start_date': request.data['start_date'],                           

            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            serializer = ExamCreateSerializer(data=query_dict)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Exam created successfully',
                    'user': serializer.data
                }
        
                return Response(response, status=status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(serializer.errors, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with School Account")



class ExamListView(ListAPIView):
    permission_classes=(IsSchoolAdmin|IsTeacher|IsStudent,)
    queryset=Exam.objects.all()
    serializer_class=ExamListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Exam.objects.filter(school=user.school.id)
            print(schoool)
            return schoool
        if user.user_type=="TE":
            teach = Exam.objects.filter(school=user.school)
            return teach
        if user.user_type=="ST":
            schoool = Exam.objects.filter(school=user.school)
            print(schoool)
            return schoool


class AllExamListView(ListAPIView):
    permission_classes=(IsSchoolAdmin|IsTeacher,)
    queryset=Exam.objects.all()
    serializer_class=ExamListSerializer
    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        schoool = Exam.objects.filter(school=user.school)
        print(schoool)
        return schoool


class ExamDetailView(RetrieveAPIView):
    permission_classes=(IsTeacher|IsSchoolAdmin|IsStudent,)
    queryset=Exam.objects.all()
    serializer_class=ExamDetailSerializer
    # lookup_field='pk'

    def get(self, request,*args,**kwargs):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Exam.objects.filter(id=kwargs['pk'],school=user.school.id)
            serializer =  ExamDetailSerializer(schoool ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user.user_type == "TE":
            schoool = Exam.objects.filter(id=kwargs['pk'],school=user.school)
            serializer =  ExamDetailSerializer(schoool ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user.user_type == "ST":
            schoool = Exam.objects.filter(id=kwargs['pk'],school=user.school)
            serializer =  ExamDetailSerializer(schoool ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ExamUpdateView(RetrieveUpdateAPIView):
    serializer_class=ExamUpdateSerializer
    permission_classes=(IsSchoolAdmin,)
    queryset=Exam.objects.all()
    lookup_field='pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Exam.objects.filter(school=user.school.id)
            print(schoool)
            return schoool


class ExamDeleteView(DestroyAPIView):
    serializer_class=ExamCreateSerializer
    permission_classes=(IsSchoolAdmin,)
    queryset=Exam.objects.all()
    lookup_field='pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Exam.objects.filter(school=user.school.id)
            print(schoool)
            return schoool



class MarksheetCreateView(GenericAPIView):
    permission_classes = [IsSchoolAdmin,]
    serializer_class = MarksheetCreateSerializer

    def generate(self, data):
        marks = data['file']
        reader = pd.read_csv(a + marks)
        gr = Grade.objects.get(school = self.request.user.school,id = data['grade'])
        for row, col in reader.iterrows():
            try:
                sub = col['Subject'].split('(')[0]
                fm = col['Subject'].split('(')[1].strip(')')#.split(',')[0]
                #pm = col['Subject'].split('(')[1].split(',')[1].strip(')')
            except Exception as e:
                print(e)
                raise ValidationError(f"The format of subject is not correct. Please makesure subject is in following form: Subject Name(full_gpa). eg. Science TH(4)")
            for i in StudentProfile.objects.filter(user__school=self.request.user.school,grade = gr.grade_name):
                try:
                    std = StudentProfile.objects.get(user__username = i.user.username)
                except:
                    raise ValidationError(f"Student in column {row}-{col} does not exist")
                try:
                    data1 = {}
                    data1["student"] = std.user.username
                    data1['sub']= sub
                    data1['obtain_mark'] = col[i.user.username]
                    data1['full_mark'] = float(fm)
                    #data1['pass_mark'] = float(pm)
                    data1['marksheet'] = int(data['id'])
                except Exception as e:
                    print(e)
                    raise APIException("Can't generate Marksheet!")

                ser = MarkCreateSerializer(data = data1)
                ser.is_valid(raise_exception=True)
                ser.save()
        return

    def post(self, request,*args,**kwargs):
        try:
            # if (Grade.objects.get(id = request.data['grade']).school and Exam.objects.get(id = request.data['exam']).school and Marksheet.object.get(created_at__year=today.year)).exists():
            #     status_code = status.HTTP_400_BAD_REQUEST
            #     response = {
            #         'message': 'Marksheet already Created.',
            #         }
            #     return Response(response, status=status_code)  
            serializer = MarksheetCreateSerializer(data=request.data)
            valid = serializer.is_valid()
            print(request.data['grade'])
            print(request.data['exam'])
            if valid:
                print(Grade.objects.get(id = request.data['grade']).school)
                print(request.user.school)
                
                if Grade.objects.get(id = request.data['grade']).school != request.user.school:
                    status_code = status.HTTP_400_BAD_REQUEST
                    response = {
                    'message': 'invalid grade id',
                    }
                    return Response(response, status=status_code)
                serializer.save()

                try:
                    mark = self.generate(serializer.data)
                    status_code = status.HTTP_201_CREATED
                    response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Marksheet created successfully',
                    'user': serializer.data
                    }
                    return Response(response, status=status_code)
                except Exception as e:
                    print("exception")
                    print(e)
                    status_code = status.HTTP_400_BAD_REQUEST
                    response = {
                    'message': str(e),
                    }
                    return Response(response, status=status_code)

                
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(serializer.errors, status=status_code)
        except Exception as e:
            print(e)
            return Response({
                    'message': 'Marks not created successfully',
                }, status=status.HTTP_400_BAD_REQUEST)


class MarksheetListView(ListAPIView):
    permission_classes=(IsSchoolAdmin,)
    queryset=Marksheet.objects.all()
    serializer_class=MarksheetListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['grade__grade_name','exam__title',]
    ordering_fields = ['grade__grade_name','exam__title',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Marksheet.objects.filter(exam__school=user.school.id)
            print(schoool)
            return schoool
        if user.user_type=="TE":
            schoool = Marksheet.objects.filter(exam__school=user.school.id)
            return schoool


class StudentMarksheetListView(ListAPIView):
    permission_classes=(IsStudent,)
    queryset=Marksheet.objects.all()
    serializer_class=MarksheetListSerializer
    pagination_class = SchoolPagination

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        student = StudentProfile.objects.get(user=self.request.user)
        schoool = Marksheet.objects.filter(exam__school=user.school,grade__grade_name=student.grade)
        print(schoool)
        return schoool


class MarksheetDetailView(RetrieveAPIView):
    permission_classes=(IsSchoolAdmin|IsTeacher|IsStudent,)
    queryset=Marksheet.objects.all()
    serializer_class=MarksheetDetailSerializer
    # lookup_field='pk'

    def get(self, request,*args,**kwargs):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Marksheet.objects.filter(id=kwargs['pk'],exam__school=user.school)
            print(schoool)
            serializer =  MarksheetDetailSerializer(schoool ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.user_type=="TE":
            schoool = Marksheet.objects.filter(id=kwargs['pk'],exam__school=user.school)
            print(schoool)
            serializer =  MarksheetDetailSerializer(schoool ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user.user_type == "ST":
            student = StudentProfile.objects.get(user=self.request.user)
            schoool = Marksheet.objects.filter(id=kwargs['pk'],exam__school=user.school,grade__grade_name=student.grade)
            print(schoool)
            serializer =  MarksheetDetailSerializer(schoool ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class MarksheetUpdateView(RetrieveUpdateAPIView):
    serializer_class=MarksheetUpdateSerializer
    permission_classes=(IsSchoolAdmin,)
    queryset=Marksheet.objects.all()
    lookup_field='pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Marksheet.objects.filter(exam__school=user.school.id)
            print(schoool)
            return schoool


class MarksheetDeleteView(DestroyAPIView):
    serializer_class=MarksheetCreateSerializer
    permission_classes=(IsSchoolAdmin,)
    queryset=Marksheet.objects.all()
    lookup_field='pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Marksheet.objects.filter(exam__school=user.school.id)
            print(schoool)
            return schoool


class MarksheetByGrade(ListAPIView):
    serializer_class=MarksheetDetails
    permission_classes=(IsSchoolAdmin|IsTeacher,)
    queryset=Marksheet.objects.all()
    #lookup_field='pk'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        exam = self.request.query_params.get('exam')
        grade = self.request.query_params.get('grade')
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA" or  user.user_type=="TE":
            schoool = Marksheet.objects.filter(grade=grade,exam=exam,exam__school=user.school)
            serializer =  MarksheetDetails(schoool ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class MarkListView(ListAPIView):
    permission_classes=(IsSchoolAdmin|IsTeacher,)
    queryset=Marks.objects.all()
    serializer_class=OnlyMarkSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['marksheet','student',]
    ordering_fields = ['marksheet','student',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Marks.objects.filter(marksheet__exam__school=user.school)
            print(schoool)
            return schoool
        if user.user_type=="TE":
            teach = Marks.objects.filter(marksheet__exam__school=user.school)
            return teach
            

class StudentMarkListView(ListAPIView):
    permission_classes=(IsStudent,)
    queryset=Marks.objects.all()
    serializer_class=MarkListSerializer
    pagination_class = SchoolPagination

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        student = StudentProfile.objects.get(user=self.request.user)
        schoool = Marks.objects.filter(marksheet__exam__school=student.school, student__id=student.user.id)
        print(schoool)
        return schoool


class MarkDetailView(RetrieveUpdateAPIView):
    permission_classes=(IsTeacher|IsSchoolAdmin,)
    queryset=Marks.objects.all()
    serializer_class=MarkDetailSerializer
    lookup_field='pk'

    def get(self, request,*args,**kwargs):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA" or user.user_type == "TE":
            schoool = Marks.objects.filter(id=kwargs['pk'],marksheet__exam__school=user.school)
            print(schoool)
            serializer =  MarkDetailSerializer(schoool ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


# Full marksheet by student id and exam id
from django.db.models import Count, Sum
class StdMarksView(GenericAPIView):
    serializer_class=OnlyMarkSerializer
    permission_classes=(IsSchoolAdmin|IsTeacher|IsStudent,)
    queryset=Marks.objects.all()
    
    def get_total_full_mark(self,obj):
        try:
            a = Marks.objects.filter(student=obj.student, marksheet__exam=obj.marksheet.exam).aggregate(Sum('full_mark'))['full_mark__sum']
            return a
        except Exception as e:
            return None

    def get_total_obtain_mark(self,obj):
        try:
            a = Marks.objects.filter(student=obj.student, marksheet__exam=obj.marksheet.exam).aggregate(Sum('obtain_mark'))['obtain_mark__sum']
            return a
        except Exception as e:
            return None

    def get_total_percentage(self,obj):
        try:
            om = self.get_total_obtain_mark(obj) if self.get_total_obtain_mark(obj) else 0
            fm = self.get_total_full_mark(obj) if self.get_total_full_mark(obj) else 0
            percentage = (om/fm)*4
            return percentage
        except:
            return None

    def get_pass_or_fail(self,obj):
        try:
            a = Marks.objects.filter(student=obj.student, marksheet__exam=obj.marksheet.exam)
            for i in a:
                if i.obtain_mark == 0 or i.obtain_mark ==0.0:
                    ab = "F"
            return ab
        except:
            return None

    def get_number_of_fail(self,obj):
        try: 
            a = Marks.objects.filter(student=obj.student, marksheet__exam=obj.marksheet.exam)
            b = 0
            for i in a:
                if i.obtain_mark == 0:
                    b = b+1
            return b
        except:
            return None

    def get(self, request, *args, **kwargs):
        user = self.request.user
        args = self.request.query_params.get('marksheet_id')

        try:
            student = StudentProfile.objects.get(id=kwargs['pk']).user.username
            roll = StudentProfile.objects.get(id=kwargs['pk']).roll_number
            dob = StudentProfile.objects.get(id=kwargs['pk']).user.dob
        except:
            return Response({'error':'invalid student profile'}, status=status.HTTP_400_BAD_REQUEST)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            if user.user_type=="SA" or user.user_type=="TE":
                school = Marks.objects.filter(student=student,marksheet=args,marksheet__exam__school=user.school)
                #print(school)
                serializer =  OnlyMarkSerializer(school,many=True)
                #print(serializer)
            elif user.user_type=="ST":
                std = StudentProfile.objects.get(user=self.request.user)
                print(std)
                if std.id != kwargs['pk']:
                    return Response({'error':'Invalid user'},status = status.HTTP_400_BAD_REQUEST)
                schoool = Marks.objects.filter(student=student,marksheet=args,marksheet__exam__school=user.school)
                #print(schoool)
                serializer =  OnlyMarkSerializer(schoool ,many=True)
            st = Marks.objects.filter(student=student,marksheet=args,marksheet__exam__school=user.school).first()
            result = {
                "school_info":user.school.school_name,
                "student_name":student,
                "roll_number":roll,
                "dob":dob,
                "total_full_marks":self.get_total_full_mark(st),
                "total_obtain_mark":self.get_total_obtain_mark(st),
                "total_gpa":self.get_total_percentage(st),
                "pass_or_fail":self.get_pass_or_fail(st),
                "number_of_fail":self.get_number_of_fail(st),
                "marks":serializer.data
            }
            # result.update(serializer.data)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'marksheet not found'}, status=status.HTTP_400_BAD_REQUEST)


class MarkDeleteView(DestroyAPIView):
    serializer_class=MarkCreateSerializer
    permission_classes=(IsSchoolAdmin,)
    queryset=Marksheet.objects.all()
    lookup_field='pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Marks.objects.filter(school=user.school)
            print(schoool)
            return schoool


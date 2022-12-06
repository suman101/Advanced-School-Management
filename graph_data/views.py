from re import sub
from django.shortcuts import render
from authentication.serializers import CasteReligionCountSerializer, SchoolCasteReligionCountSerializer
from custom_settings.permissions import IsNagarAdmin, IsSchoolAdmin
from grade_and_subject.models import Subjects
from marksheet.models import Marks, Marksheet
from marksheet.serializers import MarkForNagarAndSchool
from mcqs.models import Quiz
from notes.models import Notes
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from authentication.models import SchoolProfile, TeacherProfile, StudentProfile
from django.db.models import Count
from django.contrib.auth import get_user_model
User = get_user_model()
from itertools import count, groupby
import datetime
today = datetime.datetime.now()
#created_at__year=today.year
# Create your views here.


class TotalSchoolCountView(generics.ListAPIView):
    permission_class = [IsNagarAdmin,]
    def get(self,request,*args, **kwargs):
        data = {}
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="NA":
            data['school_count'] = SchoolProfile.objects.count()
            data['school_count_male'] = User.objects.filter(gender='Male').count()
            data['school_count_female'] = User.objects.filter(gender='Female').count()
            data['school_count_other'] = User.objects.filter(gender='Other').count()
            data['school_count_primary'] = SchoolProfile.objects.filter(school_type='PR').count()
            data['school_count_lower_secondary'] = SchoolProfile.objects.filter(school_type='LS').count()
            data['school_count_Higher_secondary'] = SchoolProfile.objects.filter(school_type='HS').count()

            return Response(data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class TotalTeacherCountView(generics.ListAPIView):
    permission_class = [IsNagarAdmin,]
    def get(self,request,*args,**kwargs):
        data = {}
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="NA":
            data['teacher_count'] = TeacherProfile.objects.count()
            data['teacher_count_male'] = TeacherProfile.objects.filter(user__gender='Male').count()
            data['teacher_count_female'] = TeacherProfile.objects.filter(user__gender='Female').count()
            data['teacher_count_other'] = TeacherProfile.objects.filter(user__gender='Other').count()

            return Response(data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class TotalStudentCountView(generics.ListAPIView):
    permission_class = [IsNagarAdmin,]
    def get(self,request,*args,**kwargs):
        data = {}
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="NA":
            data['student_count'] = StudentProfile.objects.count()
            data['student_count_male'] = StudentProfile.objects.filter(user__gender='Male').count()
            data['student_count_female'] = StudentProfile.objects.filter(user__gender='Female').count()
            data['student_count_other'] = StudentProfile.objects.filter(user__gender='Other').count()

            return Response(data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        

class TotalQuizCountView(generics.ListAPIView):
    permission_class = [IsNagarAdmin,]
    def get(self,request,*args,**kwargs):
        data = {}
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="NA":
            data['quiz_count'] = Quiz.objects.filter(publish=True).count()
            student = Quiz.objects.filter(publish=True).aggregate(Count('attended_users'))
            data['quiz_attended_student'] = student['attended_users__count']

            grade = Quiz.objects.filter(publish=True).aggregate(Count('grade'))
            data['quiz_attended_by_grade'] = grade['grade__count']

            return Response(data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class TotalCasteCountView(generics.ListAPIView):
    permission_class = [IsNagarAdmin,]
    def get(self,request,*args,**kwargs):
        data = {}
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="NA":
            data['student_count_caste'] = StudentProfile.objects.values('caste','user__school__school_name').annotate(count=Count('caste'))
            data['student_count_class'] = StudentProfile.objects.values('grade','caste').annotate(count=Count('caste'))
            data['teacher_count_caste'] = TeacherProfile.objects.values('caste','user__school__school_name').annotate(count=Count('caste'))

            return Response(data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    

class TotalReligionCountView(generics.ListAPIView):
    permission_class = [IsNagarAdmin,]
    def get(self,request,*args,**kwargs):
        data = {}
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="NA":
            data['student_count_religion'] = StudentProfile.objects.values('religion','user__school__school_name').annotate(count=Count('religion'))

            data['student_count_class'] = StudentProfile.objects.values('grade','religion').annotate(count=Count('religion'))
            data['teacher_count_religion'] = TeacherProfile.objects.values('religion','user__school__school_name').annotate(count=Count('religion'))
            return Response(data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        
class TotalNotesCountView(generics.ListAPIView):
    permission_class = [IsSchoolAdmin,]
    def get(self,request,*args,**kwargs):

        data = {}
        user = self.request.user
        if user.user_type=="SA":
            school = self.request.user.school
            data['total_notes_count'] = Notes.objects.filter(teacher__user__school=school.id ).count()
            return Response(data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class TotalMcqCountView(generics.ListAPIView):
    permission_class = [IsSchoolAdmin,]
    def get(self,request,*args,**kwargs):

        data = {}
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            school = self.request.user.school
            data['total_mcq_count'] = Quiz.objects.filter(teacher__user__school=school.id, publish=True).count()
            student = Quiz.objects.filter(teacher__user__school=school.id, publish=True).aggregate(Count('attended_users'))
            data['quiz_attended_student'] = student['attended_users__count']

            grade = Quiz.objects.filter(teacher__user__school=school.id, publish=True).aggregate(Count('grade'))
            data['quiz_attended_by_grade'] = grade['grade__count']
            return Response(data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class TotalStudentSchoolCountView(generics.ListAPIView):
    permission_class = [IsNagarAdmin|IsSchoolAdmin,]
    def get(self,request,*args,**kwargs):

        data = {}
        user = self.request.user
        try:
            if user.user_type=="SA":
                school = self.request.user.school
                data['total_teacher_school_count'] = TeacherProfile.objects.filter(user__school=school).count()
                data['school_teacher_count_male'] = TeacherProfile.objects.filter(user__school=school,user__gender='Male').count()
                data['school_teacher_count_female'] = TeacherProfile.objects.filter(user__school=school,user__gender='Female').count()
                data['school_teacher_count_other'] = TeacherProfile.objects.filter(user__school=school,user__gender='Other').count()
                data['total_student_school_count'] = StudentProfile.objects.filter(user__school=school).count()
                data['student_count_male'] = StudentProfile.objects.filter(user__school=school,user__gender='Male').count()
                data['student_count_female'] = StudentProfile.objects.filter(user__school=school,user__gender='Female').count()
                data['student_count_other'] = StudentProfile.objects.filter(user__school=school,user__gender='Other').count()
                data['student_count_class'] = StudentProfile.objects.filter(user__school__school_name=school).values('grade').annotate(count=Count('grade')).order_by('grade')
                return Response(data)
            elif user.user_type=="NA":
                schoool = self.request.query_params.get('school_id')
                data['total_teacher_school_count'] = TeacherProfile.objects.filter(user__school=schoool).count()
                data['school_teacher_count_male'] = TeacherProfile.objects.filter(user__school=schoool,user__gender='Male').count()
                data['school_teacher_count_female'] = TeacherProfile.objects.filter(user__school=schoool,user__gender='Female').count()
                data['school_teacher_count_other'] = TeacherProfile.objects.filter(user__school=schoool,user__gender='Other').count()
                data['total_student_school_count'] = StudentProfile.objects.filter(user__school__id=schoool).count()
                data['student_count_male'] = StudentProfile.objects.filter(user__school=schoool,user__gender='Male').count()
                data['student_count_female'] = StudentProfile.objects.filter(user__school=schoool,user__gender='Female').count()
                data['student_count_other'] = StudentProfile.objects.filter(user__school=schoool,user__gender='Other').count()
                data['student_count_class'] = StudentProfile.objects.filter(user__school__id=schoool).values('grade').annotate(count=Count('grade')).order_by('grade')
                return Response(data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            


class MarksNagarAdminView(generics.ListAPIView):
    queryset=Marksheet.objects.all()
    serializer_class=MarkForNagarAndSchool
    permission_classes=(IsSchoolAdmin|IsNagarAdmin,)
    #lookup_field='pk'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            if user.user_type=="SA":
                years = self.request.query_params.get('year')
                main_list = []
                schoool = Marksheet.objects.filter(exam__school=user.school,created_at__year=years).values('exam').distinct()
                for i in schoool:   # loop through every marksheet of that school
                    exam_data = {}
                    grade_list = []
                    y = Marksheet.objects.filter(exam = i['exam'],created_at__year=years).order_by('grade')
                    for k in y:
                        exam_data['exam']=k.exam.title
                        x = Marksheet.objects.get(grade = k.grade,exam = i['exam'],created_at__year=years)
                        grade_data={'grade' :k.grade.grade_name}
                        std = StudentProfile.objects.filter(grade = k.grade.grade_name, user__school=user.school)
                        fail_count = 0
                        for j in std:
                            sub_pass = 0
                            sub_fail = 0
                            for l in Marks.objects.filter(marksheet__exam = k.exam,marksheet__grade = k.grade,student = j.user.username):
                                if l.obtain_mark > 0:
                                    pass
                                else:
                                    sub_fail = 1
                                    continue
                            fail_count = fail_count +  sub_fail 
                        pass_count = std.count()-fail_count    
                        grade_data['pass']=pass_count
                        grade_data['fail_count']=fail_count

                        grade_list.append(grade_data)

                        exam_data['grades'] = grade_list
                    main_list.append(exam_data)
                return Response(main_list, status=status.HTTP_200_OK)
            
            else:
                if user.user_type=="NA":
                    args = self.request.query_params.get('school')
                    years = self.request.query_params.get('year')
                    main_list = []
                    schoool = Marksheet.objects.filter(exam__school=args,created_at__year=years).values('exam').distinct()
                    #print(Marksheet.objects.filter(exam__school=args,created_at__year=years).values('exam').distinct())
                    for i in schoool:   # loop through every marksheet of that school
                        exam_data = {}
                        grade_list = []
                        y = Marksheet.objects.filter(exam = i['exam'],created_at__year=years).order_by('grade')
                        for k in y:
                            exam_data['exam']=k.exam.title
                            x = Marksheet.objects.get(grade = k.grade,exam = i['exam'],created_at__year=years)
                            grade_data={'grade' :k.grade.grade_name}
                            std = StudentProfile.objects.filter(grade = k.grade.grade_name, user__school=args)
                            fail_count = 0
                            for j in std:
                                sub_pass = 0
                                sub_fail = 0
                                for l in Marks.objects.filter(marksheet__exam = k.exam,marksheet__grade = k.grade,student = j.user.username):
                                    if l.obtain_mark > 0:
                                        pass
                                    else:
                                        sub_fail = 1
                                        continue
                                fail_count = fail_count +  sub_fail 
                            pass_count = std.count()-fail_count    
                            grade_data['pass']=pass_count
                            grade_data['fail_count']=fail_count

                            grade_list.append(grade_data)

                            exam_data['grades'] = grade_list
                        main_list.append(exam_data)
                    return Response(main_list, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'marksheet not found'}, status=status.HTTP_400_BAD_REQUEST)


class MarksheetYearListView(generics.ListAPIView):
    queryset=Marksheet.objects.all()
    serializer_class=MarkForNagarAndSchool

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            schoool = Marksheet.objects.values('created_at__year').distinct().order_by('-created_at__year')

            return Response(schoool, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'year not found'}, status=status.HTTP_400_BAD_REQUEST)


class CasteAndReligionView(generics.ListAPIView):
    queryset=SchoolProfile.objects.all()
    serializer_class=CasteReligionCountSerializer
    permission_classes=(IsNagarAdmin,)


class SchoolGradeCasteAndReligionView(generics.ListAPIView):
    queryset=SchoolProfile.objects.all()
    serializer_class=SchoolCasteReligionCountSerializer
    permission_classes=(IsSchoolAdmin,)

    def get_queryset(self):
        user = self.request.user
        print(user.id)
        if user.user_type=="SA":
            schoool = SchoolProfile.objects.filter(school_name=user.school)
            print(schoool)
            return schoool

from pickle import APPEND
from urllib import request
from django.forms import ValidationError
from django.shortcuts import render
from authentication.models import SchoolProfile, StudentProfile, TeacherProfile
from authentication.serializers import StudentProfileViewSerializer
from custom_settings.paginations import QuizPagination, SchoolPagination
from custom_settings.permissions import IsSchoolAdmin, IsStudent, IsTeacher
from notes.serializers import SubjectListSerializer
from researchs.models import Subjects
from .models import AnswerSheet, AttemptedQuiz, Questions, Quiz, ShortAnswerSheet, ShortQuestion
from . serializers import AnswerSheetCreateSerializer, AtQuizCreateSerializer, AttemptedQuizCreateSerializer, QuestionListSerializer, QuestionCreateSerializer, QuizDetailSerializer, QuizListSerializer, QuizCreateSerializer, QuizUpdateSerializer, ResultQuizSerializer, ShortAnswerSheetCreateSerializer, ShortAnswerSheetListSerializer, ShortAnswerSheetUpdateSerializer, ShortQuestionAnswerDetailList, ShortQuestionCreateSerializer, ShortQuestionListSerializer, ShortQuestionUpdateSerializer, StdQuestionListSerializer
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView,ListAPIView, DestroyAPIView, GenericAPIView, RetrieveUpdateAPIView,UpdateAPIView, RetrieveAPIView
from rest_framework import status, serializers
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.http import QueryDict
from django.http import Http404
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy  as _
from rest_framework.filters import SearchFilter,OrderingFilter
# Create your views here.


class QuizCreateView(CreateAPIView):
    serializer_class = QuizCreateSerializer
    permission_classes = [IsTeacher,]

    def post(self, request):
        try:
            user = TeacherProfile.objects.get(user=self.request.user.id)
            print(user.id)
            user_id=user.id
            data = {
                'teacher': user_id,
                'sub':request.data['sub'],
                'grade':request.data['grade'],
                'title': request.data['title'],                 
                'description': request.data['description'],
                "total_question": request.data['total_question'],
                "publish": request.data['publish'],
                "quiz_duration": request.data['quiz_duration'],
            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            print(data)
            serializer = QuizCreateSerializer(data=query_dict)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Quiz created successfully',
                    'user': serializer.data
                }
        
                return Response(response, status=status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(serializer.error, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with Teacher Account")


class QuizListView(ListAPIView):
    """This views is only for school and teacher"""
    permission_classes=(IsSchoolAdmin|IsTeacher,)
    queryset=Quiz.objects.all()
    serializer_class=QuizListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['grade__grade_name','sub__subject','title',]
    ordering_fields = ['grade__grade_name','sub__subject','title',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type == "SA":
            teach = Quiz.objects.filter(teacher__user__school_id=user.school.id)
            return teach
        elif user.user_type=="TE":
            teacher = TeacherProfile.objects.get(user=self.request.user)
            teach = Quiz.objects.filter(teacher=teacher.id)
            return teach
        

class QuizDetailView(RetrieveAPIView):
    permission_classes=(IsSchoolAdmin|IsTeacher,)
    queryset=Quiz.objects.all()
    serializer_class=QuizDetailSerializer
    lookup_field='pk'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type == "SA":
            teach = Quiz.objects.filter(id=kwargs['pk'],teacher__user__school_id=user.school.id)
            serializer =  QuizDetailSerializer(teach ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user.user_type=="TE":
            teacher = TeacherProfile.objects.get(user=self.request.user)
            teach = Quiz.objects.filter(teacher=teacher.id)
            serializer =  QuizDetailSerializer(teach ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class StudentQuizListView(ListAPIView):
    permission_classes=(IsStudent,)
    queryset=Quiz.objects.all()
    serializer_class=QuizListSerializer
    pagination_class = SchoolPagination

    def get_queryset(self):
        user = self.request.user
        student = StudentProfile.objects.get(user=self.request.user)
        print(student.grade)
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        schoool = Quiz.objects.filter(publish=True,teacher__user__school=user.school.id,grade__grade_name=student.grade).exclude(attended_users=student)
        return schoool
        

class StudentQuizDetailView(RetrieveAPIView):
    permission_classes=(IsStudent,)
    queryset=Quiz.objects.all()
    serializer_class=QuizListSerializer
    # lookup_field='pk'

    def get(self, request,*args,**kwargs):
        user = self.request.user
        student = StudentProfile.objects.get(user=self.request.user)
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        schoool = Quiz.objects.filter(publish=True,id=kwargs['pk'],teacher__user__school=user.school,grade__grade_name=student.grade).exclude(publish = False).exclude(attended_users=student)#,grade=user.grade[0]
        print(schoool)
        serializer =  QuizListSerializer(schoool ,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizSearchView(ListAPIView):
    permission_classes = [IsSchoolAdmin|IsTeacher,]
    queryset = Quiz.objects.order_by('-id')
    serializer_class = QuizListSerializer
    filter_backends =  [filters.SearchFilter]
    search_fields = ['title']


class QuizDetailDeleteView(DestroyAPIView):
    permission_classes = [IsTeacher,]
    queryset = Quiz.objects.all()
    serializer_class = QuizListSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        teacher = TeacherProfile.objects.get(user=self.request.user)
        schoool = Quiz.objects.filter(teacher=teacher.id)
        print(schoool)
        return schoool

class QuizDetailEditView(RetrieveUpdateAPIView):
    serializer_class=QuizUpdateSerializer
    permission_classes=[IsTeacher,]
    queryset=Quiz.objects.all()
    lookup_field='pk'
    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        teacher = TeacherProfile.objects.get(user=self.request.user)
        schoool = Quiz.objects.filter(teacher=teacher.id)#,grade=user.grade[0]
        print(schoool)
        return schoool


class ActiveQuizBySubject(ListAPIView):
    permission_classes = [IsTeacher|IsStudent,]
    serializer_class = QuizListSerializer

    def get_queryset(self):
        user = self.request.user
        print(user)
        print("Hi")
        try:
            quiz__sub = self.kwargs.get('id')
            print(quiz__sub)
            if quiz__sub is not None:
                if user.user_type =="TE":
                    teacher = TeacherProfile.objects.get(user=self.request.user)
                    queryset = Quiz.objects.filter(teacher=teacher,sub_id=quiz__sub)
            
                if user.user_type =="ST":
                    student = StudentProfile.objects.get(user=self.request.user)
                    queryset = Quiz.objects.filter(publish = True,sub__id=quiz__sub,teacher__user__school=user.school,grade__grade_name=student.grade).exclude(attended_users=student)
                    print(queryset)
                    return queryset
        except Exception as e:
            print(e)
            raise ValidationError(e)


class QuizResultView(RetrieveAPIView):
    permission_classes = [IsSchoolAdmin|IsTeacher,]
    serializer_class = ResultQuizSerializer
    queryset = Quiz.objects.all()
    pagination_class = SchoolPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['created_at','title']
    lookup_field='pk'


    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type == "SA":
            teach = Quiz.objects.filter(id=kwargs['pk'],teacher__user__school_id=user.school.id)
            serializer =  ResultQuizSerializer(teach ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user.user_type=="TE":
            teacher = TeacherProfile.objects.get(user=self.request.user)
            teach = Quiz.objects.filter(id=kwargs['pk'],teacher=teacher.id)
            serializer =  ResultQuizSerializer(teach ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class QuizTableResultView(ListAPIView):
    permission_classes = [IsSchoolAdmin|IsTeacher|IsStudent,]
    serializer_class = AttemptedQuizCreateSerializer
    queryset = AttemptedQuiz.objects.all().order_by('-created_at')
    filter_backends = [filters.SearchFilter]
    def get(self, request):
        user = self.request.user
        if user.user_type == "SA":
            teach = AttemptedQuiz.objects.filter(quiz__teacher__user__school_id=user.school.id)
            serializer =  AttemptedQuizCreateSerializer(teach ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif user.user_type=="TE":
            teacher = TeacherProfile.objects.get(user=self.request.user)
            teach = AttemptedQuiz.objects.filter(quiz__teacher=teacher.id)
            serializer =  AttemptedQuizCreateSerializer(teach ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.user_type =="ST":
            student = StudentProfile.objects.get(user=self.request.user)
            queryset = AttemptedQuiz.objects.filter(quiz__teacher__user__school=user.school,user=student.id)
            serializer =  AttemptedQuizCreateSerializer(queryset ,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


#Question
class QuestionsListView(ListAPIView):
    """This views is only for school and subject teacher"""
    permission_classes = [IsSchoolAdmin|IsTeacher,]
    serializer_class = QuestionListSerializer
    queryset = Questions.objects.all()

    def get(self, request):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type == "SA":
            teach = Questions.objects.filter(quiz__teacher__user__school_id=user.school.id)
            serializer =  QuestionListSerializer(teach ,many=True)
        elif user.user_type=="TE":
            teacher = TeacherProfile.objects.get(user=self.request.user)
            teach = Questions.objects.filter(quiz__teacher=teacher.id)
            serializer =  QuestionListSerializer(teach ,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



class QuestionsCreateView(GenericAPIView):
    permission_classes = [IsTeacher,]
    serializer_class = QuestionCreateSerializer

    def post(self, request):
        try:
            user = TeacherProfile.objects.get(user=self.request.user.id)
            print(user.id)
            user_id=user.id
            data = {
                'teacher': user_id,
                'question': request.data['question'],                 
                'option1': request.data['option1'],
                "option2": request.data['option2'],
                "option3": request.data['option3'],
                "option4": request.data['option4'],
                "description": request.data['description'],
                "quiz": request.data['quiz'],
                "answer":request.data['answer']
            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            print(data)
            serializer = QuestionCreateSerializer(data=query_dict)
            if serializer.is_valid(raise_exception=True):
                quiz_id = request.data.get('quiz')
                print(quiz_id)
                quiz = Quiz.objects.get(id=quiz_id)
                print(quiz)
                q1=Questions.objects.filter(quiz=quiz_id).count()
                if not q1<quiz.total_question:
                    raise serializers.ValidationError(_('Invalid value'), code='no. of question exceed')

                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(serializer.errors, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with Teacher Account")


class QuestionByQuiz(ListAPIView):
    permission_classes = [IsSchoolAdmin|IsTeacher,]
    serializer_class = QuestionListSerializer

    def get_queryset(self):
        queryset = Questions.objects.all()
        print(queryset)
        question__quiz = self.kwargs.get('id')
        print(question__quiz)
        
        if question__quiz is not None:
            queryset = queryset.filter(
                quiz__id=question__quiz)
            return queryset


class StudentQuestionByQuiz(ListAPIView):
    permission_classes = [IsStudent,]
    serializer_class = QuestionListSerializer
    pagination_class = QuizPagination

    def get_queryset(self):
        print(self.request.data)
        student = StudentProfile.objects.get(user=self.request.user)
        queryset = Questions.objects.all()
        q = Quiz.objects.get(id = self.kwargs.get('id'))
        print(q)
        q.attended_users.add(student)
        q.save()
        q_data = {'user':student.id,'quiz':q.id}
        at_q = AtQuizCreateSerializer(data = q_data)
        try:
            at_q.is_valid(raise_exception = True)
            at_q.save()
        except Exception as e:
            print(e)
            pass
        print(queryset)
        question__quiz = self.kwargs.get('id')
        print(question__quiz)
        if question__quiz is not None:
            queryset = queryset.filter(
                quiz__id=question__quiz)
            return queryset


class QuestionsListByQuizView(ListAPIView):
    serializer_class = StdQuestionListSerializer
    queryset = Questions.objects.all()

    def get(self,request,*args,**kwargs):
        data = request.data
        print(data)
        try:
            quiz = AttemptedQuiz.objects.get(user = data['user'],quiz = data['quiz'])
            question_list = Questions.objects.filter(quiz = quiz).values('id','question','option1','option2','option3','option4')
            return Response({'data':question_list},status = status.HTTP_200_OK)
        except:
            return Response({'error':'Somthing went wrong'},status=status.HTTP_400_BAD_REQUEST)


class QuestionsDetailEditView(RetrieveUpdateAPIView):
    permission_classes = [IsTeacher,]
    queryset = Questions.objects.all()
    serializer_class = QuestionListSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        teacher = TeacherProfile.objects.get(user=self.request.user)
        schoool = Questions.objects.filter(quiz__teacher=teacher.id)#,grade=user.grade[0]
        print(schoool)
        return schoool

class QuestionsDetailDeleteView(DestroyAPIView):
    permission_classes = [IsTeacher,]
    queryset = Questions.objects.all()
    serializer_class = QuestionListSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        teacher = TeacherProfile.objects.get(user=self.request.user)
        schoool = Questions.objects.filter(quiz__teacher=teacher.id)
        return schoool


class AttempedQuizCreateView(GenericAPIView):
    serializer_class = AttemptedQuizCreateSerializer
    permission_classes = [IsStudent,]


    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        q = Quiz.objects.get(id = serializer.data['quiz'])
        q.attended_users.add(serializer.data['user'])
        q.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnswerSheetCreateView(GenericAPIView):
    serializer_class = AnswerSheetCreateSerializer
    permission_classes = [IsStudent,]

    def check_answer(self,data):
        correct_answer = 0
        uid = 0
        qid = 0
        aq = 0     
        try:
            qid = data['question']
            uid = data['user_id']
            q = Questions.objects.get(id = qid)
            q.attended_users.add(uid)
            q.save()
            if data['user_answer'] == q.answer:
                ans = AnswerSheet.objects.get(id = data['id'])
                ans.is_true = True
                aq = aq + 1
                ans.save()
            return aq
        except Exception as e:
            print(e)
            raise APIException("Can\t check the answers!")

    def post(self, request):
        answer = request.data['question']
        print(request.data)
        a = StudentProfile.objects.get(user=self.request.user)
        print(a.id)
        aq = 0
        for i in answer:

            serializer = self.serializer_class(data = i)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id=a.id)
            print(a.id)
            
            ca = self.check_answer(serializer.data)
            if ca == 1:
                aq = aq + 1
        return Response({'correct_answer': aq}, status=status.HTTP_200_OK)
    
    def get(self,request,*args, **kwargs):
        pass
        data = request.data

#shortQuestion


class ShortQuestionCreateView(CreateAPIView):
    serializer_class = ShortQuestionCreateSerializer
    permission_classes = [IsTeacher,]

    def post(self, request):
        try:
            user = TeacherProfile.objects.get(user=self.request.user.id)
            print(user.id)
            user_id=user.id
            data = {
                'teacher': user_id,
                'sub':request.data['sub'],
                'grade':request.data['grade'],
                'question': request.data['question'],                 
                'answer': request.data['answer'],
            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            print(data)
            serializer = ShortQuestionCreateSerializer(data=query_dict)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Short Question created Successfully',
                    'user': serializer.data
                }
        
                return Response(response, status=status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(serializer.errors, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with Teacher Account")


class ShortQuestionListView(ListAPIView):
    """This views is only for school and teacher"""
    permission_classes=(IsSchoolAdmin|IsTeacher,)
    queryset=ShortQuestion.objects.all()
    serializer_class=ShortQuestionListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['grade__grade_name','sub__subject',]
    ordering_fields = ['grade__grade_name','sub__subject',]
    lookup_field='pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type == "SA":
            teach = ShortQuestion.objects.filter(teacher__user__school_id=user.school.id).order_by('-created_at')
            return teach
            #serializer =  ShortQuestionListSerializer(teach ,many=True)
        elif user.user_type == "TE":
            teacher = TeacherProfile.objects.get(user=self.request.user)
            teach = ShortQuestion.objects.filter(teacher=teacher.id).order_by('-created_at')
            return teach
            #serializer =  ShortQuestionListSerializer(teach ,many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)


class StudentShortQuestionListView(ListAPIView):
    permission_classes=(IsStudent,)
    queryset=ShortQuestion.objects.all()
    serializer_class=ShortQuestionListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['sub__subject',]
    ordering_fields = ['sub__subject',]
    lookup_field='pk'

    def get_queryset(self):
        user = self.request.user
        student = StudentProfile.objects.get(user=self.request.user)
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        schoool = ShortQuestion.objects.filter(teacher__user__school=user.school,grade__grade_name=student.grade).order_by('-created_at').exclude(attended_users=student)
        print(schoool)
        return schoool
        # serializer =  ShortQuestionListSerializer(schoool ,many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)


class StudentShortQuestionDetailView(RetrieveAPIView):
    permission_classes=(IsStudent,)
    queryset=ShortQuestion.objects.all()
    serializer_class=ShortQuestionListSerializer

    def get(self, request,*args,**kwargs):
        user = self.request.user
        student = StudentProfile.objects.get(user=self.request.user)
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        schoool = ShortQuestion.objects.filter(id=kwargs['pk'],teacher__user__school=user.school,grade__grade_name=student.grade)#,grade=user.grade[0]
        print(schoool)
        serializer =  ShortQuestionListSerializer(schoool ,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShortQuestionDetailEditView(RetrieveUpdateAPIView):
    permission_classes = [IsTeacher,]
    queryset = ShortQuestion.objects.all()
    serializer_class = ShortQuestionUpdateSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        teacher = TeacherProfile.objects.get(user=self.request.user)
        schoool = ShortQuestion.objects.filter(teacher=teacher.id)#,grade=user.grade[0]
        print(schoool)
        return schoool


class ShortQuestionDetailDeleteView(DestroyAPIView):
    permission_classes = [IsTeacher,]
    queryset = ShortQuestion.objects.all()
    serializer_class = ShortQuestionListSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        teacher = TeacherProfile.objects.get(user=self.request.user)
        schoool = ShortQuestion.objects.filter(teacher=teacher.id)#,grade=user.grade[0]
        print(schoool)
        return schoool



class ShortAnswerSheetCreateView(GenericAPIView):
    permission_classes = (IsStudent,)
    serializer_class = ShortAnswerSheetCreateSerializer

    def check_answer(self,data):
        uid = 0
        qid = 0    
        try:
            a = StudentProfile.objects.get(user=self.request.user)
            qid = data['short_question']
            uid = a.id
            q = ShortQuestion.objects.get(id = qid)
            q.attended_users.add(uid)
            q.save()
        except Exception as e:
            print(e)
            raise APIException("Cant create answersheet")

    def post(self, request):
        #answer = request.data['short_question']
        print(request.data)
        a = StudentProfile.objects.get(user=self.request.user)
        print(a.id)
        data = {
            'user_id': a.id,
            'short_question':request.data['short_question'],
            'user_answer':request.data['user_answer'],
            }
        query_dict = QueryDict('', mutable=True)
        query_dict.update(data)
        print(data)
        serializer = ShortAnswerSheetCreateSerializer(data=query_dict)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        ca = self.check_answer(serializer.data)
        return Response('answersheet created', status=status.HTTP_200_OK)



class ShortAnswerSheetListView(ListAPIView):
    """This views is only for school and teacher"""
    permission_classes=(IsSchoolAdmin|IsTeacher,)
    queryset=ShortAnswerSheet.objects.all()
    serializer_class=ShortAnswerSheetListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['short_question__sub__subject',]
    ordering_fields = ['short_question__sub__subject',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type == "SA":
            teach = ShortAnswerSheet.objects.filter(short_question__teacher__user__school_id=user.school.id).order_by('-created_at')
            return teach
            #serializer =  ShortAnswerSheetListSerializer(teach ,many=True)
        elif user.user_type == "TE":
            teacher = TeacherProfile.objects.get(user=self.request.user)
            teach = ShortAnswerSheet.objects.filter(short_question__teacher=teacher.id).order_by('-created_at')
            return teach
        #     serializer =  ShortAnswerSheetListSerializer(teach ,many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)



class StudentShortAnswerSheetListView(ListAPIView):
    permission_classes=(IsStudent,)
    queryset=ShortAnswerSheet.objects.all()
    serializer_class=ShortAnswerSheetListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['short_question__sub__subject',]
    ordering_fields = ['short_question__sub__subject',]

    def get_queryset(self):
        user = self.request.user
        student = StudentProfile.objects.get(user=self.request.user)
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        schoool = ShortAnswerSheet.objects.filter(user_id=student.id).order_by('-created_at')
        print(schoool)
        return schoool
        # serializer =  ShortAnswerSheetListSerializer(schoool ,many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)


class ShortAnswerSheetDetailView(RetrieveAPIView):
    permission_classes=(IsStudent,)
    queryset=ShortAnswerSheet.objects.all()
    serializer_class=ShortQuestionListSerializer
    #lookup_field='pk'

    def get(self, request,*args,**kwargs):
        user = self.request.user
        student = StudentProfile.objects.get(user=self.request.user)
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        schoool = ShortAnswerSheet.objects.filter(id=kwargs['pk'],teacher__user__school=user.school,grade__grade_name=student.grade)#,grade=user.grade[0]
        print(schoool)
        serializer =  ShortAnswerSheetListSerializer(schoool ,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShortAnswerSheetDetailEditView(RetrieveUpdateAPIView):
    permission_classes = [IsTeacher,]
    queryset = ShortAnswerSheet.objects.all()
    serializer_class = ShortAnswerSheetUpdateSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        teacher = TeacherProfile.objects.get(user=self.request.user)
        schoool = ShortAnswerSheet.objects.filter(short_question__teacher=teacher.id)#,grade=user.grade[0]
        print(schoool)
        return schoool


class ShortAnswerSheetDetailDeleteView(DestroyAPIView):
    permission_classes = [IsTeacher,]
    queryset = ShortAnswerSheet.objects.all()
    serializer_class = ShortAnswerSheetListSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        teacher = TeacherProfile.objects.get(user=self.request.user)
        schoool = ShortAnswerSheet.objects.filter(teacher=teacher.id)#,grade=user.grade[0]
        print(schoool)
        return schoool


class ShortQuestionAnswerDetailListView(RetrieveUpdateAPIView):
    permission_classes = [IsTeacher|IsSchoolAdmin,]
    serializer_class = ShortQuestionAnswerDetailList
    queryset = ShortQuestion.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        user = self.request.user
        if user.user_type == "SA":
            teach = ShortQuestion.objects.filter(teacher__user__school_id=user.school.id).order_by('-created_at')
            return teach
        elif user.user_type == "TE":
            teacher = TeacherProfile.objects.get(user=self.request.user)
            teach = ShortQuestion.objects.filter(teacher=teacher.id).order_by('-created_at')
            return teach

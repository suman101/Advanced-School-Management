from django.shortcuts import render
from custom_settings.paginations import SchoolPagination

from custom_settings.permissions import IsSchoolAdmin, IsStudent, IsTeacher
from .models import CommentReplies, Post,Comment
from .serializers import CommentDetailSerializer, CommentListSerializer, CommentRepliesListSerializer, CommentUpdateSerializer,PostCreateSerializer, PostUpdateSerializer,PostlistSerializer,PostDetailSerializer,CommentCreateSerializer, ReplyCommentCreateSerializer, ReplyCommentUpdateSerializer
from authentication.models import StudentProfile, TeacherProfile, User
from rest_framework.generics import (GenericAPIView, RetrieveUpdateAPIView,ListAPIView,CreateAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView)
from rest_framework.response import Response
from rest_framework import status
from django.http import QueryDict
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter,OrderingFilter
import datetime
today = datetime.datetime.now()
#created_at__year=today.year
# Create your views here.



class PostCreateView(GenericAPIView):
    permission_classes = [IsTeacher,]
    serializer_class = PostCreateSerializer

    def post(self, request):
        try:
            user = TeacherProfile.objects.get(user=self.request.user.id)
            print(user.id)
            user_id=user.id
            data = {
                'teacher': user_id,
                'grade': request.data['grade'],                 
                'content': request.data['content'],                          

            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            serializer = PostCreateSerializer(data=query_dict)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'post created successfully',
                    'user': serializer.data
                }
        
                return Response(response, status=status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(serializer.errors, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with Teacher Account")




class PostListView(ListAPIView):
    permission_classes=(IsSchoolAdmin|IsTeacher|IsStudent,)
    queryset=Post.objects.all()
    serializer_class=PostlistSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['grade__grade_name','content']
    ordering_fields = ['grade__grade_name',]
    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Post.objects.filter(teacher__user__school=user.school.id)
            print(schoool)
            return schoool
            # serializer =  PostlistSerializer(schoool ,many=True)
            # return Response(serializer.data, status=status.HTTP_200_OK)
        elif user.user_type=="TE":
            teacher = TeacherProfile.objects.get(user=self.request.user)
            teach = Post.objects.filter(teacher=teacher.id)
            return teach
            # serializer =  PostlistSerializer(teach ,many=True)
            # return Response(serializer.data, status=status.HTTP_200_OK)
        if user.user_type=="ST":
            student = StudentProfile.objects.get(user=self.request.user)
            std = Post.objects.filter(teacher__user__school=user.school,grade__grade_name=student.grade)
            return std
            # serializer =  PostlistSerializer(std ,many=True)
            # return Response(serializer.data, status=status.HTTP_200_OK)



class PostDetailView(RetrieveAPIView):
    queryset=Post.objects.all()
    serializer_class=PostDetailSerializer
    lookup_field='pk'


class PostUpdateView(RetrieveUpdateAPIView):
    permission_classes =[IsTeacher,]
    queryset=Post.objects.all()
    serializer_class=PostUpdateSerializer
    lookup_field='pk'


class PostDeleteView(DestroyAPIView):
    permission_classes =[IsTeacher,]
    queryset=Post.objects.all()
    serializer_class=PostlistSerializer
    lookup_field='pk'


class CommentCreateView(GenericAPIView):
    permission_classes =[IsStudent,]
    serializer_class = CommentCreateSerializer

    def post(self, request):
        user = self.request.user
        print(user.user_type)
        if user.user_type == "ST":
            user = StudentProfile.objects.get(user=self.request.user.id)
            print(user)
            user_id=user.id
            data = {
                'post':request.data['post'],
                'comment_by': user_id,                
                'content': request.data['content'],                          

            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            serializer = CommentCreateSerializer(data=query_dict)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'comment added successfully',
                    'user': serializer.data
                }
        
                return Response(response, status=status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(serializer.errors, status=status_code)
        
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        


class ReplyCommentCreateView(GenericAPIView):
    permission_classes =[IsTeacher,]
    serializer_class = ReplyCommentCreateSerializer

    def post(self, request):
        try:
            user = TeacherProfile.objects.get(user=self.request.user.id)
            print(user)
            user_id=user.id
            data = {
                'respond_by': user_id,
                'comment': request.data['comment'],
                'content': request.data['content'],                                          

            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            serializer = ReplyCommentCreateSerializer(data=query_dict)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'comment replied added successfully',
                    'user': serializer.data
                }
        
                return Response(response, status=status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
            return Response(serializer.errors, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login to add comment")



class CommentListView(ListAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentListSerializer

class CommentDetailView(RetrieveAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentDetailSerializer
    lookup_field='pk'


class CommentUpdateView(UpdateAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentUpdateSerializer
    lookup_field='pk'


class CommentDeleteView(DestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentListSerializer
    lookup_field='pk'


class CommentRepliesListView(ListAPIView):
    queryset=CommentReplies.objects.all()
    serializer_class=CommentRepliesListSerializer


class CommentRepliesDetailView(RetrieveAPIView):
    queryset=CommentReplies.objects.all()
    serializer_class=CommentRepliesListSerializer
    lookup_field='pk'


class CommentRepliesUpdateView(UpdateAPIView):
    queryset=CommentReplies.objects.all()
    serializer_class=ReplyCommentUpdateSerializer
    lookup_field='pk'


class CommentRepliesDeleteView(DestroyAPIView):
    queryset=CommentReplies.objects.all()
    serializer_class=CommentRepliesListSerializer
    lookup_field='pk'

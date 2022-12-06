from django.urls import path
from .views import *

urlpatterns = [
    
    path('create-post/',PostCreateView.as_view(),name='post-create'),
    path('post-list/',PostListView.as_view(),name='post-list'),
    path('post-detail/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post-update/<int:pk>/',PostUpdateView.as_view(),name='post-update'),
    path('post-delete/<int:pk>/',PostDeleteView.as_view(),name='post-delete'),

    path('create-comment/',CommentCreateView.as_view(),name='comment-create'),
    
    path('comment-detail/<int:pk>/',CommentDetailView.as_view(),name='comment-detail'),
    path('comment-delete/<int:pk>/',CommentDeleteView.as_view(),name='comment-delete'),
    path('comment-update/<int:pk>/',CommentUpdateView.as_view(),name='comment-update'),
    
    path('comment-list/',CommentListView.as_view(),name='comment-list'),
    
    path('create-comment-reply/',ReplyCommentCreateView.as_view(),name='comment-reply-create'),
    path('comment-reply-detail/<int:pk>/',CommentRepliesDetailView.as_view(),name='comment-reply-detail'),
    path('comment-reply-delete/<int:pk>/',CommentRepliesDeleteView.as_view()),
    path('comment-reply-update/<int:pk>/',CommentRepliesUpdateView.as_view()),

]

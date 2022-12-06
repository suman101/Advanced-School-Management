from django.urls import path
from .views import *
urlpatterns = [
    path('create-exam/', ExamCreateView.as_view()),
    path('exam-list/', ExamListView.as_view()),
    path('student-exam-list/', AllExamListView.as_view()),
    path('exam-detail/<int:pk>/', ExamDetailView.as_view()),
    path('exam-update/<int:pk>/', ExamUpdateView.as_view()),
    path('exam-delete/<int:pk>/', ExamDeleteView.as_view()),

    path('create-marksheet/', MarksheetCreateView.as_view()),
    path('marksheet-list/', MarksheetListView.as_view()),
    path('student-marksheet-list/', StudentMarksheetListView.as_view()),
    path('marksheet-detail/<int:pk>/', MarksheetDetailView.as_view()),
    path('marksheet-update/<int:pk>/', MarksheetUpdateView.as_view()),
    path('marksheet-delete/<int:pk>/', MarksheetDeleteView.as_view()),

    #path('create-mark/', MarkCreateView.as_view()),
    path('mark-list/', MarkListView.as_view()),
    path('student-mark-list/', StudentMarkListView.as_view()),
    path('mark-detail/<int:pk>/', MarkDetailView.as_view()),
    #path('mark-update/<int:pk>/', MarkUpdateView.as_view()),
    path('mark-delete/<int:pk>/', MarkDeleteView.as_view()),

    # path('ma/<int:pk>/', Marksheets.as_view()),
    # path('ma/<int:pk>/', StdMarksUpdateView.as_view()),

    path('marksheetbystd/<int:pk>/', StdMarksView.as_view()),
    path('marksheetbygrade/', MarksheetByGrade.as_view()),

]
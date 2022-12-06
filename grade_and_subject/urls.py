from django.urls import path
from .views import *


urlpatterns = [
    path('create-subject/', SubjectAddView.as_view(),name='add-subject'),
    path('subject-update/<int:pk>/', SubjectUpdateView.as_view(),name='subject-update'),
    path('subject-delete/<int:pk>/', SubjectDeleteView.as_view(),name='subject-Delete'),
    path('subject-list/', SubjectListView.as_view(),name='schoolandteachersubject-list'),
    path('all-subject-list/', AllSubjectListView.as_view(),name='schoolandteachersubject-list'),
    path('all-sub-teacher-list/', AllSubjectTeacherListView.as_view()),

    path('create-grade/', GradeAddView.as_view(),name='add-grade'),
    path('grade-update/<int:pk>/', GradeUpdateView.as_view(),name='grade-update'),
    path('grade-delete/<int:pk>/', GradeDeleteView.as_view(),name='grade-Delete'),
    path('grade-list/', GradeListView.as_view(),name='schoolandteachergrade-list'),
    path('student-grade-list/', StudentGradeListView.as_view(),name='student-grade-update'),

    path('all-grade-teacher-list/', AllGradeListView.as_view()),
    path('sub-by-grade/', SubjectbyGradeListView.as_view()),

    path('create-class-routine/', ClassRoutineAddView.as_view()),
    path('class-routine-update/<int:pk>/', ClassRoutineUpdateView.as_view()),
    path('class-routine-delete/<int:pk>/', ClassRoutineDeleteView.as_view()),
    path('class-routine-list/', ClassRoutineListView.as_view()),
    path('class-routine-by-grade/', ClassRoutinebyGradeListView.as_view()),

    
]
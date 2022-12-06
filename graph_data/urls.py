from django.urls import path
from .views import *

urlpatterns = [
    path('school-count/', TotalSchoolCountView.as_view()),
    path('student-count/', TotalStudentCountView.as_view()),
    path('teacher-count/', TotalTeacherCountView.as_view()),
    path('quiz-count/', TotalQuizCountView.as_view()),
    path('marksheet-count/', MarksNagarAdminView.as_view()),
    path('caste-count/', TotalCasteCountView.as_view()),
    path('religion-count/', TotalReligionCountView.as_view()),
    path('note-count/', TotalNotesCountView.as_view()),
    path('mcq-count/', TotalMcqCountView.as_view()),
    path('student-count-school/', TotalStudentSchoolCountView.as_view()),
    #path('year/', MarksheetYearListView.as_view()),

    path('count-religion-and-caste/',CasteAndReligionView.as_view()),
    path('school-count-religion-and-caste/',SchoolGradeCasteAndReligionView.as_view()),
    
]
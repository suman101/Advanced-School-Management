from django.urls import path
from . import views
urlpatterns = [
    path('quiz-create/',views.QuizCreateView.as_view(),name='quiz-create'),
    path('quiz-list/', views.QuizListView.as_view(),name='quiz-list-teacher-and-school'),

    path('quiz-detail/<int:pk>/', views.QuizDetailView.as_view(),name='quiz-detail-teacher-and-school'),

    path('student-quiz-list/', views.StudentQuizListView.as_view(),name='quiz-list-student'),
    path('student-quiz-detail/<int:pk>/', views.StudentQuizDetailView.as_view(),name='quiz-list-student'),
    path('quiz/quiz-searchbytitle/', views.QuizSearchView.as_view(), name='Quiz-by-searching'),
    path('quiz/updatequiz/<int:pk>/', views.QuizDetailEditView.as_view(), name='Quiz-detailedit-view'),
    path('quiz/deletequiz/<int:pk>/', views.QuizDetailDeleteView.as_view(), name='Quiz-detaildelete-view'),
    path('quiz-report/<int:pk>/',views.QuizResultView.as_view()),
    path('quiz-report-list/',views.QuizTableResultView.as_view()),

    path('quiz-by-sub/<int:id>/', views.ActiveQuizBySubject.as_view(),name='quiz-by-sub-name'),

    path('question/allquestion/', views.QuestionsListView.as_view(), name='Question-list-view'),
    path('question/allquestionbyquiz/', views.QuestionsListByQuizView.as_view(), name='Question-list-view'),

    path('question-create/',views.QuestionsCreateView.as_view(),name='question-create'),
    path('question/updatequestion/<int:pk>/', views.QuestionsDetailEditView.as_view(), name='Question-detailedit-view'),
    path('question/deletequestion/<int:pk>/', views.QuestionsDetailDeleteView.as_view(), name='Question-detaildelete-view'),
    path('question/questionquiz/<int:id>/', views.QuestionByQuiz.as_view(), name='questionbyquiz'),
    path('question/studentquestionquiz/<int:id>/', views.StudentQuestionByQuiz.as_view(), name='studentquestionbyquiz'),



    path("attemptedquizadd/", views.AttempedQuizCreateView.as_view(), name="attmptedquiz-add" ),
    path("answersheetadd/", views.AnswerSheetCreateView.as_view(), name="answersheet-add" ),


    path('shortquestion-create/',views.ShortQuestionCreateView.as_view(),name='shortquestion-create'),
    path('shortquestion-list/', views.ShortQuestionListView.as_view(),name='shortquestion-list-teacher-and-school'),
    path('student-shortquestion-list/', views.StudentShortQuestionListView.as_view(),name='shortquestion-list-student'),
    path('student-shortquestion-detail/<int:pk>/', views.StudentShortQuestionDetailView.as_view(),name='shortquestion-list-student'),
    path('shortquestion/update/<int:pk>/', views.ShortQuestionDetailEditView.as_view(), name='shortquestion-detail-edit-view'),
    path('shortquestion/delete/<int:pk>/', views.ShortQuestionDetailDeleteView.as_view(), name='shortquestion-detail-delete-view'),

    path('shortanswersheet-create/',views.ShortAnswerSheetCreateView.as_view()),
    path('shortanswersheet-list/', views.ShortAnswerSheetListView.as_view()),
    path('student-shortanswersheet-list/', views.StudentShortAnswerSheetListView.as_view()),
    path('student-shortanswersheet-detail/<int:pk>/', views.ShortAnswerSheetDetailView.as_view()),
    path('shortanswersheet/update/<int:pk>/', views.ShortAnswerSheetDetailEditView.as_view()),
    path('shortanswersheet/delete/<int:pk>/', views.ShortAnswerSheetDetailDeleteView.as_view()),

    path('teacher-shortanswersheet-list/<int:pk>/', views.ShortQuestionAnswerDetailListView.as_view()),
]
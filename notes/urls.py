from django.urls import path
from .views import *
urlpatterns = [
    path('create-note/', NoteCreateView.as_view(),name='note-create'),
    path('note-list/', TeacherNoteListView.as_view(),name='note-list'),
    path('student-note-list/', StudentNoteListView.as_view(),name='note-list'),
    path('student-note-detail/<int:pk>/', StudentNoteDetailView.as_view(),name='note-detail'),
    path('student-note-update/<int:pk>/', NoteUpdateView.as_view(),name='note-update'),
    path('student-note-delete/<int:pk>/', NoteDeleteView.as_view(),name='note-delete'),

    path('pub-note-list/', NoteCardListView.as_view()),

]
from django.urls import path
from .views import *
urlpatterns = [
    path('send-mail/', MailboxAddView.as_view()),
    path('mail-list/', MailboxListView.as_view()),
    path('send-list/', SendListView.as_view(),name='note-list'),
    # path('student-note-detail/<int:pk>/', StudentNoteDetailView.as_view(),name='note-detail'),
    path('unseen-mail/<int:pk>/', UnseenMailSeenView.as_view()),
    path('unseen-mail-list/', UnseenMailListView.as_view()),
    path('important-mail/<int:pk>/', ImportantMailView.as_view()),
    path('important-mail-list/', ImportantMailListView.as_view()),
    path('mail-count/', MailsCountView.as_view()),

    path('draft-mail-list/', DraftMailListView.as_view()),
    path('trash-mail-list/', TrashMailListView.as_view()),

    path('mail-update/<int:pk>/', MailboxUpdateView.as_view()),
    path('mail-delete/<int:pk>/', MailboxDeleteView.as_view()),

]
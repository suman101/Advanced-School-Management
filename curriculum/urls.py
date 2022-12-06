from django.urls import path
from .views import CurriculumCreateView, CurriculumDeleteView, CurriculumDetailView, CurriculumListView,CurriculumUpdateView, DraftCurriculumDetailListView, PublishedCurriculumDetailListView

urlpatterns = [
    path('curriculum-create/', CurriculumCreateView.as_view()),
    path('curriculum-list/', CurriculumListView.as_view()),  ### endpoint for nagar admin
    path('published-curriculum-list/', PublishedCurriculumDetailListView.as_view()),  ## shown to all

    path('draft-curriculum-list/', DraftCurriculumDetailListView.as_view()),
    path('curriculum-detail/<int:pk>/', CurriculumDetailView.as_view()),
    path('curriculum-update/<int:pk>/', CurriculumUpdateView.as_view()),
    path('curriculum-delete/<int:pk>/', CurriculumDeleteView.as_view()),
]
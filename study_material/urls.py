from django.urls import path
from .views import *


urlpatterns = [
       # study material endpoint
    path('study-material-list/', StudyMaterialListView.as_view()),
    path('published-study-material-list/', PublishedStudyMaterialListView.as_view()),
    path('public-study-material-list/', PublicStudyMaterialListView.as_view()),
    path('draft-study-material-list/', DraftStudyMaterialListView.as_view()),
    path('study-material-create/', StudyMaterialCreateView.as_view()),
    path('study-material-detail/<slug>/', StudyMaterialDetailView.as_view()),
    path('study-material-delete/<slug>/', StudyMaterialDeleteView.as_view()),

    path('pub-study-material-list/', PublicStudyMaterialCardListView.as_view()),
    ]
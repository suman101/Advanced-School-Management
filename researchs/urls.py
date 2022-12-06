from django.urls import path
from .views import *


urlpatterns = [
    
       # category endpoint
    path('category-list/', CategoryListView.as_view()),
    path('category-create/', CategoryCreateView.as_view()),
    path('category-detail/<int:pk>/', CategoryDetailView.as_view()),
    path('category-delete/<int:pk>/', CategoryDeleteView.as_view()),
        
        # detail paper endpoint
    path('research-list/', ResearchDetailListView.as_view()),
    path('published-research-list/', PublishedResearchDetailListView.as_view()),
    path('public-research-list/', PublicResearchDetailListView.as_view()),
    path('draft-research-list/', DraftResearchDetailListView.as_view()),
    path('research-create/', ResearchDetailCreateView.as_view()),
    path('research-detail/<slug>/', ResearchDetailDetailView.as_view()),
    path('research-delete/<int:pk>/', ResearchDetailDeleteView.as_view()),

    path('pub-research-list/', PublicResearchDetailCardListView.as_view()),

        # path('createsubject/', SubjectAddView.as_view(),name='add-subject'),
        # path('subjectupdate/<int:pk>/', SubjectUpdateView.as_view(),name='subject-update'),
        # path('subjectdelete/<int:pk>/', SubjectDeleteView.as_view(),name='subject-Delete'),
        
]

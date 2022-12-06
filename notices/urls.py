from django.urls import path
from . import views
urlpatterns = [
    path('create-notice/', views.NoticeCreateView.as_view(),name='notice-create'),
    path('notice-list/', views.NoticeListView.as_view(),name='notice-list'),
    path('notice-detail/<int:pk>/', views.NoticeDetailView.as_view()),
    path('notice-update/<int:pk>/', views.NoticeUpdateView.as_view()),
    path('notice-delete/<int:pk>/', views.NoticeDeleteView.as_view()),
    path('school-notice/me/', views.NoticeSchoolListView.as_view()),

    path('admin-draft-notice-list/', views.NoticeDraftListView.as_view()),
    path('school-draft-notice-list/me/', views.NoticeSchoolDraftListView.as_view()),

    

    path('all-notice/', views.AllPublicNoticePagiListView.as_view()),
    path('all-notice-card/', views.AllPublicNoticesListView.as_view()),

    path('notice-dashboard/', views.NoticeListDashboard.as_view()),
    
    
    #path('event-list/', views.EventListView.as_view(),name='event-list'),

    #path('create-feedback/', views.FeedbackCreateView.as_view(),name='feedback-create-school'),
    #path('feedback-list/', views.FeedbackListView.as_view(),name='feedback-list-school'),
    #path('admin-feedback-list/', views.FeedbackListAdminView.as_view(),name='feedback-list-admin-view'),
    #path('feedback-update/<int:pk>/', views.FeedbackUpdateView.as_view(),name='feedback-update-view'),


]
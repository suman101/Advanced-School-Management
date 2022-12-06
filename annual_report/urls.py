from django.urls import path
from . import views
urlpatterns = [
	path('report-create/', views.ReportCreateView.as_view()),
    path('report-list/', views.ReportListView.as_view()),
    path('report-update/<int:pk>/', views.ReportUpdateView.as_view()),
    path('report-delete/<int:pk>/', views.ReportDeleteView.as_view()),
]
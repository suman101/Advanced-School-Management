from django.urls import path
from . import views
urlpatterns = [
    path('about-us-create/', views.CreateAboutUsApiView.as_view()),
    path('about-us-update/<int:pk>/', views.AboutUsApiView.as_view()),
    path('about-us-list/', views.AboutUsListApiView.as_view()),

    path('contact-us/create/', views.CreateContactUsApiView.as_view()),
    path('contact-us-update/<int:pk>/', views.ContactUsApiView.as_view()),
    path('contact-us-list/', views.ContactListUsApiView.as_view()),

	path('privacy-policy/create/', views.CreatePrivacyApiView.as_view()),
    path('privacy-policy/', views.ListPrivacyApiView.as_view()),
    path('privacy-policy/<int:pk>/', views.UpdatePrivacyApiView.as_view()),

    path('term-condition/create/', views.CreateTermApiView.as_view()),
    path('term-condition/', views.ListTermApiView.as_view()),
    path('term-condition/<int:pk>/', views.UpdateTermApiView.as_view()),

    path('create-cms/', views.CreateCMSView.as_view()),
    path('list-cms/', views.ListCMSView.as_view()),
    path('update-cms/<slug>/', views.UpdateCMSView.as_view()),
    path('detail-cms/<slug>/', views.DetailCMSView.as_view()),

    path('faq/',views.FaqCreateView.as_view()),
    path('faq-detail/<int:id>/',views.FaqDetailView.as_view()),

    path('smtp/',views.SmtpView.as_view()),
    path('smtp-detail/<int:pk>/',views.SmtpDetailView.as_view()),

    path('homepage-nagar/',views.HomePageNagarAdminListApiView.as_view()),
    path('homepage-nagar-detail/<int:pk>/',views.HomePageNagarAdminApiView.as_view()),

    path('create-homepage-school/', views.HomePageSchoolAdminCreateView.as_view()),
    path('homepage-school/',views.HomePageSchoolAdminListApiView.as_view()),
    path('homepage-school-detail/<int:pk>/',views.HomePageSchoolAdminApiView.as_view()),


    path('send-mail/', views.MailSendView.as_view()),
    path('bulk-mail/', views.BulkMailSendView.as_view()),

]
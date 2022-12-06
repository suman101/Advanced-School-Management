"""School_Management_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

#swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="API Doc",
      default_version='v1',
      description="School Managemet System",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@abc.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('research/', include('researchs.urls')),
    path('notices/',include('notices.urls')),
    path('notes/',include('notes.urls')),
    path('custom-settings/',include('custom_settings.urls')),
    path('mcqs/',include('mcqs.urls')),
    path('posts/',include('posts.urls')),
    path('grades/',include('grade_and_subject.urls')),
    path('study-materials/',include('study_material.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('curriculum/', include('curriculum.urls')),
    path('graph_data/', include('graph_data.urls')),
    path('marksheet/', include('marksheet.urls')),
    path('mailboxes/', include('mailboxes.urls')),
    path('annual/', include('annual_report.urls')),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

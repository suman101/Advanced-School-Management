from django.urls import URLPattern, path, include
from rest_framework_simplejwt import views as jwt_views
from .views import *
urlpatterns = [

    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('change-user-password/',ChangePasswordView.as_view(), name='change-password'),

    path('school-register/', SchoolRegistrationView.as_view(),name='school-register'),
    path('school-list/', SchoolListView.as_view(),name='school-list'),
    path('school-update/<slug>/', SchoolUpdateView.as_view(),name='school-update'),

    path('all-school-list/', AllSchoolListView.as_view(),name='all-school-list'),


    path('teacher-register/', TeacherRegistrationView.as_view(),name='teacher-register'),
    path('student-register/', StudentRegistrationView.as_view(),name='student-register'),
    path('parentRegister/', ParentRegistrationView.as_view(),name='parent-register'),
    path('staffRegister/', StaffRegistrationView.as_view(),name='staff-register'),
    path('librarianRegister/', LibrarianRegistrationView.as_view(),name='librarian-register'),


    path('teacherupdate/<int:pk>/', TeacherUpdateView.as_view(),name='teacher-update'),
    path('studentupdate/<int:pk>/', StudentUpdateView.as_view(),name='student-update'),
    path('parentupdate/<int:pk>/', ParentUpdateView.as_view(),name='parent-update'),
    path('staffupdate/<int:pk>/', StaffUpdateView.as_view(),name='staff-update'),
    path('librarianupdate/<int:pk>/', LibrarianUpdateView.as_view(),name='librarian-update'),


    path('school-delete/<slug>/', SchoolDeleteView.as_view(),name='school-Delete'),
    path('teacher-delete/<int:pk>/', TeacherDeleteView.as_view(),name='teacher-Delete'),
    path('student-delete/<int:pk>/', StudentDeleteView.as_view(),name='student-Delete'),
    path('parentdelete/<int:pk>/', ParentDeleteView.as_view(),name='parent-Delete'),
    path('staffdelete/<int:pk>/', StaffDeleteView.as_view(),name='staff-Delete'),
    path('librariandelete/<int:pk>', LibrarianDeleteView.as_view(),name='librarian-Delete'),

    path('listof-teacher/', TeacherListView.as_view(),name='teacher-list'),
    path('all-listof-teacher/', AllTeacherListView.as_view(),name='teacher-list'),
    
    path('Listof-staff/', StaffListView.as_view(),name='staff-staff'),
    path('listof-student/', StudentListView.as_view(),name='student-list'),
    path('Listof-parent/', ParentListView.as_view(),name='parent-list'),
    path('Listof-librarian/', LibrarianListView.as_view(),name='librarian-list'),

    # path('detailof-teacher/<int:pk>', TeacherDetailView.as_view(),name='teacher-detail'),
    #path('detailof-grade/<str:pk>', GradeDetailView.as_view(),name='grade-detail'),

    path('listof-studentbygrade/', StudentListByGrade.as_view(),name='student-list'),
    path('student-bulk-grades-update/', StudentClassBulkUpdateView.as_view(),name='grade-bulk-update'),

    path('student-profile/<int:pk>/', StudentProfileView.as_view(),name='student-profile'),
    path('school-profile/<int:pk>/', SchoolProfileView.as_view(),name='school-profile'),
    path('teacher-profile/<int:pk>/', TeacherProfileView.as_view(),name='teacher-profile'),
    path('staff-profile/<int:pk>/', StaffProfileView.as_view(),name='staff-profile'),
    path('librarian-profile/<int:pk>/', LibrarianProfileView.as_view(),name='librarian-profile'),

    path('updateprofilepic/<int:pk>/', UpdateProfilePictureView.as_view()),
    path('studentprofilepic/<int:pk>/', DeleteProfilePictureView.as_view()),

    path('updateteacherprofilepic/<int:pk>/', UpdateTeacherProfilePictureView.as_view()),
    path('deleteteacherprofilepic/<int:pk>/', DeleteTeacherProfilePictureView.as_view()),

    path('updateschoolprofilepic/<int:pk>/', UpdateSchoolProfilePictureView.as_view()),
    path('deleteschoolprofilepic/<int:pk>/', DeleteSchoolProfilePictureView.as_view()),


    path('password-reset/', PasswordResetView.as_view()),
    path('password-reset/<uidb64>/<token>/', ResetPasswordTokenCheckView.as_view(),name = 'password_token_check'),
    path('password-reset-complete/', NewPasswordView.as_view()),

    path('image-gallery-create/',ProfileImageCreateView.as_view()),
    path('image-gallery-list/',ProfileImageListView.as_view()),
    path('image-gallery-delete/<str:pk>/',ProfileImageDeleteView.as_view()),
    
    path('public-gallery-list/',PublicProfileImageListView.as_view()),

    path('update-school-about-us/<int:pk>/', AboutUsSchoolApiView.as_view()),
    path('public-about-us-school/', PublicAboutUsSchoolApiView.as_view()),

 
]

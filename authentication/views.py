from django.shortcuts import render
from custom_settings.paginations import SchoolPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import ImageGallarySerializer, MyTokenObtainPairSerializer, NewPasswordSerializers, PasswordResetSerializers, ProfilePictureSerializer, SchoolAboutUsSerializers, SchoolAdminCreateSerializer, SchoolProfilePictureSerializer, StaffRegisterSerializer, ParentRegisterSerializer, StudentProfileCreateSerializer, StudentProfileListViewSerializer, StudentRegisterSerializer, TeacherProfilePictureSerializer, TeacherRegisterSerializer, SchoolRegisterSerializer, ChangePasswordSerializer, SchoolUpdateSerializer, TeacherUpdateSerializer, StudentUpdateSerializer, ParentUpdateSerializer, StaffUpdateSerializer, SchoolListSerializer, TeacherListSerializer, StudentListSerializer, ParentListSerializer, StaffListSerializer, TeacherDetailSerializer, GradeListSerializer, GradeDetailSerializer, StudentProfileViewSerializer, TeacherProfileViewSerializer, StaffProfileViewSerializer, SchoolProfileViewSerializer, LibrarianRegisterSerializer, LibrarianUpdateSerializer, SchoolInfoSerializer, TeacherInfoSerializer, StudentInfoSerializer, StaffInfoSerializer, LibrarianInfoSerializer, LibrarianListSerializer, LibrarianProfileViewSerializer
from rest_framework.generics import (GenericAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView,
                                     ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import ImageGallary, User, SchoolProfile, TeacherProfile, StaffProfile, StudentProfile, LibrarianProfile
from django.http import QueryDict
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django_filters import rest_framework as filters
from researchs.models import Subjects
from custom_settings.permissions import IsNagarAdmin, IsSchoolAdmin, IsStudent, IsTeacher
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.exceptions import ValidationError, PermissionDenied,NotFound
from django.shortcuts import get_object_or_404
from custom_settings.utils import send_email, send_reset_password
from django.urls import reverse
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Create your views here.

# ------------Login---------------------------------------------


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ------------------------SCHOOL-------------------------------


class SchoolRegistrationView(GenericAPIView):
    """krishna"""
    serializer_class = SchoolRegisterSerializer
    permission_classes = (IsNagarAdmin,)
    def create_school_admin(self,data):
        data = data
        serializer = SchoolAdminCreateSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data['id']
    
    def assign_school_to_admin(self,user_id,school_id):
        user = User.objects.get(id = user_id)
        school = SchoolProfile.objects.get(id = school_id)
        user.school = school 
        user.user_type = 'SA'
        user.save()
        return

    def post(self, request,**kwargs):
        """
        sample json
        {
        "school":{
            "school_name":"school1",
            "phone_number":"9874563210"
         },
        "user":{
            "email":"schooladmin2@gmail.com",
            "password":"admin12345",
            "confirm_password":"admin12345"
            }
        }

        """
        data = request.data['school']
        data1=request.data['user']
        # print(data1['password'])
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            try:
                user_id = self.create_school_admin(request.data['user'])
            except Exception as e:
                status_code = status.HTTP_400_BAD_REQUEST
                response = {
                'success': True,
                'statusCode': status_code,
                'message': e.detail,
                }
                return Response(response, status=status_code)
            serializer.save()
            self.assign_school_to_admin(user_id,serializer.data['id'])
            user = User.objects.get(id = user_id)
            try:
                data = {
                    'subject':"SMS CREDINTIALS",
                    'username': user.username,
                    'email': user.email,
                    'password': data1['password'],
                }
                send_email(data)
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'School added successfully',
            }
        else:
            response = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)


class SchoolListView(ListAPIView):
    """krsihna"""
    permission_classes = (IsNagarAdmin,)
    serializer_class = SchoolListSerializer
    queryset = SchoolProfile.objects.all()
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['school_name','address','school_type']
    ordering_fields = ['school_name','school_type']


class AllSchoolListView(ListAPIView):
    """suds"""
    serializer_class = SchoolListSerializer
    queryset = SchoolProfile.objects.all().order_by('school_name')
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['school_name','address','school_type']
    ordering_fields = ['school_name','school_type']


class SchoolUpdateView(RetrieveUpdateAPIView):
    """krishna"""
    serializer_class = SchoolUpdateSerializer
    permission_classes = (IsNagarAdmin | IsSchoolAdmin,)
    queryset = SchoolProfile.objects.all()
    lookup_field = 'slug'

    def get_object(self):
        print('obj get')
        print(self.request.headers)
        queryset = self.filter_queryset(self.get_queryset())
        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)
        print(self.request.user)
        if not self.request.user.school == obj and not self.request.user.user_type == 'NA':
            # return Response({'error':'not school admin'},status =status.HTTP_400_BAD_REQUEST)
            raise PermissionDenied()
        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
    

class TeacherRegistrationView(GenericAPIView):
    """krishna"""
    serializer_class = TeacherRegisterSerializer
    permission_classes = (IsSchoolAdmin,)
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        school = user.school.id
        data = {
            'school': school,
            'email': request.data['email'],
            'username': request.data['username'],
            'dob': request.data['dob'],
            'gender': request.data['gender'],
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'],
            'password': request.data['password'],
            'confirm_password': request.data['confirm_password'],
            'phone_number': request.data['phone_number'],
        }
        data1 = request.data
        query_dict = QueryDict('', mutable=True)
        query_dict.update(data)
        serializer = TeacherRegisterSerializer(data=query_dict)
        
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            try:
                send_email(data1['username'], data1['email'], data1['password'])
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'message': 'Teacher added successfully',
                'user': serializer.data
            }
            return Response(response, status=status_code)
        else:
            response = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status=status_code)


class StudentRegistrationView(GenericAPIView):
    """krishna"""
    serializer_class = StudentRegisterSerializer
    permission_classes = (IsSchoolAdmin,)
    
    def create_std_profile(self,user_id,data):
        user = User.objects.get(id = user_id)
        data['user'] = user.id
        serializer = StudentProfileCreateSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return
    def post(self, request):
        user = User.objects.get(id=request.user.id)
        school = user.school.id
        data = request.data
        user_data = data['user']
        user_data = {
            'school': school,
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'dob': user_data['dob'],
            'gender': user_data['gender'],
            'username': user_data['username'],
            'phone_number': user_data['phone_number'],
            'password': user_data['password'],
            'confirm_password': user_data['confirm_password'],
        }
        query_dict = QueryDict('', mutable=True)
        query_dict.update(user_data)
        serializer = StudentRegisterSerializer(data=query_dict)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            self.create_std_profile(serializer.data['id'],data['std_profile'])
            try:
                send_email(user_data['username'], user_data['email'], user_data['password'])
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success': True,
                'message': 'Student added successfully',
                'user': serializer.data
            }
            return Response(response, status=status_code)
        else:
            response = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status=status_code)


class ParentRegistrationView(GenericAPIView):
    serializer_class = ParentRegisterSerializer

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            user_id = user.id
            if user and user.user_type == "SA":
                user_id = user.id
                data = {
                    'school': user_id,
                    'first_name': request.data['first_name'],
                    'last_name': request.data['last_name'],
                    'dob': request.data['dob'],
                    'gender': request.data['gender'],
                    'email': request.data['email'],
                    'username': request.data['username'],
                    'phone_number': request.data['phone_number'],
                    'password': request.data['password'],
                    'confirm_password': request.data['confirm_password'],

                }
                query_dict = QueryDict('', mutable=True)
                query_dict.update(data)
                serializer = ParentRegisterSerializer(data=query_dict)

                valid = serializer.is_valid(raise_exception=True)

                if valid:

                    serializer.save()
                    status_code = status.HTTP_201_CREATED

                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'Parent added successfully',
                        'user': serializer.data
                    }

                    return Response(response, status=status_code)
                else:
                    response = {
                        'error': "please enter a validated data",
                    }
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(response, status=status_code)
            else:
                response = {
                    'error': "Cannot created, Please Login with School Account"
                }
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with School Account")


class StaffRegistrationView(GenericAPIView):
    serializer_class = StaffRegisterSerializer

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            user_id = user.id
            if user and user.user_type == "SA":
                user_id = user.id
                data = {
                    'school': user_id,
                    'first_name': request.data['first_name'],
                    'last_name': request.data['last_name'],
                    'dob': request.data['dob'],
                    'gender': request.data['gender'],
                    'email': request.data['email'],
                    'username': request.data['username'],
                    'phone_number': request.data['phone_number'],
                    'password': request.data['password'],
                    'confirm_password': request.data['confirm_password'],

                }
                query_dict = QueryDict('', mutable=True)
                query_dict.update(data)
                serializer = StaffRegisterSerializer(data=query_dict)

                valid = serializer.is_valid(raise_exception=True)

                if valid:

                    serializer.save()
                    status_code = status.HTTP_201_CREATED

                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'staff added successfully',
                        'user': serializer.data
                    }

                    return Response(response, status=status_code)
                else:
                    response = {
                        'error': "please enter a validated data",
                    }
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(response, status=status_code)
            else:
                response = {
                    'error': "Cannot created, Please Login with School Account"
                }
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with School Account")


class LibrarianRegistrationView(GenericAPIView):
    serializer_class = LibrarianRegisterSerializer

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            user_id = user.id
            if user and user.user_type == "SA":
                user_id = user.id
                data = {
                    'school': user_id,
                    'email': request.data['email'],
                    'first_name': request.data['first_name'],
                    'last_name': request.data['last_name'],
                    'dob': request.data['dob'],
                    'gender': request.data['gender'],
                    'username': request.data['username'],
                    'phone_number': request.data['phone_number'],
                    'password': request.data['password'],
                    'confirm_password': request.data['confirm_password'],

                }
                query_dict = QueryDict('', mutable=True)
                query_dict.update(data)
                serializer = LibrarianRegisterSerializer(data=query_dict)

                valid = serializer.is_valid(raise_exception=True)

                if valid:

                    serializer.save()
                    status_code = status.HTTP_201_CREATED

                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'Librarian added successfully',
                        'user': serializer.data
                    }

                    return Response(response, status=status_code)
                else:
                    response = {
                        'error': "please enter a validated data",
                    }
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(response, status=status_code)
            else:
                response = {
                    'error': "Cannot created, Please Login with School Account"
                }
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with School Account")


# ---------------------------------Change Password--------------------------------------------

class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            serializer.save()
            return Response({"success": "password changed Successfully"})


# ----------------------------Update User---------------------------------------




class TeacherUpdateView(RetrieveUpdateAPIView):
    serializer_class = TeacherUpdateSerializer
    permission_classes = (IsTeacher,)
    queryset = TeacherProfile.objects.all()
    lookup_field = 'pk'


class StudentUpdateView(RetrieveUpdateAPIView):
    serializer_class = StudentUpdateSerializer
    permission_classes = (IsStudent,)
    queryset = StudentProfile.objects.all()
    lookup_field = 'pk'
    


class StaffUpdateView(UpdateAPIView):
    serializer_class = StaffUpdateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = StaffProfile.objects.all()
    lookup_field = 'pk'


class ParentUpdateView(UpdateAPIView):
    serializer_class = ParentUpdateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = 'pk'


class LibrarianUpdateView(UpdateAPIView):
    serializer_class = LibrarianUpdateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = LibrarianProfile.objects.all()
    lookup_field = 'pk'


# ------------------------User Delete-------------------------


class SchoolDeleteView(DestroyAPIView):
    serializer_class = SchoolInfoSerializer
    permission_classes = (IsNagarAdmin,)
    queryset = SchoolProfile.objects.all()
    lookup_field = 'slug'


class TeacherDeleteView(DestroyAPIView):
    serializer_class = TeacherInfoSerializer
    permission_classes = (IsSchoolAdmin,)
    queryset = User.objects.all()
    lookup_field = 'pk'
    def delete(self, request, *args, **kwargs):
        try:
            if request.user.school == User.objects.get(id = kwargs['pk']).school:
                return self.destroy(request, *args, **kwargs)
            else:
                raise PermissionDenied()
        except ObjectDoesNotExist:
            raise NotFound()


class StudentDeleteView(DestroyAPIView):
    serializer_class = StudentInfoSerializer
    permission_classes = (IsSchoolAdmin,)
    queryset = User.objects.all()
    lookup_field = 'pk'
    def delete(self, request, *args, **kwargs):
        try:
            if request.user.school == User.objects.get(id = kwargs['pk']).school:
                return self.destroy(request, *args, **kwargs)
            else:
                raise PermissionDenied()
        except ObjectDoesNotExist:
            raise NotFound()


class StaffDeleteView(DestroyAPIView):
    serializer_class = StaffInfoSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = 'pk'


class ParentDeleteView(DestroyAPIView):
    serializer_class = ParentUpdateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = 'pk'


class LibrarianDeleteView(DestroyAPIView):
    serializer_class = LibrarianInfoSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    lookup_field = 'pk'

# ---------------------------Lists-------------------



class TeacherListView(ListAPIView):
    permission_classes = (IsSchoolAdmin,)
    serializer_class = TeacherListSerializer
    queryset = TeacherProfile.objects.all()
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['user__username','user__email']
    ordering_fields = ['user__username',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        teacher = TeacherProfile.objects.filter(user__school_id=user.school.id)
        return teacher


class AllTeacherListView(ListAPIView):
    "suds"
    permission_classes = (IsNagarAdmin | IsSchoolAdmin,)
    serializer_class = TeacherListSerializer
    queryset = TeacherProfile.objects.all()
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['user__username','user__email']
    ordering_fields = ['user__username',]

    def get_queryset(self):
        user = self.request.user
        try:
            teacher = TeacherProfile.objects.filter(user__school_id=user.school.id)
            return teacher
        except:
            school = self.request.query_params.get('school_id')
            teacher = TeacherProfile.objects.filter(user__school_id=school)
            return teacher



class StudentListView(ListAPIView):
    permission_classes = (IsSchoolAdmin,)
    serializer_class = StudentListSerializer
    queryset = StudentProfile.objects.all()
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['user__username','grade',]
    ordering_fields = ['user__username','grade',]


    def get_queryset(self):
        user = self.request.user
        student = StudentProfile.objects.filter(user__school_id=user.school.id)
        return student


class ParentListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ParentListSerializer
    queryset = User.objects.filter(user_type='Parent')
    pagination_class = SchoolPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = {
        'first_name': ['contains'],
        'last_name': ['contains'],

    }

    def get(self, request):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            print(user)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        parent = User.objects.filter(school=user)
        serializer = ParentListSerializer(parent, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StaffListSerializer
    queryset = StaffProfile.objects.all()
    pagination_class = SchoolPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = {
        'user__first_name': ['contains'],
        'user__last_name': ['contains'],
    }

    def get(self, request):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            print(user)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        staf = StaffProfile.objects.filter(user__school_id=user.id)
        serializer = StaffListSerializer(staf, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LibrarianListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LibrarianListSerializer
    queryset = LibrarianProfile.objects.all()
    pagination_class = SchoolPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = {
        'user__first_name': ['contains'],
        'user__last_name': ['contains'],
    }

    def get(self, request):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            print(user)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        lib = LibrarianProfile.objects.filter(user__school_id=user.id)
        serializer = LibrarianListSerializer(lib, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class GradeListView(ListAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = GradeListSerializer
#     queryset = Subjects.objects.all()
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_fields = {
#         'grade': ['exact'],
#     }

#     def get(self, request):
#         user = self.request.user
#         print(user)
#         if user.is_anonymous:
#             print(user)
#             return Response(status=status.HTTP_401_UNAUTHORIZED)

#         schoool = Subjects.objects.filter(school=user)
#         serializer = GradeListSerializer(schoool, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class GradeDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GradeDetailSerializer
    queryset = Subjects.objects.all()
    # lookup_field='pk'

    def get(self, request, *args, **kwargs):
        grd = kwargs['pk']
        print(grd)
        user = self.request.user
        print(user)
        if user.is_anonymous:
            print(user)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        schoool = Subjects.objects.filter(school=user, grade=grd)
        serializer = GradeDetailSerializer(schoool, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class TeacherDetailView(RetrieveAPIView):
#     # permission_classes=(IsAdminUser,)
#     queryset=User.objects.all()
#     serializer_class=TeacherDetailSerializer
#     lookup_field='pk'


class StudentProfileView(RetrieveAPIView):
    permission_classes = (IsNagarAdmin|IsSchoolAdmin|IsStudent,)
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileViewSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type == 'NA':
            tech = StudentProfile.objects.filter(
                id=kwargs['pk'])
            serializer = StudentProfileViewSerializer(tech, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.user_type == 'SA':
            stdn = StudentProfile.objects.filter(
                id=kwargs['pk'], user__school_id=user.school)
            serializer = StudentProfileViewSerializer(stdn, many=True)
            print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            stdnt = StudentProfile.objects.filter(user=user)
            serializer = StudentProfileViewSerializer(stdnt, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherProfileView(RetrieveAPIView):
    permission_classes = (IsNagarAdmin|IsSchoolAdmin|IsTeacher,)
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileViewSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type == 'NA':
            tech = TeacherProfile.objects.filter(
                id=kwargs['pk'])
            serializer = TeacherProfileViewSerializer(tech, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if user.user_type == 'SA':
            tech = TeacherProfile.objects.filter(
                id=kwargs['pk'], user__school_id=user.school)
            serializer = TeacherProfileViewSerializer(tech, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            tec = TeacherProfile.objects.filter(user=user)
            serializer = TeacherProfileViewSerializer(tec, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class StaffProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileViewSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type == 'SA':
            stf = StaffProfile.objects.filter(
                id=kwargs['pk'], user__school_id=user.id)
            serializer = StaffProfileViewSerializer(stf, many=True)

        else:
            staff = StaffProfile.objects.filter(user=user)
            serializer = StaffProfileViewSerializer(staff, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class LibrarianProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = LibrarianProfile.objects.all()
    serializer_class = LibrarianProfileViewSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type == 'SA':
            stf = LibrarianProfile.objects.filter(
                id=kwargs['pk'], user__school_id=user.id)
            serializer = LibrarianProfileViewSerializer(stf, many=True)

        else:
            staff = LibrarianProfile.objects.filter(user=user)
            serializer = LibrarianProfileViewSerializer(staff, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class SchoolProfileView(RetrieveAPIView):
    permission_classes = (IsNagarAdmin|IsSchoolAdmin,)
    queryset = SchoolProfile.objects.all()
    serializer_class = SchoolProfileViewSerializer

    def get(self, request, *args, **kwargs):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="NA":
            stdn = SchoolProfile.objects.filter(id=kwargs['pk']).first()
            serializer = SchoolProfileViewSerializer(stdn)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            stdnt = SchoolProfile.objects.filter(user_school=user.id).first()
            serializer = SchoolProfileViewSerializer(stdnt)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateTeacherProfilePictureView(RetrieveUpdateAPIView):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfilePictureSerializer
    lookup_field = 'pk'


class DeleteTeacherProfilePictureView(DestroyAPIView):
    serializer_class = TeacherProfilePictureSerializer
    #permission_classes = (IsSchoolAdmin,)
    queryset = TeacherProfile.objects.all()
    lookup_field = 'pk'


class UpdateProfilePictureView(RetrieveUpdateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = ProfilePictureSerializer
    lookup_field = 'pk'


class DeleteProfilePictureView(DestroyAPIView):
    serializer_class = ProfilePictureSerializer
    #permission_classes = (IsSchoolAdmin,)
    queryset = StudentProfile.objects.all()
    lookup_field = 'pk'


class StudentListByGrade(ListAPIView):
    permission_classes = (IsNagarAdmin|IsSchoolAdmin,)
    serializer_class = StudentProfileListViewSerializer
    queryset = StudentProfile.objects.all()
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['user__username','grade',]
    ordering_fields = ['user__username','grade',]


    def get_queryset(self):
        user = self.request.user
        try:
            args = self.request.query_params.get('grade')
            student = StudentProfile.objects.filter(grade=args,user__school_id=user.school.id)
            return student
        except:
            args = self.request.query_params.get('grade')
            school = self.request.query_params.get('school_id')
            student = StudentProfile.objects.filter(grade=args,user__school_id=school)
            return student


class UpdateSchoolProfilePictureView(RetrieveUpdateAPIView):
    queryset = SchoolProfile.objects.all()
    serializer_class = SchoolProfilePictureSerializer
    lookup_field = "pk"


class DeleteSchoolProfilePictureView(DestroyAPIView):
    serializer_class = SchoolProfilePictureSerializer
    #permission_classes = (IsSchoolAdmin,)
    queryset = StudentProfile.objects.all()
    lookup_field = 'pk'


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email = email).exists():
            u = User.objects.get(email=email)
            uid64 = urlsafe_base64_encode(smart_bytes(u.id))
            token = PasswordResetTokenGenerator().make_token(u)
            current_site = settings.FRONTEND_URL
            relative_link = reverse('password_token_check', kwargs={'uidb64': uid64, 'token':token})
            absurl = current_site + relative_link
            email_body = 'Hi there '+u.username+  '\n Use this link to reset your password and try not to forget another time: \n' + absurl
            data = {
                'email_subject': 'Password Reset',
                'email_body': email_body,
                'email_receiver': u.email
            }
            send_reset_password(subject = 'password reset',body = email_body,receiver = u.email)
            return Response({'success': 'We have send you a mail with instructions about changing your password.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'email not registered'},status = status.HTTP_404_NOT_FOUND)


class ResetPasswordTokenCheckView(GenericAPIView):

    serializer_class = SchoolRegisterSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, Please request a new one'}, status= status.HTTP_401_UNAUTHORIZED)

            return Response({'success':True, 'message':'Crendentials Valid', 'uidb64':uidb64, 'token':token, 'username':user.username}, status= status.HTTP_200_OK)


        except DjangoUnicodeDecodeError as identifer:
            return Response({'error': 'Token is not valid, Please send a new one (decode error)'}, status= status.HTTP_401_UNAUTHORIZED)


class NewPasswordView(GenericAPIView):
    serializer_class = NewPasswordSerializers

    def patch(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':'Password Reset completed'}, status= status.HTTP_200_OK)


class StudentClassBulkUpdateView(RetrieveUpdateAPIView):
    serializer_class = StudentProfileListViewSerializer
    queryset = StudentProfile.objects.all()
    lookup_field = 'id'
    #permission_classes = [IsSchoolAdmin,]

    def patch(self, request):
        data = request.data
        #user = self.request.user
        #print(user)
        print(data)
        for i in data:
            data1 = {}
            data1['data1'] = StudentProfile.objects.filter(user__username=i['user'], id=i['id'],user__school_id=self.request.user.school.id ).update(grade= i['grade'])
        status_code = status.HTTP_200_OK
        response = {
            'success': True,
            'message': "Data updated successfully",
            "update": data1
        }
        return Response(response, status=status_code)



class ProfileImageCreateView(CreateAPIView):
    queryset = ImageGallary.objects.all()
    serializer_class = ImageGallarySerializer

    # def post(self, request):
    #     serializer = ImageGallarySerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         if request.user.user_type == 'SA':
    #             serializer.validated_data['school']=request.user.school.id
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileImageListView(ListAPIView):
    queryset = ImageGallary.objects.all()
    serializer_class = ImageGallarySerializer
    def get(self, request):
        if request.user.user_type == 'SA':
            profile_image= ImageGallary.objects.filter(school=self.request.user.school.id)
        elif request.user.user_type == 'NA':
            profile_image= ImageGallary.objects.filter(school=None)
        serializer = ImageGallarySerializer(profile_image,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProfileImageDeleteView(DestroyAPIView):
    queryset = ImageGallary.objects.all()
    serializer_class = ImageGallarySerializer
    lookup_field = "pk"



class PublicProfileImageListView(ListAPIView):
    queryset = ImageGallary.objects.all()
    serializer_class = ImageGallarySerializer

    def get(self, request):
        school_id = self.request.query_params.get('school_id')
        if school_id is not None:
            profile_image= ImageGallary.objects.filter(school=school_id)
            serializer = ImageGallarySerializer(profile_image,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        profile_image= ImageGallary.objects.filter(school=None)
        serializer = ImageGallarySerializer(profile_image,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AboutUsSchoolApiView(RetrieveUpdateAPIView):
    permission_classes = [IsSchoolAdmin,]
    queryset = SchoolProfile.objects.all()
    serializer_class = SchoolAboutUsSerializers
    lookup_field = "pk"

class PublicAboutUsSchoolApiView(ListAPIView):
    serializer_class = SchoolAboutUsSerializers
    queryset = SchoolProfile.objects.all()

    def get(self, request):
        school_id = self.request.query_params.get('school_id')
        if school_id is not None:
            about_us= SchoolProfile.objects.filter(id=school_id)
            serializer = SchoolAboutUsSerializers(about_us,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


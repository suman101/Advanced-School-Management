from grade_and_subject.models import ClassRoutine
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import  ImageGallary, LibrarianProfile, TeacherProfile,StudentProfile,TeacherProfile,StaffProfile,SchoolProfile
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, password_validation
from researchs.models import Subjects
from rest_framework.exceptions import AuthenticationFailed
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import datetime
from django.contrib.auth import get_user_model
User = get_user_model()

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    For login user
    """
    default_error_messages = {
        'no_active_account': 'Username or Password does not matched.'
    }

    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)

        # Add custom claims
        obj=User.objects.get(id=user.id)
        token['role'] = obj.user_type
        token['user'] = user.username
        token['email'] = obj.email
        try:
            token['school']=user.school.school_name
            token['school_id']=user.school.id
        except:
            None
        if user is None:
            raise serializers.ValidationError("User is not registered")
        return token

    def validate(self, attrs):
        #email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')
        try:
            us = User.objects.get(email__iexact=attrs.get("username"))
            username = us.username
        except Exception as e:
            pass
        email = attrs.get('email')
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid Crendential, Try again')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        refresh = self.get_token(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        return {
            'access': access_token,
            'refresh': refresh_token,
        }
    

class SchoolAdminCreateSerializer(serializers.ModelSerializer): 
    """views:
    serialize the school admin while creating"""
    confirm_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    # job_category = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ("id", "email", "password", "confirm_password",'phone_number')

    def validate(self, data):
        data['user_type'] = 'SA'
        data['username'] = data['email'].split('@')[0]
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('passwords should be same')
        return data
    
    def create(user, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user


#----------------------------------Add/Register Schools Teachers Parents Staffs-------------------------------------

class SchoolRegisterSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = SchoolProfile
        fields = ('id', 'school_name', 'school_type', 'phone_number', )

    # def create(self,validated_data):
    #     print(validated_data)
    #     auth_user = User.objects.create_user(**validated_data)
    #     auth_user.is_email_verified = True
    #     auth_user.is_staff = True
    #     auth_user.user_type = "School"
    #     auth_user.save()
    #     return auth_user
        

'''------------------ Teacher Register --------------------------'''
class TeacherRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ("school","email", "username", "dob", "gender","first_name","last_name" ,"password", "confirm_password","phone_number","user_type")

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('passwords should be same')
        data['user_type'] = "TE"
        return data

    def create(user, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user


'''---------------------Student Register-----------------------'''


class StudentProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = "__all__"


class StudentRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ("id","school", "email", "username","dob", "gender","first_name", "last_name",
                  "phone_number", "password", "confirm_password")

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('passwords should be same')
        data['user_type'] = "ST"
        return data

    def create(user, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user


'''----------------------Parent Register---------------------'''

class ParentRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ("school", "email", "username","dob", "gender","first_name", "last_name",
                  "phone_number", "password", "confirm_password")

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('passwords should be same')
        data['user_type'] = "Parent"
        return data

    def create(user, validated_data):
        print(validated_data)
        auth_user = User.objects.create_user(**validated_data)
        auth_user.user_type = "Parent"
        auth_user.save()
        return auth_user

'''------------------------Staff Register-----------------------------'''

class StaffRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ("school", "email", "username","dob", "gender","first_name", "last_name",
                  "phone_number", "password", "confirm_password")

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('passwords should be same')
        data['user_type'] = "Staff"
        return data

    def create(user, validated_data):
        print(validated_data)
        auth_user = User.objects.create_user(**validated_data)
        auth_user.user_type = "Staff"
        auth_user.save()
        return auth_user


'''-----------------------Librarian Register--------------------------'''
class LibrarianRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ("school", "email", "username","dob", "gender","first_name", "last_name",
                  "phone_number", "password", "confirm_password")

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('passwords should be same')
        data['user_type'] = "Librarian"
        return data

    def create(user, validated_data):
        print(validated_data)
        auth_user = User.objects.create_user(**validated_data)
        auth_user.user_type = "Librarian"
        auth_user.save()
        return auth_user



#-------------------------------------Change User Password----------------------------------------------------------

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    retype_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.'))
        return value

    def validate(self, data):
        if data['new_password'] != data['retype_password']:
            raise serializers.ValidationError(
                {'retype_password': _("The two password fields didn't match.")})
        password_validation.validate_password(
            data['new_password'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class PasswordResetSerializers(serializers.Serializer):
    email = serializers.EmailField(max_length=256, min_length=2)

    class Meta:
        fields = ['email']


class NewPasswordSerializers(serializers.Serializer):
    password = serializers.CharField(max_length=68,min_length=2, write_only= True)
    token = serializers.CharField(min_length=1, write_only= True)
    uidb64 = serializers.CharField(min_length=1, write_only= True)

    class Meta:
        fields = ['password','token', 'uidb64']


    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id = id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)

            
#----------------------------------Update User----------------------------------------------------
class UserDetailSerializer(serializers.ModelSerializer):
    """
    this serializer is used for detail of user , by the help
    of this serializer we can view user's first name, last name,
    username, email, phone, usertype and where user's email is
    verified or not
    """
    class Meta:
        model = User
        fields = ['id','username', 'email', 'is_email_verified', 'user_type']



''' In this serializer School info is for getting data field from User model 
and nested in SchoolUpdateSerializer'''

class SchoolInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SchoolProfile
        fields = ("school_name","phone_number",)
#"email","username"

class SchoolUpdateSerializer(serializers.ModelSerializer):
    """views"""
    slug = serializers.ReadOnlyField()
    class Meta:
        model=SchoolProfile
        fields="__all__"
    
    # def update(self, instance, validated_data):
    #     user_data = validated_data.pop('user')
    #     user_serializer = SchoolInfoSerializer()
    #     instance.user.school_name = user_data.get('school_name')
    #     super(self.__class__, self).update(instance,validated_data)
    #     super(SchoolInfoSerializer,user_serializer).update(instance.user,user_data)
    #     return instance
    

''' In this serializer Teacher info is for getting data field from User model 
and nested in TeacherUpdateSerializer'''

class TeacherInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("dob", "gender","first_name", "last_name",
                  "phone_number",)


class TeacherUpdateSerializer(serializers.ModelSerializer):
    user=TeacherInfoSerializer()
    
    class Meta:
        model = TeacherProfile
        fields = ('id',"user","address", "salary", "cv",'religion','joined_date','nationality','experience','caste','department')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = TeacherInfoSerializer()
        super(self.__class__, self).update(instance,validated_data)
        super(TeacherInfoSerializer,user_serializer).update(instance.user,user_data)
        return instance


''' In this serializer Student info is for getting data field from User model 
and nested in StudentUpdateSerializer'''

class StudentInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("dob", "gender","first_name", "last_name",
                  "phone_number",)


class StudentUpdateSerializer(serializers.ModelSerializer):
    user=StudentInfoSerializer()
    class Meta:
        model = StudentProfile
        fields = ('id',"user","address",'grade', "father_name", "mother_name",'admission_date','religion','nationality','caste','roll_number')
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = StudentInfoSerializer()
        super(self.__class__, self).update(instance,validated_data)
        super(StudentInfoSerializer,user_serializer).update(instance.user,user_data)
        return instance





class ParentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("school", "email", "username","dob", "gender","first_name", "last_name",
                  "phone_number",)




''' In this serializer Staff info is for getting data field from User model 
and nested in StaffUpdateSerializer'''
class StaffInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("dob", "gender","first_name", "last_name",
                  "phone_number",)


class StaffUpdateSerializer(serializers.ModelSerializer):
    user=StaffInfoSerializer()
    class Meta:
        model = StaffProfile
        fields = ("user","address", "salary", "cv",)
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = StaffInfoSerializer()
        super(self.__class__, self).update(instance,validated_data)
        super(StaffInfoSerializer,user_serializer).update(instance.user,user_data)
        return instance



''' In this serializer Librarian info is for getting data field from User model 
and nested in LibraryUpdateSerializer'''
class LibrarianInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("dob", "gender","first_name", "last_name",
                  "phone_number",)


class LibrarianUpdateSerializer(serializers.ModelSerializer):
    user=LibrarianInfoSerializer()
    class Meta:
        model = LibrarianProfile
        fields = ("user","address", "salary", "cv",)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = LibrarianInfoSerializer()
        super(self.__class__, self).update(instance,validated_data)
        super(LibrarianInfoSerializer,user_serializer).update(instance.user,user_data)
        return instance



class GradeListSerializer(serializers.ModelSerializer):
    # grade=serializers.SerializerMethodField()
    class Meta:
        model=Subjects
        fields=('id','subject')



class GradeDetailSerializer(serializers.ModelSerializer):
    # subject=serializers.SerializerMethodField()
    # teacher=serializers.SerializerMethodField()
    sub_teacher=serializers.SerializerMethodField()

    class Meta:
        model=Subjects
        fields=('subject','sub_teacher')
    
    def get_sub_teacher(self,obj):
        return TeacherProfile.objects.filter(user=obj.subject_teacher).values('id','first_name','last_name')

    # def get_subject(self,obj):
    #     return Curriculum.objects.filter(grade=obj.id).values('subject')

    # def get_teacher(self,obj):
    #     return Curriculum.objects.filter(grade=obj.id).values('subject_teacher')



class TeacherDetailSerializer(serializers.ModelSerializer):
    grade=serializers.SerializerMethodField()
    # subject=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=("id","email", "username","dob", "gender","first_name", "last_name",
                  "phone_number","grade")

    def get_grade(self,obj):
        grade= Subjects.objects.filter(subject_teacher=obj.id).values('grade','subject')
        return grade
    
#------------------------------Profile-------------------------------------
''' In this serializer SchoolProfileSerializer is for getting data field from User model 
and nested in SchoolProfileViewSerializer to show all data in user profile'''

class SchlProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=(
            "school","email", "username","phone_number",)


class SchoolProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolProfile
        fields = (
            "profile_pic",
        )

class SchoolProfileViewSerializer(serializers.ModelSerializer):
    user_school=serializers.SerializerMethodField()
    class Meta:
        model=SchoolProfile
        fields=('user_school','school_name','slug','school_email','address','school_website','school_type','phone_number','profile_pic')
    
    def get_user_school(self,obj):
        school = User.objects.filter(school=obj.id,user_type="SA").values('username',"email")
        return school        

class ProfileSerializer(serializers.ModelSerializer):
    school=serializers.StringRelatedField()
    class Meta:
        model=User
        fields=("school","email", "username", "phone_number","dob", "gender","first_name","last_name",)

class TeacherProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = (
            "profile_pic",
        )
        

class TeacherProfileViewSerializer(serializers.ModelSerializer):
    user=ProfileSerializer(read_only=True)
    routine_teacher=serializers.SerializerMethodField()
    class Meta:
        model=TeacherProfile
        fields=('id','user','address','salary','cv','religion','department','joined_date','caste','nationality', 'experience',"profile_pic","routine_teacher")
    
    def get_routine_teacher(self,obj):
        print(obj.user)
        a = ClassRoutine.objects.filter(teacher__user=obj.user)
        print(a)
        return ClassRoutine.objects.filter(teacher__user=obj.user).values('grade__grade_name','sub__subject')

class StaffProfileViewSerializer(serializers.ModelSerializer):
    user=ProfileSerializer(read_only=True)
    class Meta:
        model=StaffProfile
        fields=('user','address','salary','cv')


class LibrarianProfileViewSerializer(serializers.ModelSerializer):
    user=ProfileSerializer(read_only=True)
    class Meta:
        model=LibrarianProfile
        fields=('user','address','salary','cv')


class ProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = (
            "profile_pic",
        )

class StudentProfileSerializer(serializers.ModelSerializer):
    school=serializers.StringRelatedField()
    class Meta:
        model=User
        fields=("school","email", "username",
        #"grade",
        "phone_number", "dob", "gender","first_name","last_name",)

class StudentProfileViewSerializer(serializers.ModelSerializer):
    user=StudentProfileSerializer(read_only=True)

    class Meta:
        model=StudentProfile
        fields=('id','user','address','father_name','mother_name','grade','admission_date','roll_number','religion','caste', "profile_pic")


class StudentProfileListViewSerializer(serializers.ModelSerializer):
    user=StudentProfileSerializer(read_only=True)

    class Meta:
        model=StudentProfile
        fields=('id','user','grade',)


#---------------------------------Lists--------------------------------------------


class SchoolSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('school_name','phone_number','email')


class SchoolListSerializer(serializers.ModelSerializer):
    class Meta:
        model=SchoolProfile
        fields=('id','school_name','address','phone_number','school_type','slug', 'profile_pic')


class StudentSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('first_name','last_name')


class StudentListSerializer(serializers.ModelSerializer):
    # user=StudentSearchSerializer(read_only=True)
    username = serializers.CharField(source = "user.username")
    email = serializers.CharField(source = "user.email")
    phone_number = serializers.CharField(source = "user.phone_number")
    user_id = serializers.CharField(source = "user.id")
    class Meta:
        model=StudentProfile
        fields=('id','username','email','phone_number','grade','user_id')


class TeacherBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','email','phone_number')


class TeacherListSerializer(serializers.ModelSerializer):
    # user=TeacherBasicInfoSerializer(read_only=True)
    username = serializers.CharField(source = "user.username")
    email = serializers.CharField(source = "user.email")
    phone_number = serializers.CharField(source = "user.phone_number")
    user_id = serializers.CharField(source = "user.id")
    class Meta:
        model=TeacherProfile
        fields=('id',"user_id","username","email","phone_number")

class LibrarianListSerializer(serializers.ModelSerializer):
    user=TeacherBasicInfoSerializer(read_only=True)
    class Meta:
        model=LibrarianProfile
        fields=('id',"user",)



class StaffListSerializer(serializers.ModelSerializer):
    user=TeacherBasicInfoSerializer(read_only=True)
    class Meta:
        model=StaffProfile
        fields=('id',"user",)


class ParentListSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id',"first_name", "last_name",)

from django.db.models import Count

class CasteReligionCountSerializer(serializers.ModelSerializer):
    caste = serializers.SerializerMethodField()
    religion = serializers.SerializerMethodField()
    class Meta:
        model = SchoolProfile
        fields = (
            'school_name',
            'caste',
            'religion',  
        )

    def get_caste(self, obj):
        caste = StudentProfile.objects.filter(user__school__school_name=obj.school_name).values('caste').annotate(count=Count('caste'))
        return caste
    

    def get_religion(self, obj):
        religion = StudentProfile.objects.filter(user__school__school_name=obj.school_name).values('religion').annotate(count=Count('religion'))
        return religion


class SchoolCasteReligionCountSerializer(serializers.ModelSerializer):
    # caste = serializers.SerializerMethodField()
    # religion = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    class Meta:
        model = SchoolProfile
        fields = (
            'school_name',
            'grade',
            # 'caste',
            # 'religion', 
        )

    # def get_caste(self, obj):
    #     caste = StudentProfile.objects.values('caste').annotate(count=Count('caste'))
    #     return caste
    

    # def get_religion(self, obj):
    #     religion = StudentProfile.objects.values('religion').annotate(count=Count('caste'))
    #     return religion
    
    def get_grade(self, obj):
        print(obj)
        grade = StudentProfile.objects.filter(user__school__school_name=obj.school_name).values('grade').distinct().order_by('-grade')
        caste = StudentProfile.objects.filter(user__school__school_name=obj.school_name).values('grade','caste').annotate(count=Count('caste'))
        religion = StudentProfile.objects.filter(user__school__school_name=obj.school_name).values('grade','religion').annotate(count=Count('caste'))

        for i in grade:
            print(grade)
            grade_list = []
            grade_list.append({'grade':grade})
        
        return grade_list



class ImageGallarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageGallary
        fields = (
            'id',
            'school',
            'image'
        )


class SchoolAboutUsSerializers(serializers.ModelSerializer):
    class Meta:
        model = SchoolProfile
        fields = (
            'id',
            'about_us',
        )
        read_only_fields = (
            'school',
        )


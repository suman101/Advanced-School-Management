from grade_and_subject.models import ClassRoutine, Subjects, Grade
from rest_framework import serializers


class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subjects
        fields=('subject',)


class SubjectsListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subjects
        fields=('id','subject','created_at')


class SubjectsUpdateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Subjects
        fields=('id','subject',)


class SubjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subjects
        fields=('id','subject','created_at')


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Grade
        fields=('grade_name','section','subject','admission_fee','monthly_fee','extra_fee')


class GradeListSerializer(serializers.ModelSerializer):
    subject= serializers.StringRelatedField(many = True)  
    class Meta:
        model=Grade
        fields=('id','grade_name','section','subject', 'created_at','admission_fee','monthly_fee','extra_fee')


class GradeDetailSerializer(serializers.ModelSerializer):
    subject= serializers.StringRelatedField()
    class Meta:
        model=Grade
        fields=('id','grade_name','section','subject', 'created_at','admission_fee','monthly_fee','extra_fee')


class GradeUpdateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Grade
        fields=('id','grade_name','section','subject', 'admission_fee','monthly_fee','extra_fee')


class GradeSubjectListSerializer(serializers.ModelSerializer):
    subject= serializers.StringRelatedField(many = True)
    class Meta:
        model=Grade
        fields=('id','grade_name','subject')


class ClassRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model=ClassRoutine
        fields=('school','teacher','grade','sub','time')


class ClassRoutineListSerializer(serializers.ModelSerializer):
    teacher=serializers.StringRelatedField()
    sub= serializers.StringRelatedField()
    grade= serializers.StringRelatedField()
    school=serializers.StringRelatedField()   
    class Meta:
        model=ClassRoutine
        fields=('id','school','teacher','grade','sub','time')


class ClassRoutineUpdateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=ClassRoutine
        fields=('id','school','teacher','grade','sub','time')


class ClassRoutineDetailSerializer(serializers.ModelSerializer):
    sub= serializers.StringRelatedField()
    grade= serializers.StringRelatedField()
    teacher=serializers.StringRelatedField()
    school=serializers.StringRelatedField()
    class Meta:
        model=ClassRoutine
        fields=('id','school','teacher','grade','sub','time')

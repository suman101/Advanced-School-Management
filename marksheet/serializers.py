from itertools import count, groupby
from authentication.models import StudentProfile
from grade_and_subject.models import Grade, Subjects
from rest_framework import serializers
from .models import Exam, Marks, Marksheet


class ExamCreateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Exam
        fields=('school','title','routine','start_date')


class ExamListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Exam
        fields=('id','title','routine','start_date')


class ExamUpdateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Exam
        fields=('id','title','routine','start_date')


class ExamDetailSerializer(serializers.ModelSerializer):
    school=serializers.StringRelatedField()  
    class Meta:
        model=Exam
        fields=('id','school','title','routine','start_date')


class MarksheetCreateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Marksheet
        fields=('id','exam','grade','file')        



class MarksheetListSerializer(serializers.ModelSerializer):
    exam=serializers.StringRelatedField()
    grade=serializers.StringRelatedField()
    exam_start_date = serializers.CharField(source = 'exam.start_date')

    class Meta:
        model=Marksheet
        fields=('id','exam','exam_id','grade','grade_id','exam_start_date','created_at')



class MarksheetUpdateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Marksheet
        fields=('id','exam','grade','file')


class MarksheetDetailSerializer(serializers.ModelSerializer):
    exam=serializers.StringRelatedField()
    grade=serializers.StringRelatedField()  
    class Meta:
        model=Marksheet
        fields=('id','exam','grade','file')


class MarkCreateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Marks
        fields=('marksheet','student','sub','obtain_mark','full_mark')


class MarkListSerializer(serializers.ModelSerializer):
    # marksheet=serializers.StringRelatedField()
    # student=serializers.StringRelatedField()  
    sub=serializers.StringRelatedField()
    class Meta:
        model=Marks
        fields=('id','marksheet','student','sub','obtain_mark','full_mark')
        depth = 1


class MarkUpdateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Marks
        fields=('id','marksheet','student','sub','obtain_mark','full_mark')


class MarkDetailSerializer(serializers.ModelSerializer):
    marksheet=serializers.StringRelatedField()
    student=serializers.StringRelatedField()  
    sub=serializers.StringRelatedField()  
    class Meta:
        model=Marks
        fields=('id','marksheet','student','sub','obtain_mark','full_mark')


class FileUploadSerializer(serializers.Serializer):
  file = serializers.FileField()

class OnlyMarkSerializer(serializers.ModelSerializer): 
    sub = serializers.StringRelatedField()
    class Meta:
        model=Marks
        fields=('id','sub','obtain_mark','full_mark')

from django.db.models import Sum,Count
class MarkGradeListSerializer(serializers.ModelSerializer): 
    sub=serializers.StringRelatedField()
    class Meta:
        model=Marks
        fields=('id','marksheet','student','sub','obtain_mark','full_mark')

class MarksheetDetails(serializers.ModelSerializer):
    exam=serializers.StringRelatedField()
    grade=serializers.CharField(source = 'grade.grade_name')
    # mark_marksheet =  MarkGradeListSerializer(many=True, read_only=True)
    mark_marksheet = serializers.SerializerMethodField()
    school_info = serializers.SerializerMethodField()
    
    class Meta:
        model=Marksheet
        fields=('id','exam','exam_id','grade','mark_marksheet','school_info' )
    
    def get_mark_marksheet(self,obj):
        print('marksheet')
        INFO = Marks.objects.filter(marksheet = obj.id).values('id','student','sub','obtain_mark','full_mark')
        # define a fuction for key
        def key_func(k):
            return k['student']
        
        # sort INFO data by 'company' key.
        INFO = sorted(INFO, key=key_func)
        l = []
        for key, value in groupby(INFO, key_func):
            l.append({'student':key,'marks':list(value)})
            print(key)
            print(list(value))
        return l
        
    def get_school_info(self,obj):
        try:
            return obj.exam.school.school_name
        except:
            return None


class MarkForNagarAndSchool(serializers.ModelSerializer):
    exam=serializers.StringRelatedField()
    #grade=serializers.CharField(source = 'grade.grade_name')
    #mark_marksheet = serializers.SerializerMethodField()
    #exam = serializers.SerializerMethodField()
    school_info = serializers.SerializerMethodField()
    
    class Meta:
        model=Marksheet
        fields=('id','school_info','exam',
        
        )
    def get_school_info(self,obj):
        try:
            return obj.exam.school.school_name
        except:
            return None
    # def get_exam(self,obj):
    #     print(obj)
    #     fail = Marks.objects.values('marksheet__exam__title').distinct()

    #     for i in Marks.objects.filter(marksheet__exam=obj.exam).distinct():
    #         for j in Marks.objects.filter(marksheet__grade = i.grade).distinct():
                
    #         pass
    #     pa = Marks.objects.filter(obtain_mark__gt=0,marksheet__exam=obj.exam).values('obtain_mark',).annotate(total=Count('obtain_mark')).order_by('student')
    #     print(fail)
    #     print(pa)
    #     INFO = Marksheet.objects.all().values('grade','exam')
    
    #     # # define a fuction for key
    #     def key_func(k):
    #         return k['grade']
    #     # # sort INFO data by 'grade' key.
    #     #INFO = sorted(INFO, key=key_func)
    #     l = []
    #     for key, value in groupby(INFO, key_func):
    #     #for i in l:
    #         l.append({'grade':key,'pass':pa,'fail':fail,'avg_gpa':'list(value)'})
    #     #     # print(key)
    #     #     # print(list(value))
    #     return fail
        
    
        
        
    # def get_total_full_mark(self,obj):
    #     try:
    #         a = Marks.objects.filter(marksheet__exam=obj.marksheet.exam).aggregate(Sum('full_mark'))['full_mark__sum']
    #         return a
    #     except Exception as e:
    #         return None

    # def get_total_full_mark(self,obj):
    #     try:
    #         a = Marks.objects.filter(marksheet__exam=obj.exam)
    #         print(a)
    #         instances = []
    #         for i in a:
    #             instances.append(i.full_mark)
    #         return sum(instances)
    #     except:
    #         return None

    # def get_total_obtain_mark(self,obj):
    #     a = Marks.objects.filter(student=obj.id)
    #     try:
    #         a = Marks.objects.filter(student__id=obj.student.id, marksheet__exam=obj.exam)
    #         instances = []
    #         for i in a:
    #             if i.obtain_mark < i.pass_mark:
    #                 ab = "F"
    #                 return ab
    #             instances.append(i.obtain_mark)

    #         return sum(instances)
    #     except:
    #         return None

    # def get_total_percentage(self,obj):
    #     try:
    #         a = Marks.objects.filter(student__id=obj.student.id, marksheet__exam=obj.exam)
    #         obm = []
    #         fm = []
    #         for i in a:
    #             if i.obtain_mark < i.pass_mark:
    #                 ab = "F"
    #                 return ab
    #             obm.append(i.obtain_mark)
    #             fm.append(i.full_mark)
    #         ob_m = sum(obm)
    #         fu_m = sum(fm)
    #         percentage = (ob_m*100)/fu_m
    #         return percentage
    #     except:
    #         return None

    # def get_pass_or_fail(self,obj):
    #     try:
    #         a = Marks.objects.filter(student__id=obj.student.id, marksheet__exam=obj.exam)
    #         for i in a:
    #             if i.obtain_mark >= i.pass_mark:
    #                 ab = "P"
    #             else:
    #                 ab = "F"
    #         return ab 
    #     except:
    #         return None

    # def get_number_of_fail(self,obj):
    #     try: 
    #         a = Marks.objects.filter(student__id=obj.student.id, marksheet__exam=obj.exam)
    #         b = 0
    #         for i in a:
    #             if i.obtain_mark < i.pass_mark:
    #                 b = b+1
    #         return b
    #     except:
    #         return None
    
    

    # def get_total_obtain_mark(self,obj):
    #     try:
    #         a = Marks.objects.filter(student=obj.student, marksheet__exam=obj.marksheet.exam).aggregate(Sum('obtain_mark'))['obtain_mark__sum']
    #         return a
    #     except Exception as e:
    #         return None

    # def get_total_percentage(self,obj):
    #     try:
    #         om = self.get_total_obtain_mark(obj) if self.get_total_obtain_mark(obj) else 0
    #         fm = self.get_total_full_mark(obj) if self.get_total_full_mark(obj) else 0
    #         percentage = (om/fm)*100
    #         return percentage
    #     except:
    #         return None

    # def get_pass_or_fail(self,obj):
    #     try:
    #         a = Marks.objects.filter(student=obj.student, marksheet__exam=obj.marksheet.exam)
    #         for i in a:
    #             if i.obtain_mark < i.pass_mark:
    #                 ab = "F"
    #         return ab
    #     except:
    #         return None

    # def get_number_of_fail(self,obj):
    #     try: 
    #         a = Marks.objects.filter(student=obj.student, marksheet__exam=obj.marksheet.exam)
    #         b = 0
    #         for i in a:
    #             if i.obtain_mark < i.pass_mark:
    #                 b = b+1
    #         return b
    #     except:
    #         return None
from rest_framework import serializers
from .models import AnswerSheet, AttemptedQuiz, Quiz, Questions, ShortAnswerSheet, ShortQuestion

    

class QuizCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Quiz
        fields = ('sub', 'grade', "teacher", "title", "description", "total_question", "publish", "quiz_duration", "published_date", "created_at", "updated_at")
    

class QuizListSerializer(serializers.ModelSerializer):
    grade =serializers.StringRelatedField()
    sub= serializers.StringRelatedField()
    teacher= serializers.StringRelatedField()
    #total_marks = serializers.SerializerMethodField(default=0)
    class Meta:
        model = Quiz
        fields = ("id","sub",'grade',"teacher","title", "description", "total_question", "publish", "quiz_duration", "published_date", "created_at","updated_at")
        depth  = 2
    
    # def get_total_marks(self, obj):
    #     q1=Questions.objects.filter(quiz=obj.id).count()
    #     if Questions.exists() or ShortQuestion.exists():
    #         total_marks = q1
    #         return total_marks


class QuizUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ("id","sub",'grade',"title", "description", "total_question", "publish", "quiz_duration", "published_date", "created_at","updated_at")
        # depth  = 2
    


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta : 
        model = Questions
        fields = ("question","option1","option2", "option3", "option4", "answer", "description", "quiz", "updated_at")



class QuestionListSerializer(serializers.ModelSerializer):
    sub= serializers.StringRelatedField()
    teacher= serializers.StringRelatedField()
    class Meta : 
        model = Questions
        fields = ("id","sub","teacher", "question","option1","option2", "option3", "option4", "answer", "description", "quiz", "created_at","updated_at")
        #depth = 1

class QuizDetailSerializer(serializers.ModelSerializer):
    question_quiz = QuestionListSerializer(many=True, read_only=True)
    grade =serializers.StringRelatedField()
    sub= serializers.StringRelatedField()
    teacher= serializers.StringRelatedField()
    class Meta:
        model = Quiz
        fields = ("id","sub",'grade',"teacher","title", "description", "total_question", "publish", "quiz_duration", "published_date","created_at","updated_at",'question_quiz',)
        #depth  = 2

class StdQuestionListSerializer(serializers.ModelSerializer):
    sub= serializers.StringRelatedField()
    teacher= serializers.StringRelatedField()
    class Meta : 
        model = Questions
        fields = ("id","sub","teacher","question","option1","option2", "option3", "option4", "quiz")
        depth = 1


class ResultQuizSerializer(serializers.ModelSerializer):
    attended_users = serializers.SerializerMethodField()
    sub= serializers.StringRelatedField()
    teacher= serializers.StringRelatedField()
    class Meta:
        model = Quiz
        fields = ("id","sub",'grade',"teacher","title", "publish", "quiz_duration", "published_date", "created_at","attended_users",
        )
        # depth  = 1
    # def get_total_obtain_marks(self,obj):
    #     pass

    def get_attended_users(self,obj):
        ls = []
        for user in obj.attended_users.all():
            l={}
            q = Questions.objects.filter(quiz=obj.id)
            aq=0
            for i in q:
                try:
                    u = AnswerSheet.objects.get(user_id=user.id,question =i.id)
                    if u.user_answer == i.answer:
                        aq = aq + 1
                except Exception as e:
                    print(e)
                    pass
            l['student']=user.user.username
            l['marks']=aq
            ls.append(l)
        return ls


class AtQuizCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttemptedQuiz
        fields = (
            "user",
            "quiz",
            "mark_obtain",
            "created_at",
        )


class AttemptedQuizCreateSerializer(serializers.ModelSerializer):
    mark_obtain = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only = True)
    user = serializers.StringRelatedField()
    class Meta:
        model = AttemptedQuiz
        fields = (
            "user",
            "quiz",
            "mark_obtain",
            "created_at",
        )
    def get_mark_obtain(self,obj):
      
        q = Questions.objects.filter(quiz=obj.quiz)
        print(q)
        aq=0
        for i in q:
            try:
                u = AnswerSheet.objects.get(user_id=obj.user.id,question =i.id)
                print(u)
                if u.user_answer == i.answer:
                    print('true')
                    aq = aq + 1
                else:
                    print('false')
            except Exception as e:
                print(e)
                pass
                print(aq)
        # l['student']=user.user.username
        # l['marks']=aq
        # ls.append(l)
        return aq


class AttemptedQuizListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = 'user.username')
    email = serializers.CharField(source = 'user.email')
    quiz_grade = serializers.CharField(source = 'quiz.grade')
    quiz_sub = serializers.CharField(source = 'quiz.sub')
    quiz_title = serializers.CharField(source = 'quiz.title')
    quiz_id = serializers.CharField(source = 'quiz.id')
    quiz_description = serializers.CharField(source = 'quiz.description')
    quiz_duration = serializers.CharField(source = 'quiz.quiz_duration')
    class Meta:
        model = AttemptedQuiz
        fields = ("user","email","quiz_grade","quiz_sub","quiz_id","quiz_title","quiz_description","quiz_duration","mark_obtain","created_at","updated_at")
        depth = 2


class AnswerSheetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerSheet
        fields = ("id",
            "user_id",
            "question",
            "user_answer"
        )

class AnswerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerSheet
        fields = ["id",
            "user_id",
            "question",
            "user_answer"]
        depth = 2



#ShortQuestion
class ShortQuestionCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShortQuestion
        fields = ('sub','grade',"teacher","question", "answer",'mark',"created_at", "updated_at",)


class ShortQuestionListSerializer(serializers.ModelSerializer):
    grade = serializers.StringRelatedField()
    sub= serializers.StringRelatedField()
    teacher= serializers.StringRelatedField()
    class Meta:
        model = ShortQuestion
        fields = ("id",'sub','grade',"teacher","question", "answer",'mark',"created_at", "updated_at")
        depth  = 2


class ShortQuestionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortQuestion
        fields = ("id",'sub','grade',"teacher","question", "answer",'mark',"created_at", "updated_at")
        # depth  = 2


class ShortAnswerSheetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortAnswerSheet
        fields = (
            "id",
            "user_id",
            "short_question",
            "user_answer",
            "answer_file"
        )

class ShortAnswerSheetListSerializer(serializers.ModelSerializer):
    short_question = serializers.StringRelatedField()
    user_id = serializers.StringRelatedField()
    grade = serializers.CharField(source = 'short_question.grade')
    sub = serializers.CharField(source = 'short_question.sub')
    class Meta:
        model = ShortAnswerSheet
        fields = (
            "id",
            "user_id",
            "short_question",
            "user_answer",
            'grade',
            'sub',
            "answer_file",
            'mark_ob',
            'created_at'
            )
        # depth  = 2


class ShortAnswerSheetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortAnswerSheet
        fields = (
            "id",
            "user_id",
            "short_question",
            "user_answer",
            'answer_file',
            'mark_ob',
            )
        # depth  = 2

class ShortQuestionAnswerDetailList(serializers.ModelSerializer):
    sub = serializers.StringRelatedField()
    grade = serializers.StringRelatedField()
    teacher = serializers.StringRelatedField()
    shortquestionanswer = ShortAnswerSheetListSerializer(many=True, read_only=True)
    class Meta:
        model = ShortQuestion
        fields = (
            "id",
            'sub',
            'grade',
            "teacher",
            "question",
            "mark",
            "created_at",
            "updated_at",
            "shortquestionanswer",
            )
        
    
from rest_framework import serializers
from .models import *


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id','title', 'detail_notice','pdf', 'published_date','school','is_public']


class NagarNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id','title', 'detail_notice','pdf', 'published_date','is_public']
    

class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id','title', 'detail_notice','pdf', 'published_date','is_public']

#class FeedbackSerializer(serializers.ModelSerializer):
    #class Meta:
        #model = Feedback
        #fields = ['title', 'school', 'message','sended_on']


#class StudentFeedbackSerializer(serializers.ModelSerializer):
    #class Meta:
        #model = StudentFeedback
        #fields = ['title', 'student', 'message','sended_on']


#class EventSerializer(serializers.ModelSerializer):
    #class Meta:
        #model = Event
        #fields = ['title','posted_by','description','date_of_event','updated_on']
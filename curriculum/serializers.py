from .models import Curriculum
from rest_framework import serializers

class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = ['title','pdf','is_published','posted_by']


class CurriculumListSerializer(serializers.ModelSerializer):
    posted_by = serializers.StringRelatedField()
    class Meta:
        model = Curriculum
        fields = ['id','title','pdf','is_published','posted_by']
from email.policy import default
from rest_framework import serializers
from .models import StudyMaterial


class StudyMaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = ['id','title','published_by','publish','created_at','short_description','slug', 'link', 'pdf']



class StudyMaterialSerializer(serializers.ModelSerializer):
    approved = serializers.BooleanField(default=True)
    class Meta:
        model = StudyMaterial
        fields = "__all__"
from rest_framework import serializers
from .models import Category, ResearchDetail,Subjects

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug']


class ResearchListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = ResearchDetail
        fields = ['id','title','published_by','publish','created_at','pdf','category','slug']



class ResearchDetailSerializer(serializers.ModelSerializer):
    approved = serializers.BooleanField(default=True)
    class Meta:
        model = ResearchDetail
        fields = "__all__"

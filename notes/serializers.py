from .models import Notes
from rest_framework import serializers


class NoteCreateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Notes
        fields=('title','teacher','sub','grade','notes_pdf')


class NoteListSerializer(serializers.ModelSerializer):
    grade=serializers.StringRelatedField()
    sub=serializers.StringRelatedField()
    teacher=serializers.StringRelatedField()   
    class Meta:
        model=Notes
        fields=('id','title','teacher','grade','sub','notes_pdf')


class SubjectListSerializer(serializers.ModelSerializer):
    sub=serializers.StringRelatedField()
    class Meta:
        model=Notes
        fields=('id','title','sub','grade','notes_pdf')


class NoteUpdateSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Notes
        fields=('id','title','sub','grade','notes_pdf')


class NoteDetailSerializer(serializers.ModelSerializer):
    grade=serializers.StringRelatedField()
    sub=serializers.StringRelatedField()
    teacher=serializers.StringRelatedField()   
    class Meta:
        model=Notes
        fields=('id','title','teacher','sub','grade','notes_pdf')

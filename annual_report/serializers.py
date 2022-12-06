from .models import Report
from rest_framework import serializers

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['school','grade','exam','file']


class ReportUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id','school','grade','exam','file']


class ReportListSerializer(serializers.ModelSerializer):
    grade = serializers.StringRelatedField()
    school = serializers.StringRelatedField()
    exam = serializers.StringRelatedField()
    class Meta:
        model = Report
        fields = ['id','school','grade','exam','file']
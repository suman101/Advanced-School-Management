from django.shortcuts import render
from custom_settings.paginations import SchoolPagination
from custom_settings.permissions import IsNagarAdmin, IsSchoolAdmin
from rest_framework.generics import (GenericAPIView, RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView,
ListAPIView,CreateAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView)
from study_material.models import StudyMaterial
from study_material.serializers import StudyMaterialListSerializer, StudyMaterialSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter,OrderingFilter

# Create your views here.


class StudyMaterialListView(ListAPIView):
    """suds"""
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialListSerializer

class PublishedStudyMaterialListView(ListAPIView):
    """suds"""

    queryset = StudyMaterial.objects.not_approved()
    serializer_class = StudyMaterialListSerializer
    permission_classes = [IsNagarAdmin | IsSchoolAdmin,]
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['published_by','title']
    ordering_fields = ['title',]

    def get_queryset(self):
        print(self.request.user.school)
        print(self.request.user.user_type)
        print(self.request.user)
        if self.request.user.user_type == 'SA':
            print('owner')
            qs = StudyMaterial.objects.filter(school = self.request.user.school.id,publish = True,approved = False)
        elif self.request.user.user_type == 'NA':
            print(' not owner')

            qs = self.queryset
        return qs


class DraftStudyMaterialListView(ListAPIView):
    """suds"""

    queryset = StudyMaterial.objects.draft()
    serializer_class = StudyMaterialListSerializer
    permission_classes = [IsNagarAdmin | IsSchoolAdmin,]
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['published_by','title']
    ordering_fields = ['title','created_at',]

    def get_queryset(self):
        print(self.request.user.school)
        print(self.request.user.user_type)
        print(self.request.user)
        if self.request.user.user_type == 'SA':
            print('owner')
            qs = StudyMaterial.objects.filter(school = self.request.user.school.id,publish = False)
        elif self.request.user.user_type == 'NA':
            qs = StudyMaterial.objects.filter(school = None,publish = False)
            print(' not owner')

        return qs


class PublicStudyMaterialListView(ListAPIView):
    """suds"""

    queryset = StudyMaterial.objects.public()
    serializer_class = StudyMaterialListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['published_by','title',]
    ordering_fields = ['title','created_at',]


class StudyMaterialCreateView(CreateAPIView):
    """suds"""

    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer
    permission_classes = [IsNagarAdmin | IsSchoolAdmin,]
    
    def post(self, request, *args, **kwargs):
        detail_serializer = StudyMaterialSerializer(data=request.data)
        print(request.user)
        if detail_serializer.is_valid():
            if request.user.user_type == 'SA':
                detail_serializer.validated_data['approved']=False
                detail_serializer.validated_data['school']=request.user.school
            detail_serializer.save()
            return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    
class StudyMaterialDetailView(RetrieveUpdateAPIView):
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer
    lookup_field='slug'

    
class StudyMaterialDeleteView(DestroyAPIView):
    permission_classes = [IsNagarAdmin|IsSchoolAdmin,]
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer
    lookup_field='slug'


class PublicStudyMaterialCardListView(ListAPIView):
    """suds"""

    queryset = StudyMaterial.objects.public()
    serializer_class = StudyMaterialListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['published_by','title',]
    ordering_fields = ['title','-created_at',]
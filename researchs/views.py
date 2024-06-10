from django.shortcuts import render
from rest_framework import generics
from rest_framework.generics import (GenericAPIView, RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView,
ListAPIView,CreateAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView)
from custom_settings.paginations import SchoolPagination

from custom_settings.permissions import IsNagarAdmin, IsSchoolAdmin
from .serializers import CategorySerializer, ResearchDetailSerializer, ResearchListSerializer
from .models import Category, ResearchDetail
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from authentication.models import User
from django.http import QueryDict
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.filters import SearchFilter,OrderingFilter
from django.db.models.deletion import ProtectedError
# Create your views here.
class CategoryListView(generics.ListAPIView):
    """suman -> views"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class CategoryCreateView(generics.CreateAPIView):
    """suman -> views"""
    permission_classes=(IsNagarAdmin,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def post(self, request, *args, **kwargs):
        
        category_serializer = CategorySerializer(data=request.data)
        
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
class CategoryDetailView(generics.RetrieveUpdateAPIView):
    """suman -> views"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field='pk'
    
class CategoryDeleteView(generics.DestroyAPIView):
    """suman -> views"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field='pk'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            data = {'success':'ok'}
            return Response(data, status=status.HTTP_204_NO_CONTENT)
        except ProtectedError as e:
            data = {'protected_error':'The category you wish to delete is used in Research Detail.'}
            return Response(data,status=status.HTTP_403_FORBIDDEN)

        
class ResearchDetailListView(generics.ListAPIView):
    """suman -> views"""
    queryset = ResearchDetail.objects.all()
    serializer_class = ResearchListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title','created_at',]
    permission_classes = [IsNagarAdmin,]


class PublishedResearchDetailListView(generics.ListAPIView):
    """views"""

    queryset = ResearchDetail.objects.not_approved()
    serializer_class = ResearchListSerializer
    permission_classes = [IsNagarAdmin | IsSchoolAdmin,]
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title','created_at',]

    def get_queryset(self):
        if self.request.user.user_type == 'SA':
            print('owner')
            qs = ResearchDetail.objects.filter(school = self.request.user.school.id,publish = True,approved = False)
        elif self.request.user.user_type == 'NA':
            qs = self.queryset
        return qs


class DraftResearchDetailListView(generics.ListAPIView):
    """views"""

    queryset = ResearchDetail.objects.draft()
    serializer_class = ResearchListSerializer
    permission_classes = [IsNagarAdmin | IsSchoolAdmin,]
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title','created_at',]

    def get_queryset(self):
        if self.request.user.user_type == 'SA':
            print('owner')
            qs = ResearchDetail.objects.filter(school = self.request.user.school.id,publish = False)
        elif self.request.user.user_type == 'NA':
            print(' not owner')

            qs = ResearchDetail.objects.filter(school = None,publish = False)

        return qs

class PublicResearchDetailListView(generics.ListAPIView):
    """views"""

    queryset = ResearchDetail.objects.public()
    serializer_class = ResearchListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title','created_at',]


class ResearchDetailCreateView(generics.CreateAPIView):
    """suman -> views"""

    queryset = ResearchDetail.objects.all()
    serializer_class = ResearchDetailSerializer
    permission_classes = [IsNagarAdmin | IsSchoolAdmin,]
    
    def post(self, request, *args, **kwargs):
        print(request.user.user_type)
        print(request.data)
        detail_serializer = ResearchDetailSerializer(data=request.data)
        if detail_serializer.is_valid():
            if request.user.user_type == 'SA':
                print('school')
                detail_serializer.validated_data['approved']=False
                detail_serializer.validated_data['school']=request.user.school
            detail_serializer.save()
            print(detail_serializer.data)
            return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    
class ResearchDetailDetailView(generics.RetrieveUpdateAPIView):
    """suman - >views"""

    queryset = ResearchDetail.objects.all()
    serializer_class = ResearchDetailSerializer
    lookup_field='slug'

    
class ResearchDetailDeleteView(generics.DestroyAPIView):
    """suman - >views"""
    queryset = ResearchDetail.objects.all()
    serializer_class = ResearchDetailSerializer
    permission_classes = [IsNagarAdmin|IsSchoolAdmin,]
    lookup_field='pk'

    
class PublicResearchDetailCardListView(generics.ListAPIView):
    """views"""

    queryset = ResearchDetail.objects.public()
    serializer_class = ResearchListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title','created_at',]


from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import CurriculumListSerializer, CurriculumSerializer
from rest_framework import generics
from .models import Curriculum
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from custom_settings.permissions import IsNagarAdmin, IsSchoolAdmin
from custom_settings.paginations import SchoolPagination
from rest_framework.filters import SearchFilter,OrderingFilter
User = get_user_model()


# Create your views here.]

class CurriculumCreateView(generics.CreateAPIView):
    serializer_class = CurriculumSerializer
    permission_classes = [IsNagarAdmin,]

    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            user_id=user.id
            print(user_id)
            if user and user.user_type=="NA":
                data = {
                    'posted_by': user_id,
                    'title': request.data['title'],
                    'pdf': request.data['pdf'], 
                    'is_published':request.data['is_published']                
                }
                query_dict = QueryDict('', mutable=True)
                query_dict.update(data)
                serializer = CurriculumSerializer(data=query_dict)
                valid = serializer.is_valid(raise_exception=True)
                if valid:
                    serializer.save()
                    status_code = status.HTTP_201_CREATED
                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'Curriculum created successfully',
                        'notice': serializer.data
                    }
            
                    return Response(response, status=status_code)
                else:
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(serializer.errors, status=status_code)
            else:
                response = {
                        'error': "Cannot created, Please Login with Nagar Account"
                    }
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(response, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with Nagar Account")


class CurriculumListView(generics.ListAPIView):
    permission_classes=(IsNagarAdmin,)
    queryset=Curriculum.objects.filter(is_published=True).order_by('-created_at')
    serializer_class=CurriculumListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    pagination_class = SchoolPagination
    search_fields = ['title',]
    ordering_fields = ['title','pdf']


    # def get(self, request):
    #     user = self.request.user
    #     print(user)
    #     if user.is_anonymous:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)

    #     nagar = Curriculum.objects.filter(posted_by=user.nagar)#,grade=user.grade[0]
    #     print(nagar)
    #     serializer =  CurriculumSerializer(nagar ,many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class PublishedCurriculumDetailListView(generics.ListAPIView):
    queryset = Curriculum.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = CurriculumListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title','pdf']


class DraftCurriculumDetailListView(generics.ListAPIView):
    queryset = Curriculum.objects.filter(is_published=False).order_by('-created_at')
    serializer_class = CurriculumListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title','pdf']


class CurriculumDetailView(generics.RetrieveAPIView):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumListSerializer
    lookup_fields = 'pk'

class CurriculumUpdateView(generics.UpdateAPIView):
    permission_classes = [IsNagarAdmin,]
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumListSerializer
    lookup_fields = 'pk'

class CurriculumDeleteView(generics.DestroyAPIView):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumListSerializer
    permission_classes = [IsNagarAdmin,]
    lookup_fields = 'pk'



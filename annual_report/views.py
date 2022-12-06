from django.shortcuts import render
from authentication.models import SchoolProfile, User
from .models import Report
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (GenericAPIView, RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView,
                    ListAPIView,CreateAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView)
from django.http import QueryDict
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .serializers import ReportSerializer, ReportListSerializer, ReportUpdateSerializer
from custom_settings.permissions import IsSchoolAdmin, IsNagarAdmin
from custom_settings.paginations import SchoolPagination
from rest_framework.filters import SearchFilter,OrderingFilter
# Create your views here.



class ReportCreateView(GenericAPIView):
    permission_classes = [IsSchoolAdmin,]
    serializer_class = ReportSerializer
      
    def post(self, request):
        try:
            user = SchoolProfile.objects.get(id=self.request.user.school.id)
            print(user.id)
            user_id=user.id
            data = {
                'school': user_id,
                'grade': request.data['grade'],
                'exam': request.data['exam'],                 
                'file': request.data['file'],                           

            }
            query_dict = QueryDict('', mutable=True)
            query_dict.update(data)
            serializer = ReportSerializer(data=query_dict)
            valid = serializer.is_valid(raise_exception=True)
            if valid:
                serializer.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Result created successfully',
                    'school': serializer.data
                }
        
                return Response(response, status=status_code)
            else:
                status_code = status.HTTP_400_BAD_REQUEST
                return Response(serializer.errors, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with School Account")



class ReportListView(ListAPIView):
    permission_classes=(IsSchoolAdmin|IsNagarAdmin,)
    queryset=Report.objects.all()
    serializer_class=ReportListSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['grade__grade_name','school__school_name',]
    ordering_fields = ['school__school_name','grade__grade_name','exam__title']

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Report.objects.filter(school=user.school.id)
            print(schoool)
            return schoool
        if user.user_type=="NA":
            nagar = Report.objects.all()
            return nagar


# class AllReportListView(ListAPIView):
#     permission_classes=(IsSchoolAdmin|IsNagarAdmin,)
#     queryset=Report.objects.all()
#     serializer_class=ReportListSerializer
#     def get_queryset(self):
#         user = self.request.user
#         print(user)
#         if user.is_anonymous:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         schoool = Report.objects.filter(school=user.school)
#         print(schoool)
#         return schoool


class ReportUpdateView(RetrieveUpdateAPIView):
    serializer_class=ReportUpdateSerializer
    permission_classes=(IsSchoolAdmin,)
    queryset=Report.objects.all()
    lookup_field='pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Report.objects.filter(school=user.school.id)
            print(schoool)
            return schoool


class ReportDeleteView(DestroyAPIView):
    serializer_class=ReportListSerializer
    permission_classes=(IsSchoolAdmin,)
    queryset=Report.objects.all()
    lookup_field='pk'

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.user_type=="SA":
            schoool = Report.objects.filter(school=user.school.id)
            print(schoool)
            return schoool
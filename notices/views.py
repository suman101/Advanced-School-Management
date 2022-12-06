from django.shortcuts import render
from authentication.models import SchoolProfile, User
from .models import Notice #Feedback, Event
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (GenericAPIView, RetrieveUpdateAPIView,RetrieveUpdateDestroyAPIView,
                    ListAPIView,CreateAPIView,UpdateAPIView,RetrieveAPIView,DestroyAPIView)
from django.http import QueryDict
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from notices.serializers import NagarNoticeSerializer, NoticeListSerializer, NoticeSerializer #EventSerializer, FeedbackSerializer 
from custom_settings.permissions import IsSchoolAdmin
from custom_settings.paginations import SchoolPagination
from custom_settings.permissions import IsNagarAdmin
from rest_framework.filters import SearchFilter,OrderingFilter
# Create your views here.



class NoticeCreateView(GenericAPIView):
    permission_classes = [IsNagarAdmin|IsSchoolAdmin,]
    serializer_class = NoticeSerializer
      
    def post(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            if user.user_type=="NA":
                print(user)
                data = {
                    'title': request.data['title'],
                    'detail_notice': request.data['detail_notice'], 
                    'pdf': request.data['pdf'], 
                    'is_public':request.data['is_public'],
                                        
                }
                query_dict = QueryDict('', mutable=True)
                query_dict.update(data)
                serializer = NagarNoticeSerializer(data=query_dict)
                valid = serializer.is_valid(raise_exception=True)
                print("HI")
                if valid:
                    serializer.save()
                    status_code = status.HTTP_201_CREATED
                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'Notice created successfully',
                        'notice': serializer.data
                    }
            
                    return Response(response, status=status_code)
                else:
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(serializer.errors, status=status_code)
            else:
                user = SchoolProfile.objects.get(user_school=self.request.user.id)
                user_id = user.id
                data = {
                    'school': user_id,
                    'title': request.data['title'],
                    'detail_notice': request.data['detail_notice'], 
                    'pdf': request.data['pdf'], 
                    'is_public':request.data['is_public'],
                                        
                }
                query_dict = QueryDict('', mutable=True)
                query_dict.update(data)
                serializer = NoticeSerializer(data=query_dict)
                valid = serializer.is_valid(raise_exception=True)
                if valid:
                    serializer.save()
                    status_code = status.HTTP_201_CREATED
                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'Notice created successfully',
                        'notice': serializer.data
                    }
            
                    return Response(response, status=status_code)
                else:
                    status_code = status.HTTP_400_BAD_REQUEST
                    return Response(serializer.errors, status=status_code)
        except ObjectDoesNotExist:
            raise Http404("Cannot created, Please Login with Authorized Account")



class NoticeListView(ListAPIView):
    queryset=Notice.objects.filter(is_public=True)
    serializer_class=NoticeListSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            teach = Notice.objects.filter(school= None, is_public=True)
            a =teach.union(Notice.objects.filter(is_public=True,school=user.school )).order_by('-id')
            return a


class NoticeDraftListView(ListAPIView):
    permission_classes = [IsNagarAdmin,]
    queryset=Notice.objects.filter(school= None, is_public=False)
    serializer_class=NoticeSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            teach = Notice.objects.filter(school= None, is_public=False)
            return teach


class NoticeSchoolListView(ListAPIView):
    queryset=Notice.objects.filter(is_public=True)
    permission_classes = [IsSchoolAdmin,]
    serializer_class=NoticeSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            teach = Notice.objects.filter(school=user.school.id,is_public=True)
            return teach


class NoticeSchoolDraftListView(ListAPIView):
    permission_classes = [IsSchoolAdmin,]
    queryset=Notice.objects.all()
    serializer_class=NoticeSerializer
    pagination_class = SchoolPagination
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title',]

    def get_queryset(self):
        user = self.request.user
        print(user)
        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            teach = Notice.objects.filter(is_public=False,school=user.school.id)
            return teach


class AllPublicNoticePagiListView(ListAPIView):
    #permission_classes = (IsNagarAdmin,)
    queryset = Notice.objects.filter(is_public=True)
    pagination_class = SchoolPagination
    serializer_class = NoticeSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title',]

    def get_queryset(self):
        school_id = self.request.query_params.get('school_id')
        if school_id is not None:
            notice= Notice.objects.filter(school=school_id,is_public=True).order_by('-id')
            return notice
        notice= Notice.objects.filter(school=None,is_public=True).order_by('-id')
        return notice


class AllPublicNoticesListView(ListAPIView): #without pagination
    permission_classes = (IsNagarAdmin,)
    queryset = Notice.objects.filter(is_public=True)
    serializer_class = NoticeSerializer
    lookup_field = 'pk'
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title',]


class NoticeDetailView(RetrieveAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    lookup_field = 'pk'

class NoticeUpdateView(UpdateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    lookup_field = 'pk'

class NoticeDeleteView(DestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_class = [IsNagarAdmin,]
    lookup_field = 'pk'

class NoticeListDashboard(ListAPIView):
    queryset=Notice.objects.filter(is_public=True,school= None )
    serializer_class = NoticeSerializer
    lookup_field = 'pk'
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['title',]


    #################### not used ##########################


#class EventCreateView(GenericAPIView):
    #serializer_class = EventSerializer

    #def post(self, request):
        #try:
            #user = User.objects.get(id=request.user.id)
            #user_id=user.id
            #if user and user.user_type=="School":
                #user_id = user.id
                #data = {
                    #'school': user_id,
                    #'title': request.data['title'],
                    #'description': request.data['description'],
                    #'date_of_event': request.data['date_of_event'],                
                    #'posted_by': user_id,
                #}
                #query_dict = QueryDict('', mutable=True)
                #query_dict.update(data)
                #serializer = EventSerializer(data=query_dict)
                #valid = serializer.is_valid(raise_exception=True)
                #if valid:
                    #serializer.save()
                    #status_code = status.HTTP_201_CREATED
                    #response = {
                        #'success': True,
                        #'statusCode': status_code,
                        #'message': 'Event created successfully',
                        #'event': serializer.data
                    #}
            
                    #return Response(response, status=status_code)
                #else:
                    #response = {
                            #'error': "please enter a validated data",
                        #}
                    #status_code = status.HTTP_400_BAD_REQUEST
                    #return Response(response, status=status_code)
            #else:
                #response = {
                        #'error': "Cannot created, Please Login with School Account"
                    #}
                #status_code = status.HTTP_400_BAD_REQUEST
                #return Response(response, status=status_code)
        #except ObjectDoesNotExist:
            #raise Http404("Cannot created, Please Login with School Account")


#class EventListView(ListAPIView):
    #permission_classes=(IsAuthenticated,)
    #queryset=Notice.objects.all()
    #serializer_class=EventSerializer

    #def get(self, request):
        #user = self.request.user
        #print(user)
        #if user.is_anonymous:
            #return Response(status=status.HTTP_401_UNAUTHORIZED)

        #schoool = Event.objects.filter(school_id=user.school)#,grade=user.grade[0]
        #print(schoool)
        #serializer =  EventSerializer(schoool ,many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)


#class FeedbackCreateView(GenericAPIView):
    #serializer_class = FeedbackSerializer

    #def post(self, request):
        #try:
            #user = User.objects.get(id=request.user.id)
            #user_id=user.id
            #if user and user.user_type=="School":
                #user_id = user.id
                #data = {
                    #'school': user_id,
                    #'title': request.data['title'],
                    #'message': request.data['message'],
                #}
                #query_dict = QueryDict('', mutable=True)
                #query_dict.update(data)
                #serializer = FeedbackSerializer(data=query_dict)
                #valid = serializer.is_valid(raise_exception=True)
                #if valid:
                    #serializer.save()
                    #status_code = status.HTTP_201_CREATED
                    #response = {
                        #'success': True,
                        #'statusCode': status_code,
                        #'message': 'Feedback created successfully',
                        #'school': serializer.data
                    #}
            
                    #return Response(response, status=status_code)
                #else:
                    #response = {
                            #'error': "please enter a validated data",
                        #}
                    #status_code = status.HTTP_400_BAD_REQUEST
                    #return Response(response, status=status_code)
            #else:
                #response = {
                        #'error': "Cannot created, Please Login with School Account"
                    #}
                #status_code = status.HTTP_400_BAD_REQUEST
                #return Response(response, status=status_code)
        #except ObjectDoesNotExist:
            #raise Http404("Cannot created, Please Login with School Account")


#class FeedbackListAdminView(ListAPIView):
    #permission_classes=[IsAdminUser,]
    #queryset=Feedback.objects.all()
    #serializer_class=FeedbackSerializer

    #def get(self, request):
        #user = self.request.user
        #print(user)
        #if user.is_anonymous:
            #return Response(status=status.HTTP_401_UNAUTHORIZED)
        #if user.is_superuser:
            #feedback = Feedback.objects.all()
            #serializer =  FeedbackSerializer(feedback,many=True)
            #return Response(serializer.data, status=status.HTTP_200_OK)
        #schoool = Feedback.objects.filter(school_id=user.id)
        #serializer =  FeedbackSerializer(schoool,many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)


#class FeedbackListView(ListAPIView):
    #permission_classes=(IsAuthenticated,)
    #queryset=Feedback.objects.all()
    #serializer_class=FeedbackSerializer

    #def get(self, request):
        #user = self.request.user
        #print(user)
        #if user.is_anonymous:
            #return Response(status=status.HTTP_401_UNAUTHORIZED)

        #schoool = Feedback.objects.filter(school_id=user.id)#,grade=user.grade[0]
        #print(schoool)
        #serializer =  FeedbackSerializer(schoool ,many=True)
        #return Response(serializer.data, status=status.HTTP_200_OK)


#class FeedbackUpdateView(UpdateAPIView):
    #permission_classes =[IsAdminUser,]
    #queryset = Feedback.objects.all()
    #serializer_class = FeedbackSerializer
    #lookup_field = 'pk'

    # def get(self, request):
    #     user = self.request.user
    #     print(user)
    #     if user.is_anonymous:
    #         return Response(status=status.HTTP_401_UNAUTHORIZED)

    #     schoool = Feedback.objects.filter(school_id=user.id)#,grade=user.grade[0]
    #     print(schoool)
    #     serializer =  FeedbackSerializer(schoool ,many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    
    #def patch(self, request, pk):
        #user = self.request.user
        #print(user)
        #if user.is_anonymous:
            #return Response(status=status.HTTP_401_UNAUTHORIZED)
        #if Feedback.school_id == user.id:
            #print(Feedback.school_id)
            #print(user.id)
            #feedback = self.get_object(pk)
            #serializer = self.serializer_class(feedback, data=request.data, partial=True)
            #valid = serializer.is_valid()
            #if valid:
                #serializer.save()
                #status_code = status.HTTP_201_CREATED
                #response = {
                    #'success': True,
                    #'message': "feedback has been updated successfully"
                #}
                #return Response(response, status=status_code)
            #else:
                #status_code = status.HTTP_400_BAD_REQUEST
                #response = {
                    #'success': False,
                    #'message': "put correct data"
                #}
                #return Response(response, status=status_code)

# class CategoryDetailDeleteView(DestroyAPIView):
#     serializer_class = FeedbackSerializer
#     lookup_field = 'pk'

#     def delete(self, request, pk):
#         user = self.request.user
#         if user.is_anonymous:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         schoool = Feedback.objects.filter(school_id=user.id)
#         review_and_rating = self.get_object(pk)
#         review_and_rating.delete()
#         status_code = status.HTTP_204_NO_CONTENT
#         response = {
#             'success': True,
#             'message': "ReviewAndRating has been deleted successfully"
#         }
#         return Response(response, status=status_code)

# class ReviewAndRatingUpdateView(GenericAPIView):
#     """
#     to update a feedback
#     """
#     serializer_class = ReviewAndRatingSerializer

#     def get_object(self, pk):
#         try:
#             return ReviewAndRating.objects.get(id=pk)
#         except ReviewAndRating.DoesNotExist:
#             raise serializers.ValidationError(
#                             'ReviewAndRating does not exist')

#     def get(self, request, pk):
#         review_and_rating = self.get_object(pk)
#         serializer = self.serializer_class(review_and_rating)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def patch(self, request, pk):
#         review_and_rating = self.get_object(pk)
#         serializer = self.serializer_class(review_and_rating, data=request.data, partial=True)
#         valid = serializer.is_valid()
#         if valid:
#             serializer.save()
#             status_code = status.HTTP_201_CREATED
#             response = {
#                 'success': True,
#                 'message': "ReviewAndRating has been updated successfully"
#             }
#             return Response(response, status=status_code)
#         else:
#             status_code = status.HTTP_400_BAD_REQUEST
#             response = {
#                 'success': False,
#                 'message': "put correct data"
#             }
#             return Response(response, status=status_code)


# class ReviewAndRatingDeleteView(generics.GenericAPIView):
#     """
#     to delete a review and rating
#     """
#     serializer_class = ReviewAndRatingSerializer

#     def get_object(self, pk):
#         try:
#             return ReviewAndRating.objects.get(id=pk)
#         except ReviewAndRating.DoesNotExist:
#             raise serializers.ValidationError(
#                             'ReviewAndRating does not exist')

#     def get(self, request, pk):
#         review_and_rating = self.get_object(pk)
#         serializer = self.serializer_class(review_and_rating)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def delete(self, request, pk):
#         review_and_rating = self.get_object(pk)
#         review_and_rating.delete()
#         status_code = status.HTTP_204_NO_CONTENT
#         response = {
#             'success': True,
#             'message': "ReviewAndRating has been deleted successfully"
#         }
#         return Response(response, status=status_code)
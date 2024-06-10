from rest_framework import permissions
from django.contrib.auth import get_user_model

from authentication.models import SchoolProfile

User = get_user_model()

class IsNagarAdmin(permissions.BasePermission):
    """"permission class 
    checks either user is nagar admin or not
    """

    def has_permission(self, request, view):
        try:
            return True if request.user.user_type == 'NA' else False
        except:
            return False
            

class IsSchoolAdmin(permissions.BasePermission):
    """"permission class"""
    def has_permission(self, request, view):
        try:
            if request.user.user_type == 'SA':
                return True
        except:
            return False     


class IsTeacher(permissions.BasePermission):
    """"permission class"""
    def has_permission(self, request, view):
        try:
            if request.user.user_type == 'TE':
                return True
        except Exception as e:
            print(e)
            return False


class IsStudent(permissions.BasePermission):
    """"suds"""
    def has_permission(self, request, view):
        try:
            if request.user.user_type == 'ST':
                return True
        except Exception as e:
            print(e)
            return False


class IsOwner(permissions.BasePermission):
    """"suds"""
    def has_object_permission(self, request, view, obj):
        try:
            print(obj)
            return obj.user == self.request.user
        except Exception as e:
            print(e)
            return False
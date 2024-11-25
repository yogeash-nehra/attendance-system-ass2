# from rest_framework import permissions
#
# class IsAdminUser(permissions.BasePermission):
#     """
#     Custom permission to only allow administrators to access certain endpoints.
#     """
#     def has_permission(self, request, view):
#         return request.user and request.user.is_staff
#
# class IsLecturerUser(permissions.BasePermission):
#     """
#     Custom permission to only allow lecturers to access certain endpoints.
#     """
#     def has_permission(self, request, view):
#         return request.user and hasattr(request.user, 'lecturer')
#
# class IsStudentUser(permissions.BasePermission):
#     """
#     Custom permission to only allow students to access certain endpoints.
#     """
#     def has_permission(self, request, view):
#         return request.user and hasattr(request.user, 'student')
from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff  # Assume 'is_staff' is for Admin

class IsLecturerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'lecturer_profile')  # Assuming a `lecturer_profile` attribute

class IsStudentUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and hasattr(request.user, 'student_profile')  # Assuming a `student_profile` attribute

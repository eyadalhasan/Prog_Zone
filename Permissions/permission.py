
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist

class IsSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow superusers to access.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsEmployee(permissions.BasePermission):
    """
    Custom permission to only allow employees of the system to create, update or delete.
    """

    def has_permission(self, request, view):
        
        # Check if the user is an employee
        try:
            request.user.employee
            return True
        except ObjectDoesNotExist:
            return False

class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow employees of the system to create, update or delete.
    """

    def has_permission(self, request, view):
        
        # Check if the user is an employee
        try:
            request.user.is_student()
            return True
        except ObjectDoesNotExist:
            return False

class IsStudentOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow students to read.
    """


    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            try:
               
                x=request.user.is_student()
                
                return x
            
            except ObjectDoesNotExist:
                return False
        # Write permissions are not allowed for students
        return False

class IsRelatedEmployeeOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow employees of a course to edit it.
    Assumes there's a method in the Course model to check this relationship.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        print(f"obj.user==request.user",obj.user==request.user)
        
        return obj.user==request.user
class IsRelatedUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow employees of a course to edit it.
    Assumes there's a method in the Course model to check this relationship.
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        print(f"obj.user==request.user",obj.user==request.user)
        
        return obj.user==request.user

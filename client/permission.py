from rest_framework.permissions import BasePermission

from client.models import SCHOOL_ADMIN

SAFE_METHODS = ['POST', 'HEAD', 'OPTIONS']

class IsAuthenticatedOrPOSTOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """
    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated):
            return True
        return False

class IsOwner(BasePermission):
    def has_object_permission(self, request, view , obj):
        return obj.user.id == request.user.id


PROTECTED_METHODS = ['DELETE']

class IsNonDeleteTeacher(BasePermission):
    message="Could not delete since the teacher is the school's superuser."
    def has_object_permission(self, request, view, obj):
        if (request.method in PROTECTED_METHODS):
            return not obj.role==SCHOOL_ADMIN
        return True

class IsSystemAdmin(BasePermission):
  """
  The request is authenticated as a user, or is a read-only request.
  """

  def has_permission(self, request, view):
    if (request.user.is_authenticated):
      return request.user.role=="A" or request.user.is_superuser
    return False

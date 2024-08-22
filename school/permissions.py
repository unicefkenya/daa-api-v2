from rest_framework.permissions import BasePermission

PROTECTED_METHODS = ['DELETE']

class IsNonDeleteTeacher(BasePermission):
    message="Could not delete since the teacher is the school's superuser."
    def has_object_permission(self, request, view, obj):
        if (request.method in PROTECTED_METHODS):
            return not obj.is_non_delete
        return True



class IsAnEmptySteam(BasePermission):
    message="Move students before attempting to delete the class."
    def has_object_permission(self, request, view, obj):
        if (request.method in PROTECTED_METHODS):
            return obj.students.all().count()==0
        return True

from rest_framework.permissions import BasePermission


class IsTeacherOfTheSchool(BasePermission):

    def has_permission(self, request, view):
        # is_in_group=Group.objects.get(name="teachers").user_set.filter(id=request.user.id)
        # is_in_group=is_in_group.exists()
        if(request.user and request.user.is_authenticated):
            return True
        return False


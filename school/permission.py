from rest_framework.permissions import BasePermission


class IsSchoolAttendant(BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    message="You are not a staff member of the school selected."

    def has_permission(self, request, view):
        if request.method =="POST":
            # print("school ",request.data.get("registered_school"))
            # print(request.user.schools.values_list("id",flat=True))
            return  request.user.schools.filter(id=request.data.get("registered_school")).exists()
        return True


class IsSchoolAttendant2(BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    message="You are not a staff member of the school selected."

    def has_permission(self, request, view):
        if request.method =="POST":
            # print("school ",request.data.get("registered_school"))
            # print(request.user.schools.values_list("id",flat=True))
            return  request.user.schools.filter(id=request.data.get("school")).exists()
        return True
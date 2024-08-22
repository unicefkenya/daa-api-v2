from rest_framework.permissions import BasePermission


class IsRegionAttendant(BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    message="You are not a staff member of the region selected."

    def has_permission(self, request, view):
        if request.method =="POST":
            # print("region ",request.data.get("registered_region"))
            # print(request.user.regions.values_list("id",flat=True))
            return  request.user.regions.filter(id=request.data.get("registered_region")).exists()
        return True


class IsRegionAttendant2(BasePermission):
    """
    Global permission check for blacklisted IPs.
    """
    message="You are not a staff member of the region selected."

    def has_permission(self, request, view):
        if request.method =="POST":
            # print("region ",request.data.get("registered_region"))
            # print(request.user.regions.values_list("id",flat=True))
            return  request.user.regions.filter(id=request.data.get("region")).exists()
        return True
from rest_framework.permissions import IsAuthenticated


class IsOwner(IsAuthenticated):
    """
    Allow only the event's owner to modify it
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner

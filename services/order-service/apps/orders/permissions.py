from rest_framework.permissions import BasePermission



class IsAdminOrSeller(BasePermission):

    def has_permission(self, request, view):
        return request.user and (request.user.role.lower() == 'admin' or request.user.role.lower()=='seller')

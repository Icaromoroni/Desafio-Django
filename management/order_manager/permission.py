from rest_framework.permissions import BasePermission

class IsStaffUser(BasePermission):
    """
    Permissão que permite apenas usuários staff editar informações.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff
        return True
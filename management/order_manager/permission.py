from rest_framework.permissions import BasePermission

class IsStaffUser(BasePermission):
    """
    Permissão que permite apenas usuários staff editar informações.
    """

    def has_permission(self, request, view):
    
        if request.method in ['POST','PUT', 'PATCH', 'DELETE']:
            if not request.user.is_staff:
                return False
        return request.user and request.user.is_authenticated

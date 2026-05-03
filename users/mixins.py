from django.core.exceptions import PermissionDenied


class RoleRequiredMixin:
    role = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.role != self.role:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

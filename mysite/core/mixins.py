from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

class AuthorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != request.user:
            messages.error(request, "У вас нет прав для редактирования этого поста!")
            return redirect('post_detail', pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)
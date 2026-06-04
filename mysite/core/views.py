from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpResponse,
    HttpRequest,
    HttpResponseNotFound,
    HttpResponsePermanentRedirect,
    Http404,
    HttpResponseBadRequest,
)
from django.urls import reverse, reverse_lazy
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.db.models import Avg

from core.mixins import AuthorRequiredMixin
from .models import Comment, Post, CustomUser
from .forms import CustomUserCreationForm, LoginForm, ProfileEditForm, UserCreationForm, PostForm, PostUpdateForm, CommentForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.views import LogoutView as AuthLogoutView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def custom_404(request, exception=None):
    return HttpResponseNotFound("<h1>404 - Страница не найдена</h1>")


def custom_400(request, exception=None):
    return HttpResponseBadRequest("<h1>400 - Неверный запрос</h1>")


class PostListView(ListView):
    model = Post
    template_name = "core/index.html"
    context_object_name = "posts"
    ordering = ["-created_at"]
    
    def get_queryset(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED)

class PostDetailView(DetailView):
    model = Post
    template_name = "core/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context
    
class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "core/post_create.html"
    form_class = PostForm
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    template_name = "core/post_update.html"
    form_class = PostUpdateForm
    model = Post
    success_url = reverse_lazy("home")
    
class AddCommentView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = "core/add_comment.html"
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.instance.post = post
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        comment = form.instance
        
        subject = f"Новый комментарий к вашей записи: {post.title}"
        message = f"Пользователь {self.request.user.username} оставил комментарий: {comment.text}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [post.author.email]
        
        send_mail(subject, message, from_email, recipient_list)
        
        return response
    
    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.kwargs["pk"]})

class AboutView(View):
    def get(self, request):
        return render(request, "core/about.html")

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "core/register.html"
    success_url = reverse_lazy("home")
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.save()
        return super().form_valid(form)

class LoginView(AuthLoginView):
    template_name = "core/login.html"
    success_url = reverse_lazy("home")
    form_class = LoginForm
    
    def form_valid(self, form):
        """Успешный вход"""
        response = super().form_valid(form)
        messages.success(self.request, f"Добро пожаловать, {self.request.user.username}!")
        return response
    
    def form_invalid(self, form):
        """Неудачный вход"""
        messages.error(self.request, "Неверное имя пользователя или пароль.")
        return super().form_invalid(form)

class LogoutView(AuthLogoutView):
    next_page = reverse_lazy("home")


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "core/profile.html"
    context_object_name = "user"
    
    def get_object(self, queryset=None):
        return self.request.user

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileEditForm
    template_name = "core/profile_editing.html"
    success_url = reverse_lazy("profile")
    
    def get_object(self, queryset=None):
        return self.request.user
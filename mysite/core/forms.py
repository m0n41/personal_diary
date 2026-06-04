from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import Comment, CustomUser, Post
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


class CustomUserCreationForm(forms.ModelForm):
    
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        
        if len(username) < 3:
            raise ValidationError('Имя пользователя должно содержать минимум 3 символа.')
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email
    
    def clean_password(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        
        if password1 and len(password1) < 8:
            raise ValidationError("Пароль должен содержать минимум 8 символов")
        
        if password1.isdigit():
            raise ValidationError("Пароль не должен состоять только из цифр")
        
        return password1
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data["password1"]
        password2 = cleaned_data["password2"]
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают.')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        return user
        

class ProfileEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={"class": "form-control-file"}))
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    
    class Meta:
        model = get_user_model()
        fields = ("username", "email", "avatar", "birth_date")
        
    def clean_username(self):
        username = self.cleaned_data["username"]
        if get_user_model().objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Пользователь с таким именем уже существует.')
        
        if len(username) < 3:
            raise ValidationError("Имя пользователя должно содержать мнимум 3 символа")
        
        return username
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        return email
    
    def clean_avatar(self):
        avatar = self.cleaned_data["avatar"]
        if avatar and avatar.size > 2 * 1024 * 1024:
            raise ValidationError("Размер аватара не должен превышать 2 МБ")
        
        if avatar and not avatar.content_type.startswith("image/"):
            raise ValidationError("Загруженный файл должен быть изображением")
        
        return avatar
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise ValidationError("Неверное имя пользователя или пароль.")
        return cleaned_data
    
    def get_user(self):
        return getattr(self, 'user', None)
    
class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
    status = forms.ChoiceField(choices=Post.Status.choices, widget=forms.Select(attrs={"class": "form-control"}))
    
    class Meta:
        model = Post
        fields = ("title", "content", "status")
        
class PostUpdateForm(PostForm):
    pass

class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Ваш комментарий..."}))

    class Meta:
        model = Comment
        fields = ("text",)

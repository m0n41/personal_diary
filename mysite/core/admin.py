from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Comment, CustomUser, Post

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
    
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "content")
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "post", "user", "created_at")
    list_filter = ("created_at",)
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    text_preview.short_description = "Comment"
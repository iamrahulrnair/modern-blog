from django.contrib import admin
from .models import Post, PostComment


# Register your models here.
class PostCommentInline(admin.StackedInline):
    model = PostComment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostCommentInline]

    prepopulated_fields = {
        "slug": ("title", 'time_to_read')
    }


admin.site.register(PostComment)

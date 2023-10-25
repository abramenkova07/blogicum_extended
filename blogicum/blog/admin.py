from django.contrib import admin

from .models import Category, Comment, Location, Post, Tag


admin.site.empty_value_display = 'Не задано'


class PostInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    list_display_links = ('title',)
    search_fields = ('title', 'description')
    inlines = (PostInline,)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    list_display_links = ('name',)
    search_fields = ('name',)
    inlines = (PostInline,)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'is_published')
    list_editable = ('is_published',)
    list_filter = ('author', 'is_published')
    list_display_links = ('title',)
    search_fields = ('title', 'text')
    raw_id_fields = ('author',)
    date_hierarchy = 'pub_date'
    ordering = ('pub_date',)
    filter_horizontal = ('tags',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at', 'author')
    list_filter = ('text', 'author')
    list_display_links = ('text',)
    search_fields = ('text',)
    date_hierarchy = 'created_at'
    ordering = ('created_at',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'slug')
    list_editable = ('slug',)
    list_filter = ('tag',)
    search_fields = ('tag',)
    prepopulated_fields = {'slug': ['tag']}

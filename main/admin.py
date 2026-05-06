from django.contrib import admin
from .models import Category, Photo, Blog, Comment, ContactMessage


admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(Blog)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'blog', 'approved', 'created')
    list_filter = ('approved',)
    search_fields = ('name', 'message')

    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'project_type', 'created')
    search_fields = ('first_name', 'last_name', 'email', 'message')
    list_filter = ('created',)

admin.site.site_header = "Didack Media Admin"
admin.site.site_title = "Didack Media"
admin.site.index_title = "Welcome to Didack Media Dashboard"
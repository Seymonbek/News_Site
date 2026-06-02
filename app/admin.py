from django.contrib import admin
from app.models import News, Category, ContactData, Contact, Comment


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_time']
    list_filter = ['created_time']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_time']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'publish_time', 'status', 'category']
    list_filter = ['status', 'created_time', 'publish_time', 'category']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ['title', 'body']
    ordering = ['-publish_time']
    list_editable = ['status']
    readonly_fields = ['created_time', 'updated_time']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(ContactData)
class ContactDataAdmin(admin.ModelAdmin):
    list_display = ['address', 'phone', 'email']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'body', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['body', 'user__username']
    list_editable = ['active']
    actions = ['disable_comments', 'activate_comments']

    def disable_comments(self, request, queryset):
        queryset.update(active=False)
    disable_comments.short_description = "Tanlangan izohlarni o'chirish"

    def activate_comments(self, request, queryset):
        queryset.update(active=True)
    activate_comments.short_description = "Tanlangan izohlarni faollashtirish"

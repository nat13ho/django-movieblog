from django.contrib import admin

from .models import Post, Category, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'pub_date', 'mod_date', 'category')
    search_fields = ('title', 'content')
    list_filter = ('pub_date', 'category')
    list_display_links = ('id', 'title')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'content', 'post', 'pub_date')
    list_display_links = ('id', 'get_username')
    list_filter = ('pub_date',)
    search_fields = ('content',)

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)

from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'is_subscribed')
    list_display_links = ('id', 'get_username')
    search_fields = ('get_username',)

    def get_username(self, obj):
        return obj.user.username

    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'


admin.site.register(Profile, ProfileAdmin)

from django.contrib import admin
from banner.models import Banner, Activity, FriendLink


class BannerAdmin(admin.ModelAdmin):
    list_display_links = ['name']
    list_display = ['name', 'img_url', 'link']
    list_editable = ['img_url', 'link']


class ActivityAdmin(admin.ModelAdmin):
    list_display_links = ['name']
    list_display = ['name', 'img_url', 'link']
    list_editable = ['img_url', 'link']


class FriendLinkAdmin(admin.ModelAdmin):
    list_display_links = ['name']
    list_display = ['name', 'link']
    list_editable = ['link']

admin.site.register(Banner, BannerAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(FriendLink, FriendLinkAdmin)

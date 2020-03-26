from django.contrib import admin
from community.models import Article, ArticleTag, ArticleClassification


class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ['tag']


class ArticleClassificationAdmin(admin.ModelAdmin):

    list_display = ['classification', 'level', 'icon', 'official']
    list_editable = ['level', 'icon', 'official']

# @admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):

    list_display = ['title', 'created', 'status', 'top', 'essence']
    list_editable = ['status', 'top', 'essence']
    actions = ['set_top', 'set_essence', 'delete_top', 'delete_essence',]

    def set_top(self, request, queryset):
        queryset.update(top=True)

    def set_essence(self, request, queryset):
        queryset.update(essence=True)

    def delete_top(self, request, queryset):
        queryset.update(top=False)

    def delete_essence(self, request, queryset):
        queryset.update(essence=False)

    # 显示的文本，与django admin一致
    set_top.short_description = '置顶'
    set_essence.short_description = '精华'
    delete_top.short_description = '取消置顶'
    delete_essence.short_description = '取消精华'
    # # icon，参考element-ui icon与https://fontawesome.com
    # set_top.icon = 'fas fa-arrow-alt-circle-up'
    # set_essence.icon = 'fas fa-medal'
    #
    # delete_top.icon = 'fas fa-arrow-alt-circle-down'
    # delete_essence.icon = 'far fa-star'
    #
    # set_top.type = 'success'
    # set_essence.type = 'success'
    #
    # delete_top.type = 'warning'
    # delete_essence.type = 'warning'





admin.site.register(ArticleTag, ArticleTagAdmin)
admin.site.register(ArticleClassification,ArticleClassificationAdmin)
admin.site.register(Article, ArticleAdmin)

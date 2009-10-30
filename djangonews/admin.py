from django.contrib import admin

from djangonews import models, widgets, forms

class ImageInline(admin.StackedInline):
    model = models.Image
    extra = 1

class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    list_display = ('title', 'release_date', 'expire_date', 'active', 
        'featured')
    search_fields = ['title', 'body', 'teaser',]
    list_filter = ('release_date', 'expire_date', 'active', 'featured', 
        'categories', 'location')
    prepopulated_fields = {'slug' : ('title',)}
    date_heirarchy = 'release_date'
    fieldsets = (
               (None, {'fields': (('title', 'active', 'featured'), 
                       'categories', 'location', 'teaser', 'body', 
                       ('release_date', 'expire_date'), 'slug')}),
    )
    form = forms.ArticleAdminModelForm

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ['title',]
    prepopulated_fields = {'slug' : ('title',)}
    fieldsets = (
               ('Category', {'fields': ('title', 'slug')}),
    )

admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Category, CategoryAdmin)

################################################################################ 
# Django News: a simple Django-based news application
# Copyright (c) 2009, Imaginary Landscape
# All rights reserved.
#                    
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Imaginary Landscape nor the names of its
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
################################################################################

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

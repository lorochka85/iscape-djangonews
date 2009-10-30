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
from datetime import datetime
from django import http, shortcuts, template
from django.conf import settings
from django.utils import safestring
from django.utils.http import urlencode
from django.core.urlresolvers import reverse
from django.views.generic import date_based
from djangonews import models
from django.core.paginator import Paginator
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def index(request):
    site = Site.objects.get_current()
    featured_list = models.Article.objects.get_featured()
    article_list = models.Article.objects.get_published()
    return shortcuts.render_to_response('djangonews/index.html', locals(),
        context_instance=template.RequestContext(request))

def category_detail(request, slug):
    category = models.Category.objects.get(slug__exact=slug)
    article_list = category.articles.get_published()
    return shortcuts.render_to_response(
        'djangonews/category_detail.html', 
        {'category': category, 'article_list': article_list,},
        context_instance=template.RequestContext(request))        

def article_list(request):
    article_list = models.Article.objects.get_published()

    paginator = Paginator(article_list, 10)
    page = int(request.GET.get('page', '1'))
    article_list = paginator.page(page)

    return shortcuts.render_to_response(
        'djangonews/article_list.html', {'article_list': article_list,},
        context_instance=template.RequestContext(request))

def article_detail(request, year, month, day, slug):
    return date_based.object_detail(
        request,
        year = year,
        month = month,
        day = day,
        date_field = 'release_date',
        slug = slug,
        queryset = models.Article.objects.get_published()
    )

def article_archive_year(request, year):
    return date_based.archive_year(
        request,
        year = year,
        date_field = 'release_date',
        queryset = models.Article.objects.get_published(),
        make_object_list = True,
    )
 
 
def article_archive_month(request, year, month):
    return date_based.archive_month(
        request,
        year = year,
        month = month,
        date_field = 'release_date',
        queryset = models.Article.objects.get_published(),
    )
 
 
def article_archive_day(request, year, month, day):
    return date_based.archive_day(
        request,
        year = year,
        month = month,
        day = day,
        date_field = 'release_date',
        queryset = models.Article.objects.get_published(),
    )

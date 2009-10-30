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
from django.conf.urls.defaults import *
from djangonews.feeds import FeaturedEntries, AllEntries

from djangonews import models 


##Custom 
urlpatterns = patterns(
    'djangonews.views',
    (r'^$', 'index', {}, 'news_index'),
    (r'^articles/$',
     'article_list', None, 'news_article_list'),
    (r'^categories/(?P<slug>[\-\d\w]+)/$',
       'category_detail', None, 'news_category_detail'),
    url(r'^articles/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$', 
        'article_detail', name='news_article_detail'),
    url(r'^articles/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 
        'article_archive_day'),
    url(r'^articles/(?P<year>\d{4})/(?P<month>[a-z]{3})/$', 'article_archive_month'),
    url(r'^articles/(?P<year>\d{4})/$', 'article_archive_year') 
)


##Category List
urlpatterns += patterns('django.views.generic.list_detail',
    url(r'^categories/$', 'object_list', 
        {'queryset': models.Category.objects.all(), 'allow_empty': True,})
)


##Feeds
feed_args = {
    'featured': FeaturedEntries,
    'all': AllEntries,
}
urlpatterns += patterns('',
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', 
        {'feed_dict': feed_args}),
)


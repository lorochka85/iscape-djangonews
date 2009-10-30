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


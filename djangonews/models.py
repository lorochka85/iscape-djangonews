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
from django.db import models
from django.contrib.syndication.feeds import Feed
from random import choice
from djangonews import managers
from sorl.thumbnail import fields
import PIL
from django.conf import settings

class Article(models.Model):
    """A single news article"""
    title = models.CharField(max_length=400)
    location = models.CharField(max_length=200, blank=True)
    slug = models.SlugField('ID',
        unique_for_date='release_date',
        help_text='Automatically generated from the title.'
    )
    body = models.TextField()
    teaser = models.TextField(blank=True, 
        help_text="A summary preview of the article.")
    release_date = models.DateTimeField('Publication Date', 
        default=datetime.now)
    expire_date = models.DateTimeField('Expiration Date', null=True, blank=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    categories = models.ManyToManyField('Category', related_name='articles', 
        null=True, blank=True)
    
    objects = managers.ArticleManager()

    class Meta:
        ordering = ('-release_date',)
        get_latest_by = 'release_date'

    def random_thumbnail(self):
        """Returns randon marked as thumbnail image attached to the article"""
        if self.images.filter(thumbnail=True).count() > 0:
            return choice(self.images.filter(thumbnail=True))

    def __unicode__(self):
        return u'%s' %(self.title)

    def get_absolute_url(self):
        return ('news_article_detail', (), { 
            'year': self.release_date.strftime('%Y'),
            'month': self.release_date.strftime('%b').lower(),
            'day': self.release_date.strftime('%d'),
            'slug': self.slug })
    get_absolute_url = models.permalink(get_absolute_url)

    def get_previous_published(self):
        try: 
            return self.get_previous_by_release_date(active=True, 
            expire_date__gte=datetime.now, release_date__lte=datetime.now())
        except:
            return self.get_previous_by_release_date(active=True, 
            expire_date__isnull=True, release_date__lte=datetime.now())
     
    def get_next_published(self):
        try:
            return self.get_next_by_release_date(active=True, 
            expire_date__gte=datetime.now, release_date__lte=datetime.now())
        except:
            return self.get_next_by_release_date(active=True, 
            expire_date__isnull=True, release_date__lte=datetime.now())


class Category(models.Model):
    """Category model for articles"""
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(
        help_text='Automatically generated from the title.'
    )

    class Meta:
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('news_category_detail', [str(self.slug)])


class Image(models.Model):
    """Image for an article"""
    image = fields.ImageField(blank=False, upload_to='djangonews/images',
        help_text="Images larger than 800x600 will be resized")
    article = models.ForeignKey(Article, related_name='images')
    caption = models.CharField(max_length=200, blank=True)
    name = models.CharField('description', max_length=100, blank=True, 
        help_text="This will be used for alt text.")
    thumbnail = models.BooleanField('Use as Thumbnail', default=False, 
        help_text="To be displayed on article listing pages. If more than "
                  "one is selected, the thumbnail used will be chosen at "
                  "random.")
    sort = models.IntegerField(default=0)

    class Meta:
        ordering = ('sort',)

    def save(self):
        """
        Save image as regular model if it's parameters satisfy 
        DJANGONEWS_IMAGE_WIDTH, DJANGONEWS_IMAGE_HEIGHT,
        DJANGONEWS_IMAGE_QUALITY settings. Otherwise using 
        PIL to modify attached image file
        """
        super(Image, self).save()
        if self.image:
            filename = self.image.path
            image = PIL.Image.open(filename)
            try:
                width = settings.DJANGONEWS_IMAGE_WIDTH
            except:
                width = 800
            try:
                height = settings.DJANGONEWS_IMAGE_HEIGHT
            except:
                height = 600
            try:
                imquality = settings.DJANGONEWS_IMAGE_QUALITY
            except:
                imquality = 100
            size=(width, height)
            image.thumbnail(size, PIL.Image.ANTIALIAS)
            image.save(filename, quality=imquality)

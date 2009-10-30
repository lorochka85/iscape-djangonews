from datetime import datetime
from django.db import models
from django.contrib.syndication.feeds import Feed
from random import choice
from djangonews import managers
from sorl.thumbnail import fields
import PIL
from django.conf import settings

class Article(models.Model):
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

class Location(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.title

from django.contrib.syndication.feeds import Feed
from djangonews.models import Article

class FeaturedEntries(Feed):
    title = "Featured Articles"
    link = "/news/"
    description = "Featured Articles"

    def items(self):
        return Article.objects.get_featured()

class AllEntries(Feed):
    title = "All News"
    link = "/news/"
    description = "All News"

    def items(self):
        return Article.objects.get_published()

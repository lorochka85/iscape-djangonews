from django.template import Library, Node
from djangonews.models import Article

register = Library()

class FeaturedNode(Node):
    def render(self, context):
        context['featured_list'] = Article.objects.get_featured()
        return ''

    def get_featured(parser, token):
        return FeaturedNode()
    get_featured = register.tag(get_featured)


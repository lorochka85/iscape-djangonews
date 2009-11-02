from django import forms
from django.utils.safestring import mark_safe 
from django.conf import settings


class TinyMCEWidget(forms.Textarea):
    """
    Textarea widget with TinyMCE.
    Don't forget to put TinyMCE in the directory specified in MEDIA_ROOT
    """
    def render(self, name, value, attrs=None):
        self.attrs = {'class': 'tinymce vLargeTextField', 'rows': '16','cols': '40'}
        output = [super(TinyMCEWidget, self).render(name, value, attrs)]
        return mark_safe(u''.join(output)) 

    class Media:
        js = (
            '/%s/tiny_mce/tiny_mce.js' % settings.MEDIA_URL,
            # appmedia is default location for staticmedia. See
            # django-staticmedia documentation for more info.
            '/appmedia/djangonews/djangonews/js/textareas.js', 
        )

class SmallTextField(forms.Textarea):
    """Default TextArea seems to be too big..."""
    def render(self, name, value, attrs=None):
        self.attrs = {'rows': '3','cols': '50'}
        output = [super(SmallTextField, self).render(name, value, attrs)]
        return mark_safe(u''.join(output))


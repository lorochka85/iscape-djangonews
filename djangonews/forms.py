from django import forms
from django.db.models import get_model
from djangonews import widgets

class ArticleAdminModelForm(forms.ModelForm):
    body = forms.CharField(widget=widgets.TinyMCEWidget())
    teaser = forms.CharField(required=False, widget=widgets.SmallTextField())

    class Meta:
        model = get_model('djangonews', 'article')


# from django.core.urlresolvers import reverse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    This view renders the main page
    """
    template_name = 'emailer/index.html'

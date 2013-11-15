# from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from .models import Sector, Email


class IndexView(TemplateView):
    """
    This view renders the main page
    """
    template_name = 'emailer/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['sectors'] = Sector.objects.all()
        context['total_emails'] = Email.objects.all().count()
        return context

# from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View, DetailView, ListView, CreateView
from braces.views import AjaxResponseMixin, JSONResponseMixin
from .models import *
from .forms import *


class IndexView(TemplateView):
    """
    This view renders the main page
    """
    template_name = 'emailer/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['sectors'] = Sector.objects.all()
        context['total_emails'] = Email.objects.all().count()
        context['latest_campaigns'] = Campaign.objects.all()[:10]
        context['button_dashboard_on'] = True
        return context

#### Campaign ####


class CampaignsNavButtonOnMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CampaignsNavButtonOnMixin, self).get_context_data(**kwargs)
        context['button_campaigns_on'] = True
        return context


class CampaignCreateView(CampaignsNavButtonOnMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "emailer/campaign-create.html"


class CampaignDetailView(CampaignsNavButtonOnMixin, DetailView):
    model = Campaign
    template_name = "emailer/campaign-detail.html"


class CampaignListView(CampaignsNavButtonOnMixin, ListView):
    model = Campaign
    template_name = "emailer/campaign-list.html"
    paginate_by = 5


class SectorsChartDataView(JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):

        # This is very naive...
        response = []
        for sector in Sector.objects.all():
            response.append({'label': sector.name, 'value': sector.num_emails})
        return self.render_json_response(response)

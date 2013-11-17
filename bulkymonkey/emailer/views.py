from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View, DetailView, ListView, CreateView, DeleteView, FormView
from braces.views import AjaxResponseMixin, JSONResponseMixin, LoginRequiredMixin, StaffuserRequiredMixin
from .models import *
from .forms import *


class IndexView(LoginRequiredMixin, StaffuserRequiredMixin, TemplateView):
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


class CampaignCreateView(LoginRequiredMixin, StaffuserRequiredMixin, CampaignsNavButtonOnMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = "emailer/campaign-create.html"


class CampaignDetailView(LoginRequiredMixin, StaffuserRequiredMixin, CampaignsNavButtonOnMixin, DetailView):
    model = Campaign
    template_name = "emailer/campaign-detail.html"


class CampaignDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, CampaignsNavButtonOnMixin, DeleteView):
    model = Campaign
    form_class = DeleteForm
    template_name = "emailer/delete.html"
    success_message = _("Campaign deleted successfully")

    def get_context_data(self, **kwargs):
        context = super(CampaignDeleteView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('bulkymonkey:campaign-list')


class CampaignListView(LoginRequiredMixin, StaffuserRequiredMixin, CampaignsNavButtonOnMixin, ListView):
    model = Campaign
    template_name = "emailer/campaign-list.html"
    paginate_by = 5


#### Sector ####


class SectorsNavButtonOnMixin(object):
    def get_context_data(self, **kwargs):
        context = super(SectorsNavButtonOnMixin, self).get_context_data(**kwargs)
        context['button_campaigns_on'] = True
        return context


class SectorCreateView(LoginRequiredMixin, StaffuserRequiredMixin, SectorsNavButtonOnMixin, CreateView):
    model = Sector
    form_class = SectorForm
    template_name = "emailer/sector-create.html"


class SectorDetailView(LoginRequiredMixin, StaffuserRequiredMixin, SectorsNavButtonOnMixin, DetailView):
    model = Sector
    template_name = "emailer/sector-detail.html"


class SectorDeleteView(LoginRequiredMixin, StaffuserRequiredMixin, SectorsNavButtonOnMixin, DeleteView):
    model = Sector
    form_class = DeleteForm
    template_name = "emailer/delete.html"
    success_message = _("Sector deleted successfully")

    def get_context_data(self, **kwargs):
        context = super(SectorDeleteView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def get_success_url(self):
        messages.success(self.request, self.success_message)
        return reverse('bulkymonkey:index')


class SectorsChartDataView(LoginRequiredMixin, StaffuserRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View):
    def get_ajax(self, request, *args, **kwargs):

        # This is very naive...
        response = []
        for sector in Sector.objects.all():
            response.append({'label': sector.name, 'value': sector.num_emails})
        return self.render_json_response(response)


#### Load emails from file ####


class LoadEmailsFromFileView(SuccessMessageMixin, FormView):
    template_name = "emailer/load-emails.html"
    form_class = LoadEmailsFromFileForm
    success_message = _('{num_emails} emails were added to {sector}')
    success_url = reverse_lazy('bulkymonkey:index')

    @method_decorator(transaction.atomic)
    def dispatch(self, request, *args, **kwargs):
        return super(LoadEmailsFromFileView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super(LoadEmailsFromFileView, self).get_initial()
        initial['sectors'] = Sector.objects.all().values_list('pk', 'name')
        return initial

    def form_valid(self, form):
        self.emails_to_load = form.cleaned_data['data'].splitlines()
        for address in self.emails_to_load:
            email = Email.objects.get_or_create(address=address)[0]
            email.sectors.add(form.cleaned_data['sector'])
        return super(LoadEmailsFromFileView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message.format(sector=cleaned_data['sector'],
                                           num_emails=len(self.emails_to_load))

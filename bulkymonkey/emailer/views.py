from django.core.urlresolvers import reverse, reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import TemplateView, View, DetailView, ListView, CreateView, DeleteView, FormView
from django.core.mail import EmailMultiAlternatives
from braces.views import AjaxResponseMixin, JSONResponseMixin, LoginRequiredMixin, StaffuserRequiredMixin
from .models import *
from .forms import *


class PaginateMixin(object):
    paginate_model = None
    paginate_ctx_name = 'object_list'
    paginator_obj_ctx_name = 'page_obj'
    paginate_by = 10
    paginate_queryset = None

    def get_context_data(self, **kwargs):
        context = super(PaginateMixin, self).get_context_data(**kwargs)
        if self.paginate_queryset is not None:
            object_list = self.paginate_queryset
        else:
            object_list = self.paginate_model.objects.all()
        paginator = Paginator(object_list, self.paginate_by)  # Show self.paginate_by contacts per page

        context['is_paginated'] = len(object_list) > self.paginate_by

        if context['is_paginated']:
            page = self.request.GET.get('page')
            try:
                objects = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                objects = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                objects = paginator.page(paginator.num_pages)

            context[self.paginator_obj_ctx_name] = objects
            context[self.paginate_ctx_name] = objects
        else:
            context[self.paginate_ctx_name] = object_list
        return context


class SectorChoicesInitialMixin(object):
    def get_initial(self):
        initial = super(SectorChoicesInitialMixin, self).get_initial()
        initial['sectors'] = Sector.objects.all().values_list('pk', 'name')
        return initial


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
        context['campaign_logs'] = SentCampaignLog.objects.all()[:10]
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
    paginate_by = 10


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


class SectorDetailView(LoginRequiredMixin, StaffuserRequiredMixin, PaginateMixin, SectorsNavButtonOnMixin, DetailView):
    model = Sector
    template_name = "emailer/sector-detail.html"
    paginate_by = 50
    paginate_ctx_name = 'email_list'

    def get_context_data(self, **kwargs):
        self.paginate_queryset = self.object.email_set.all()
        context = super(SectorDetailView, self).get_context_data(**kwargs)
        context['num_emails'] = len(context[self.paginate_ctx_name])
        return context


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


class LoadEmailsFromFileView(SectorChoicesInitialMixin, SuccessMessageMixin, FormView):
    template_name = "emailer/load-emails.html"
    form_class = LoadEmailsFromFileForm
    success_message = _('{num_emails} emails were added to {sector}')
    success_url = reverse_lazy('bulkymonkey:index')

    @method_decorator(transaction.atomic)
    def dispatch(self, request, *args, **kwargs):
        return super(LoadEmailsFromFileView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.emails_to_load = form.cleaned_data['data'].splitlines()
        for address in self.emails_to_load:
            email = Email.objects.get_or_create(address=address)[0]
            email.sectors.add(form.cleaned_data['sector'])
        return super(LoadEmailsFromFileView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message.format(sector=cleaned_data['sector'],
                                           num_emails=len(self.emails_to_load))


#### Send emails ####


class SendEmailsView(SectorChoicesInitialMixin, SuccessMessageMixin, FormView):
    template_name = "emailer/send-emails.html"
    form_class = SendEmailsForm
    success_message = _('{num_emails} emails from {sector} were queued in Mandrill')
    success_url = reverse_lazy('bulkymonkey:index')

    def get_initial(self):
        initial = super(SendEmailsView, self).get_initial()
        initial['campaigns'] = Campaign.objects.all().values_list('pk', 'title')
        return initial

    def form_valid(self, form):
        sector = form.cleaned_data['sector']
        self.num_emails = sector.email_set.count()
        campaign = form.cleaned_data['campaign']

        # Log action
        campaign_log = SentCampaignLog.objects.create(campaign=campaign, sector=sector, num_emails=self.num_emails)

        # Build message
        msg = EmailMultiAlternatives(
            subject=campaign.title,
            body='',
            from_email="{from_name} <{from_email}>".format(from_name=campaign.from_name,
                                                           from_email=campaign.from_email),
        )
        msg.attach_alternative(campaign.html_mail.read(), "text/html")

        # Optional Mandrill-specific extensions:
        msg.tags = campaign.get_tags()
        msg.async = True
        msg.track_opens = True
        msg.track_clicks = True

        # Send to Mandrill
        for email in sector.email_set.all():
            msg.to = [email.address]
            msg.send()

        # Change status
        campaign_log.is_sent = True
        campaign_log.save()

        return super(SendEmailsView, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message.format(sector=cleaned_data['sector'],
                                           num_emails=self.num_emails)

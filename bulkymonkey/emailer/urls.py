from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    '',

    # Index page
    url(r'^$', IndexView.as_view(), name='index'),

    # Campaign
    url(r'^campaigns$', CampaignListView.as_view(), name='campaign-list'),
    url(r'^campaign/add$', CampaignCreateView.as_view(), name='campaign-create'),
    url(r'^campaign/(?P<pk>\d+)/$', CampaignDetailView.as_view(), name='campaign-detail'),
    url(r'^campaign/(?P<pk>\d+)/delete$', CampaignDeleteView.as_view(), name='campaign-delete'),

    # Sector
    # url(r'^sectors$', SectorListView.as_view(), name='sector-list'),
    url(r'^sector/add$', SectorCreateView.as_view(), name='sector-create'),
    url(r'^sector/(?P<pk>\d+)/$', SectorDetailView.as_view(), name='sector-detail'),
    url(r'^sector/(?P<pk>\d+)/delete$', SectorDeleteView.as_view(), name='sector-delete'),

    # Ajax
    url(r'^sectors/chart$', SectorsChartDataView.as_view(), name='sectors-chart-ajax'),

    # Load emails
    url(r'^load-emails$', LoadEmailsFromFileView.as_view(), name='load-emails'),

    # Send emails
    url(r'^send-emails$', SendEmailsView.as_view(), name='send-emails'),
    url(r'^progress/(?P<pk>\d+)/$', ShowProgressView.as_view(), name='progress'),
    url(r'^get-progress/(?P<pk>\d+)/$', GetCurrentProgressView.as_view(), name='get-progress'),
)

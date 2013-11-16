from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns(
    '',

    # Index page
    url(r'^$', IndexView.as_view(), name='index'),

    # Campaign
    url(r'^campaigns$', CampaignListView.as_view(), name='campaign-list'),
    url(r'^campaign/add$', CampaignCreateView.as_view(), name='campaign-create'),
    url(r'^campaign/(?P<pk>\d+)$', CampaignDetailView.as_view(), name='campaign-detail'),
    url(r'^campaign/(?P<pk>\d+)/delete$', CampaignDeleteView.as_view(), name='campaign-delete'),

    # Ajax
    url(r'^sectors/chart$', SectorsChartDataView.as_view(), name='sectors-chart-ajax'),
)

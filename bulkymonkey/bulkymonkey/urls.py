from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

import emailer.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bulkymonkey.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(emailer.urls, namespace='bulkymonkey')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'emailer/login.html'},  name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'emailer/logout.html'}, name="logout"),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

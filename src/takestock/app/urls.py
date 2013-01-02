from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import DetailView, ListView


admin.autodiscover()


urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    url(r'^$', 'takestock.app.views.index'),
    url(r'^clubs/$', 'takestock.app.views.club_general',
        name='club_general'),
    url(r'^clubs/(?P<club_id>\d+)/$',
        'takestock.app.views.club_detail',
        name='club_detail'),
    url(r'^clubs/(?P<club_id>\d+)/pdf/$',
        'takestock.app.views.club_detail_pdf',
        name='club_detail_pdf'),
)

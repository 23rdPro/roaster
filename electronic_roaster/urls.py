

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import logout, login

from roaster_app.views import (
    admin_function, 
    record_detail, 
    get_pdf, 
    super_admin_list, 
    delete_record,
    update_record,
    welcome_page
)

urlpatterns = [
    url(r'^$', welcome_page, name='welcome'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^login/$', login, name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^register/', include('roaster_app.urls', namespace='entry')),
    url(r'^record/', admin_function, name='list'),
    url(r'^super-admin/', super_admin_list, name='super'),
    url('delete/(?P<id>\d+)/$', delete_record, name='delete'),
    url('entry/(?P<id>\d+)/$', record_detail, name='detail'),
    url('edit/(?P<id>\d+)/$', update_record, name='edit'),
    url('pdf-record/', get_pdf, name='pdf'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



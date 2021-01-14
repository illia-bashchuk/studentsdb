from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView, TemplateView
from students.views.contact_admin import ContactView
from students.views.groups import (GroupCreateView, GroupDeleteView, GroupList,
                                   GroupUpdateView)
from students.views.journal import JournalView
from students.views.students import (StudentDeleteView, StudentList,
                                     StudentUpdateView)

from .settings import DEBUG, MEDIA_ROOT

js_info_dict = {
    'packages': ('students',),
}

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'studentsdb.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),


                       # Students urls
                       url(r'^$',
                           StudentList.as_view(), name='home'),
                       # url(r'^$', 'students.views.students.students_list', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^students/add/$',
                           'students.views.students.students_add', name='students_add'),
                       url(r'^students/(?P<pk>\d+)/edit/$',
                           StudentUpdateView.as_view(), name='students_edit'),
                       url(r'^students/(?P<pk>\d+)/delete/$',
                           StudentDeleteView.as_view(), name='students_delete'),
                       # journal urls
                       url(r'^journal/(?P<pk>\d+)?/?$',
                           login_required(JournalView.as_view()), name='journal'),

                       # Group urls
                       url(r'^groups/$',
                           login_required(GroupList.as_view()), name='groups'),
                       url(r'^groups/add/$',
                           login_required(GroupCreateView.as_view()), name='groups_add'),
                       url(r'^groups/(?P<pk>\d+)/edit/$',
                           login_required(GroupUpdateView.as_view()), name='groups_edit'),
                       url(r'^groups/(?P<pk>\d+)/delete/$',
                           login_required(GroupDeleteView.as_view()), name='groups_delete'),

                       # Contact Admin Form
                       url(r'^contact-admin/$', login_required(ContactView.as_view()),
                           name='contact_admin'),

                       url(r'^admin/', include(admin.site.urls)),

                       # JavaScript i18n
                       url(r'^jsi18n\.js$',
                           'django.views.i18n.javascript_catalog', js_info_dict),

                       

                       # User Related urls
                       url(r'^users/profile/$', login_required(TemplateView.as_view(
                           template_name='registration/profile.html')), name='profile'),
                       url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'},
                           name='auth_logout'),
                       url(r'^users/register/complete/$', RedirectView.as_view(pattern_name='home'),
                           name='registration_complete'),
                       url(r'^users/', include('registration.backends.simple.urls')),
                       )


if DEBUG:
    # serve files from media folder
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': MEDIA_ROOT}))

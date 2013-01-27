from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# importamos settings
from entrecalle import settings

handler404 = "entrecalle_app.views.handler404"
handler500 = "entrecalle_app.views.handler500"

 
urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    #aqui comienzan las urls de entrecalle
    url(r'', include('multiuploader.urls')),
    url(r'^$', 'entrecalle_app.views.index', name='index'),

    
    url(r'^register/$', 'entrecalle_app.views.register', name='register'),
    url(r'^login/$', 'entrecalle_app.views.login', name='login'),
    url(r'^logout/$', 'entrecalle_app.views.logout', name='logout'),
    url(r'^user/$', 'entrecalle_app.views.infoUser', name='infoUser'),
    url(r'^user/info$', 'entrecalle_app.views.infoUser_ajax', name='infoUser_ajax'),





    url(r'^terminos/$', 'entrecalle_app.views.terminos', name='Terminos'),
    url(r'^privacidad/$', 'entrecalle_app.views.privacidad', name='Privacidad'),
    url(r'^password/$', 'entrecalle_app.views.passord_reset', name='Reset'),



    
    
    url(r'^building/add/$', 'entrecalle_app.building.build_add', name='build_add'),
    url(r'^building/view/(\d+)/$', 'entrecalle_app.building.build_view', name='build_view'),
    url(r'^building/photo/add/(\d+)/$', 'entrecalle_app.building.building_photo_render', name='building_photo_render'),
    url(r'^building/photo/add/ajax$', 'entrecalle_app.building.building_photo_ajax', name='building_photo_ajax'),
    url(r'^building/json/$', 'entrecalle_app.services.building_json', name='build_json'),
    url(r'^building/add/cronica/$', 'entrecalle_app.building.Agregar_Cronica', name='Agregar_Cronica'),
    

    # Reseteo de password
    #url(r'^passreset/$',auth_views.password_reset,{'template_name': 'forgot_password.html'},name='forgot_password1',),
    url(r'^forgot_password/$',auth_views.password_reset,name='forgot_password1'),
    url(r'^forgot_password/done/$',auth_views.password_reset_done,name='forgot_password2'),
    url(r'^forgot_password/confirm/(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,name='forgot_password3'),
    url(r'^forgot_password/complete/$',auth_views.password_reset_complete,name='forgot_password4'),
    
    #url(r'^style/add/$', 'entrecalle_app.views.style_add', name='style_add'),
    
)

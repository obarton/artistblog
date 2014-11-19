from django.conf import settings
from django.conf.urls import patterns, url
from artistblog import views

urlpatterns = patterns('', 
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
	url(r'^register/$', views.register, name='register'),
	url(r'^registerartist/$', views.register_artist, name='register_artist'),
	url(r'^registerblog/$', views.register_blog, name='register_artist'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^restricted/',views.restricted, name='restricted'),
	url(r'^logout/$', views.user_logout, name='logout')
	)

if settings.DEBUG:
	urlpatterns += patterns(
		'django.views.static',
		(r'media/(?P<path>.*)',
		'serve',
		{'document_root': settings.MEDIA_ROOT}),)
from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.post_list, name='post_list'),
	url(r'^upload', views.upload_image, name='upload_image'),
	url(r'^post/new$', views.post_new, name='post_new'),
	url(r'^post/(?P<post_id>[0-9]+$)', views.blog_post, name='blog_post'),
	url(r'^post/(?P<post_id>[0-9]+)/post_edit$', views.post_edit, name='blog_post_edit'),
]

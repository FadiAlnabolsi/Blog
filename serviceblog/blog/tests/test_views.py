from django.core.urlresolvers import resolve
from django.test import TestCase, Client
from django.http import HttpRequest
from django.template.loader import render_to_string

from blog.views import post_list, blog_post, post_edit
from blog.models import Post
from blog.forms import initialPostForm, editPostForm

import unittest

class blog_post_view(TestCase):

	def test_specific_post_redirects_to_blog_post_view(self):
		sample = Post()
		sample.save()
		found = resolve('/blog/post/1')
		self.assertEqual(found.func, blog_post)

	def test_invalid_post_redirects_to_404(self):
		request = HttpRequest()
		response = blog_post(request, 2)
		self.assertIn('Page not found', response.content.decode())

	def test_blog_page_renders_blog_template(self):
		response = self.client.get('/blog')
		self.assertTemplateUsed(response, 'base.html')

	def test_inactive_posts_arent_viewable_by_casuals(self):
		sample = Post()
		sample.active = False
		sample.save()
		request = HttpRequest()
		response = blog_post(request, 1)
		self.assertIn('Page not found', response.content.decode())

	def test_active_posts_are_viewable_by_casuals(self):
		sample = Post()
		sample.active = True
		sample.save()
		request = HttpRequest()
		response = blog_post(request, 1)
		self.assertIn('Page not found', response.content.decode())

class post_list_view(TestCase):

	def test_bolg_redirect_to_blog_view(self):
		found = resolve('/blog')
		self.assertEqual(found.func, post_list)

	def test_uses_blog_template(self):
		response = self.client.get('/blog')
		self.assertTemplateUsed(response,'blog.html')

	def test_inactive_posts_dont_show_on_blog_page(self):
		sample = Post()
		sample.title = 'TestTitle'
		sample.text = 'TestText'
		sample.active = False
		sample.save()

		sample2 = Post()
		sample2.title = 'SecondTestTitle'
		sample2.text = 'SecondTestText'
		sample2.active = False
		sample2.save()

		post = Post.objects.all()

		expected_html = render_to_string('blog.html', {'post':post})

		self.assertNotIn('TestTitle', expected_html)
		self.assertNotIn('SecondTestTitle', expected_html)

	def test_active_posts_show_on_blog_page(self):
		sample = Post()
		sample.title = 'TestTitle'
		sample.text = 'TestText'
		sample.active = True
		sample.save()

		sample2 = Post()
		sample2.title = 'SecondTestTitle'
		sample2.text = 'SecondTestText'
		sample2.active = True
		sample2.save()

		post = Post.objects.all()

		expected_html = render_to_string('blog.html', {'post':post})
		self.assertIn('TestTitle', expected_html)
		self.assertIn('TestText', expected_html)
		self.assertIn('SecondTestTitle', expected_html)
		self.assertIn('SecondTestText', expected_html)


		#class post_new_view(TestCase):

	
	# def test_inactive_posts_show_for_admins(self):
	# 	self.client = Client()
	# 	response = self.client.post('/api/login/',{'email':'falnabolsi@service.com', 'password':'junk'})
	# 	print(response.status_code)

	# 	sample = Post()
	# 	sample.title = 'TestTitle'
	# 	sample.text = 'TestText'
	# 	sample.active = False
	# 	sample.save()

	# 	sample2 = Post()
	# 	sample2.title = 'SecondTestTitle'
	# 	sample2.text = 'SecondTestText'
	# 	sample2.active = False
	# 	sample2.save()

	# 	post = Post.objects.all()
	# 	self.assertIn('TestTitle', expected_html)
	# 	self.assertIn('SecondTestTitle', expected_html)
class post_edit_view(TestCase):

	def test_edit_redirects_to_post_edit_view(self):
		sample = Post()
		sample.save()
		found = resolve('/blog/post/1/post_edit')
		self.assertEqual(found.func, post_edit)

class BlogPageTest(TestCase):

	def test_forms_show_on_blog_post_page(self):
		response = self.client.get('/blog/post/new')
		self.assertIsInstance(response.context['form'], initialPostForm)


from django.core.urlresolvers import resolve
from django.test import TestCase, Client
from django.http import HttpRequest
from django.template.loader import render_to_string

from users.models import ServiceUser, ServiceUserManager

from blog.views import post_list, blog_post, post_edit
from blog.models import Post

import unittest

def create_instance(num_instances, isActive):
	if num_instances == 1:
		sample = Post()
		sample.author = 'Fadi'
		sample.title = 'TestTitle'
		sample.created_date = '2015-09-04'
		sample.published_date = '2015-09-04'
		sample.text = 'AND NEW'
		sample.active = isActive
		sample.save()
		return Post.objects.all()

	elif num_instances == 2:
		sample = Post()
		sample.title = 'TestTitle'
		sample.text = 'TestText'
		sample.created_date = '2015-09-04'
		sample.published_date = '2015-09-04'
		sample.active = isActive
		sample.save()

		sample2 = Post()
		sample2.title = 'SecondTestTitle'
		sample2.text = 'SecondTestText'
		sample2.created_date = '2015-09-04'
		sample2.published_date = '2015-09-04'
		sample2.active = isActive
		sample2.save()

	return Post.objects.all()

def login_to_superuser(self):
	self.client = Client()
	self.client.login(email='blog@test.com', password='password')

class blog_post_view(TestCase):
	fixtures = ['users.json']
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
	
	def test_inactivate_posts_are_viewable_by_superusers(self):
		login_to_superuser(self)

		post = create_instance(1, False)


		response = self.client.get('/blog/post/%s' % post[0].id)
		self.assertIn('TestTitle', response.content.decode())

	def test_login(self):
		self.client = Client()
		response = self.client.login(email='blog@test.com', password='password')
		self.assertTrue(response)

class post_list_view(TestCase):
	fixtures = ['users.json']

	def test_blog_redirect_to_blog_view(self):
		found = resolve('/blog')
		self.assertEqual(found.func, post_list)

	def test_uses_blog_template(self):
		response = self.client.get('/blog')
		self.assertTemplateUsed(response,'blog.html')

	def test_inactive_posts_in_list_arent_viewable_by_casuals(self):
		create_instance(2, False)

		response = self.client.get('/blog')
		expected_html = response.content.decode()

		self.assertNotIn('TestTitle', expected_html)
		self.assertNotIn('SecondTestTitle', expected_html)

	def test_active_posts_show_on_blog_list_page(self):
		create_instance(2, True)

		response = self.client.get('/blog')
		expected_html = response.content.decode()

		self.assertIn('TestTitle', expected_html)
		self.assertIn('SecondTestText', expected_html)

	def test_inactivate_posts_in_list_are_viewable_by_superusers(self):
		login_to_superuser(self)

		create_instance(1, False)

		response = self.client.get('/blog')
		self.assertIn('TestTitle', response.content.decode())

class post_edit_view(TestCase):
	fixtures = ['users.json']
	
	def test_unauthorized_user_redirected_to_front_blog_page(self):
		response = self.client.get('/blog/post/1/post_edit')

		self.assertEqual('http://testserver/blog', response.url)

	def test_edit_redirects_to_post_edit_view(self):
		sample = Post()
		sample.save()
		found = resolve('/blog/post/7/post_edit')
		self.assertEqual(found.func, post_edit)
		
	def test_if_submit_is_pressed_redirects_to_specific_post(self):
		login_to_superuser(self)
		
		post = create_instance(1, False)

		response = self.client.post(
			'/blog/post/' + str(post[0].id) + '/post_edit', 
			{
				'author':'Fadi Alnabolsi',
				'title':'Fadi', 
				'text':'Testing out this blog', 
				'active':False,
				'submit':'submit'
			}, 
			follow=True)

		self.assertRedirects(response, '/blog/post/' + str(post[0].id))

	def test_if_preview_is_pressed_redirects_to_preview_page(self):
		login_to_superuser(self)
		
		post = create_instance(1, False)

		response = self.client.post(
			'/blog/post/' + str(post[0].id) + '/post_edit', 
			{
				'author':'Fadi Alnabolsi',
				'title':'Fadi', 
				'text':'Testing out this blog', 
				'active':False,
				'preview':'preview'
			}, 
			follow=True)
		self.assertTemplateUsed(response, 'preview_post.html')

	def test_if_delete_if_pressed_redirects_to_front_page(self):
		login_to_superuser(self)
		
		post = create_instance(1, False)

		response = self.client.post(
			'/blog/post/' + str(post[0].id) + '/post_edit', 
			{
				'title':'Fadi', 
				'text':'Testing out this blog', 
				'active':False,
				'delete':'delete'
			}, 
			follow=True)

		self.assertRedirects(response, '/blog/')




#class post_new_view(TestCase):


# class BlogPageTest(TestCase):
# 	fixtures = ['users.json']

# 	def test_forms_show_on_blog_post_page(self):
# 		login_to_superuser(self)

# 		response = self.client.get('/blog/post/new')
# 		self.assertIsInstance(response.context['form'], initialPostForm)



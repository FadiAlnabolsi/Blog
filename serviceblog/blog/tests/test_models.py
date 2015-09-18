from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from blog.views import post_list, blog_post, post_edit
from blog.models import Post

import unittest

class BlogModelTest(TestCase):
	
	def test_model_post_creation(self):
		sample = Post()
		sample.author = 'Fadi'
		sample.title = 'Test Yo'
		sample.created_date = '2015-09-04'
		sample.text = 'AND NEW'
		sample.slug = '1'
		sample.save()

		sample2 = Post()
		sample2.author = 'Swift'
		sample2.title = 'UFC Champion'
		sample2.created_date = '2015-09-04'
		sample2.text = 'AND STILL'
		sample2.slug = '2'
		sample2.save()

		saved_posts = Post.objects.all()
		self.assertEqual(saved_posts.count(), 2)

		first_sample = saved_posts[0]
		second_sample = saved_posts[1]
		self.assertEqual(first_sample.author, 'Fadi')
		self.assertEqual(first_sample.text, 'AND NEW')
		self.assertEqual(first_sample.title, 'Test Yo')
		#self.assertEqual(first_sample.created_date.datefield, '2015-09-04')
		self.assertEqual(second_sample.author, 'Swift')
		self.assertEqual(second_sample.text, 'AND STILL')
		self.assertEqual(second_sample.title, 'UFC Champion')
		#self.assertEqual(second_sample.created_date, '2015-09-04')

	
	@unittest.skip("No slugs to test for now")
	def test_duplicate_slugs_are_not_saved(self):
		try:
			sample = Post()
			sample.slug = '1'
			sample.save()

			sample2 = Post()
			sample2.slug = '1'
			sample2.save()
			
		except Exception as e:
			print('DUPLICATE SLUG \n')
			pass
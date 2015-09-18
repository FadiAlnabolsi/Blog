from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

class Post(models.Model):
	author = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	text = models.TextField()
	draft = models.TextField()
	created_date = models.DateTimeField(
			default=timezone.now)
	published_date = models.DateTimeField(
			blank=True, null=True)
	active = models.BooleanField(default=True)
	#slug = models.SlugField(unique=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	#def save(self, *args, **kwargs):
	#	self.slug = slugify(self.title)
	#	super(Post, self).save(*args, **kwargs)

	def __str__(self):
		return self.title
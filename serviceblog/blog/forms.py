from django import forms
from blog.models import Post, Asset

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('author', 'title', 'text', 'active')

class editDraftPostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('draftTitle', 'draft', 'active')

class ImageForm(forms.ModelForm):

	class Meta:
		model = Asset
		fields = ('asset', 'name')
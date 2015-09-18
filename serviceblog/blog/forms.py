from django import forms
from blog.models import Post

class initialPostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('author', 'title', 'text', 'active')

class editPostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'text', 'active')

class editDraftPostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'draft', 'active')
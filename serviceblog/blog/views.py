from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, Http404, HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import slugify
from django.utils import timezone
from blog.models import Post, Asset
from blog.forms import PostForm, editDraftPostForm, ImageForm

import datetime

def checkUserIsAdmin(request):
	if (request.user.is_superuser == False):
		print('Not authorized user, returning to front blog page')
		return redirect('/blog')	

def upload_image(request):
	print('\nView: upload_image')
	if (request.user.is_superuser == False):
		print('Not authorized user, returning to front blog page')
		return redirect('/blog')	

	Form = ImageForm(request.POST, request.FILES)

	if Form.is_valid():
		Form.save()

	asset = Asset.objects.all().order_by('-id')
	paths = []

	for x in asset:
		paths.append(x.asset.path.split('/main', 1)[-1])

	paginator = Paginator(paths, 15) #5 blog posts per page

	page = request.GET.get('page')

	try:
		pagPaths = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		pagPaths = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		pagPaths = paginator.page(paginator.num_pages)
	return render(request,'image_portal.html', {'ImageForm':Form, 'paths':pagPaths})

# viewing a single blog post
# will return 404 if page is inactive and not an admin
# will return actual blog post if admin

def blog_post(request, post_id):
	print('\nView: Blog_Post')
	
	try:
		post = Post.objects.get(id=post_id)

		#only admins can view inactive posts
		if (post.active == False) and (request.user.is_superuser == True):
			print('Authorized User, inactive post')
			return render(request, 'single_post.html', {'post':post})

		if (post.active == False) and (request.user.is_superuser == False):
			print('Unauthorized User, inactive post')
			return redirect('/blog')

		print('Active Post, free for anyone to view')
		return render(request, 'single_post.html', {'post':post})

	except Exception as e:
		return redirect('/blog')


# page to view all posts
# authenticated users see active and inactive posts
# regular users just see active posts
def post_list(request):

	print('\nView: post_List')

	if request.user.is_superuser:
		print('User Authenticated')
		post = Post.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
		paginator = Paginator(post, 5) #5 blog posts per page

		page = request.GET.get('page')

		try:
			blogPosts = paginator.page(page)
		except PageNotAnInteger:
			#If page is not an integer, deliver first page.
			blogPosts = paginator.page(1)
		except EmptyPage:
			#If page is out of range, deliver last page of results
			blogPosts = paginator.page(paginator.num_pages)
		return render(request, 'blog.html', {'blogPosts':blogPosts, 'ImageForm':ImageForm})
	
	else:
		print('User not authenticated')
		
		post = Post.objects.filter(created_date__lte=timezone.now()).filter(active=True).order_by('-created_date')
		paginator = Paginator(post, 5) #5 blog posts per page

		page = request.GET.get('page')
		try:
			blogPosts = paginator.page(page)
		except PageNotAnInteger:
			#If page is not an integer, deliver first page.
			blogPosts = paginator.page(1)
		except EmptyPage:
			#If page is out of range, deliver last page of results
			blogPosts = paginator.page(paginator.num_pages)
		return render(request, 'blog.html', {'blogPosts':blogPosts})

# page to post a new post
def post_new(request):
	print('\nView: post_new')
	if (request.user.is_superuser == False):
		print('Not authorized user, returning to front blog page')
		return redirect('/blog')

	if request.method =='POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			#post.author = request.user
			post.draft = form['text']
			post.published_date = timezone.now()
			post.save()
			return redirect('blog.views.blog_post', post_id=post.id)

	else:
		form = PostForm()
		
	return render(request, 'post_edit.html', {'form': form})

# modifying an already-made post
def post_edit(request, post_id):
	print('\nView: post_edit')
	if (request.user.is_superuser == False):
		print('Not authorized user, returning to front blog page')
		return redirect('/blog')

	post = get_object_or_404(Post, id=post_id)
	form = PostForm(request.POST, instance=post)
	editForm = editDraftPostForm(request.POST, instance=post)
	textHolder = post.text
	titleHolder = post.title

	if request.method == 'POST':

		if 'submit' in request.POST:
			if form.is_valid():
				print('Form Submit')
				post = form.save(commit=False)
				post.draft = form.data['text']
				post.draftTitle = form.data['title']
				post.published_date = timezone.now()
				post.save()

				return redirect('blog.views.blog_post', post_id=post_id)

			if editForm.is_valid():
				post.text = form.data['draft']
				post.title = form.data['draftTitle']
				post.save()

		if 'preview' in request.POST:
			if form.is_valid():
				print('Form Preview')
				post.draft = form.data['text']
				post.draftTitle = form.data['title']
				post.save()
				post.text = textHolder
				post.title = titleHolder
				post.save()
				return render(request, 'preview_post.html', {'post':post})

			if editForm.is_valid():
				post.save()
				return render(request, 'preview_post.html', {'post':post})

		#Delete in previewing post
		if 'delete' in request.POST:
			print('Global Delete')
			post.delete()
			return redirect('post_list')

		#Submitting in previewing post
		if 'prev_submit' in request.POST:
			print('Preview_Submit')
			post.text = post.draft
			post.save()
			return redirect('blog.views.blog_post', post_id=post_id)

		#'Edit' in previewing post
		if 'prev_edit' in request.POST:
			print('prev_edit')
			draftForm = editDraftPostForm(instance=post)
			return render(request, 'post_edit.html', {'form': draftForm})

		#Cancel is selected
		if 'cancel' in request.POST:
			print('cancel')
			return redirect('blog.views.blog_post', post_id=post_id)

	else:
		form = PostForm(instance=post)
			
	form = PostForm(instance=post)
	print('no condition met')
	return render(request, 'post_edit.html', {'form': form})
	

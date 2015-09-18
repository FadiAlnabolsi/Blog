from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, Http404, HttpResponseNotFound
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from blog.models import Post
from blog.forms import initialPostForm, editPostForm, editDraftPostForm

# viewing a single blog post
def blog_post(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		print('Active: %s' % post.active)
		print('User Authenticated: %s' % request.user.is_superuser)

		#only admins can view inactive posts
		if (post.active == False) and (request.user.is_superuser):
			return render(request, 'single_post.html', {'post':post})

		if (post.active == False) and (request.user.is_superuser == False):
			return HttpResponseNotFound('<h1>Page not found</h1>')

		return render(request, 'single_post.html', {'post':post})

	except Exception as e:
		return HttpResponseNotFound('<h1>Page not found</h1>')

# page to view all posts
def post_list(request):
	# authenticated users see active and inactive posts
	# regular users just see active posts
	if request.user.is_authenticated():
		print('authenticated')
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
		return render(request, 'blog.html', {'blogPosts':blogPosts})
	
	else:
		print('not authenticated')
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
	if request.method =='POST':
		form = initialPostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			#post.author = request.user
			post.draft = form['text']
			post.published_date = timezone.now()
			post.save()
			return redirect('blog.views.blog_post', post_id=post.id)

	else:
		form = initialPostForm()
		
	return render(request, 'post_edit.html', {'form': form})

# modifying an already-made post
def post_edit(request, post_id):
	post = get_object_or_404(Post, id=post_id)
	form = editPostForm(request.POST, instance=post)
	editForm = editDraftPostForm(request.POST, instance=post)
	textHolder = post.text

	#initial post/form
	if form.is_valid():
		print('Form Is valid')
		if request.method == 'POST':
			if 'submit' in request.POST:
				print('Form Submit')
				post = form.save(commit=False)
				post.draft = form.data['text']
				post.published_date = timezone.now()
				post.save()

				return redirect('blog.views.blog_post', post_id=post_id)

			if 'preview' in request.POST:
				print('Form Preview')
				post.draft = form.data['text']
				post.save()
				post.text = textHolder
				post.save()
				return render(request, 'preview_post.html', {'post':post})

			if 'delete' in request.POST:
				print('Form Delete')
				post.delete()
				return redirect('post_list')

	#form for edting a post (holds the draft)
	elif editForm.is_valid():
		print('Edit Form Is Valid')
		if request.method == 'POST':
			if 'submit' in request.POST:
				print('Edit Form Submit')
				post = editForm.save(commit=False)
				post.text = form.data['draft']
				post.published_date = timezone.now()
				post.save()
				return redirect('blog.views.blog_post', post_id=post_id)

			if 'preview' in request.POST:
				print('Edit Form Preview')
				post.save()
				return render(request, 'preview_post.html', {'post':post})

			if 'delete' in request.POST:
				print('Edit Form Delete')
				post.delete()
				return redirect('post_list')

	#Delete in previewing post
	elif 'delete' in request.POST:
		print('Global Delete')
		post.delete()
		return redirect('post_list')

	#Submitting in previewing post
	elif 'prev_submit' in request.POST:
		print('Preview_Submit')
		post.text = post.draft
		post.save()
		return redirect('blog.views.blog_post', post_id=post_id)

	#'Edit' in previewing post
	elif 'prev_edit' in request.POST:
		print('Preview_Edit')
		draftForm = editDraftPostForm(instance=post)
		return render(request, 'post_edit_draft.html', {'form': draftForm})

	else:
		form = editPostForm(instance=post)
			
	form = editPostForm(instance=post)
	print('no condition met')
	return render(request, 'post_edit.html', {'form': form})
	

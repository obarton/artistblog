# Create your views here.
from datetime import datetime
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from artistblog.models import Blog
from artistblog.forms import BlogForm
from artistblog.forms import ArtistForm, ArtistProfileForm
from artistblog.forms import UserForm, UserProfileForm

def index(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for extample.
	context = RequestContext(request)

	blog_list = Blog.objects.all()
	context_dict = {'blogs': blog_list}

	if request.session.get('last_visit'):
		# The session has a value for last visit
		last_visit_time = request.session.get('last_visit')
		visits = request.session.get('visits', 0)

		if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days >0:
			request.session['visits'] = visits + 1
			request.session['last_visit'] = str(datetime.now())

	else:
		# The get returns None, and the session does not have a
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = 1
	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render_to_response('artistblog/index.html', context_dict, context)

def about(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)

	# Construct a dictionary to pass the template engine as its context.
	# Note the key boldmessage is the same as {{ aboutmessage }} in the template!
	context_dict = {'aboutmessage': "Here is the about message"}

	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render_to_response('artistblog/about.html', context_dict, context)

def register(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)
	# Return a rendered response to send to the client.
	# We make use of the shortcut function to make our lives easier.
	# Note that the first parameter is the template we wish to use.
	return render_to_response('artistblog/register.html', {}, context)



def register_artist(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)

	registered = False

	if request.method == 'POST':
		artist_form = ArtistForm(data=request.POST)
		artist_profile_form = ArtistProfileForm(data=request.POST)

		if artist_form.is_valid() and artist_profile_form.is_valid():
			artist = artist_form.save()

			artist.set_password(artist.password)
			artist.save()

			artistprofile = artist_profile_form.save(commit=False)
			artistprofile.user = artist

			if 'picture' in request.FILES:
				artistprofile.picture = request.FILES['picture']

			profile.save()

			registered = True

		else:
			print artist_form.errors, artist_profile_form.errors
	else:
		artist_form = ArtistForm()
		artist_profile_form = ArtistProfileForm()


	# Return a rendered response to send to the client.
	return render_to_response('artistblog/registerartist.html', 
		{'artist_form':artist_form,
		'artist_profile_form':artist_profile_form}, context)

def register_blog(request):
	# Request the context of the request.
	# The context contains information such as the client's machine details, for example.
	context = RequestContext(request)

	registered = False

	if request.method == 'POST':
		blog_form = BlogForm(data=request.POST)

		if blog_form.is_valid():
			blog = blog_form.save()

			blog.set_password(blog.password)
			blog.save()

			registered = True

		else:
			print blog_form.errors
	else:
		blog_form = BlogForm()


	# Return a rendered response to send to the client.
	return render_to_response('artistblog/registerblog.html', {'blog_form':blog_form}, context)

def user_login(request):
	# Like before, obtain the context for the user's request.
	context = RequestContext(request)
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST['username']
		password = request.POST['password']

		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)

		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homeBlog.
				login(request, user)
				return HttpResponseRedirect('/artistblog/')
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your artistblog account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	# The request is not a HTTP POST, so display the login form.
	# This scenario would most likely be a HTTP GET.
	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render_to_response('artistblog/login.html', {}, context)

@login_required
def restricted(request):
	return HttpResponse("Since you're logged in, you can see this text!")

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)

	# Take the user back to the homeBlog.
	return HttpResponseRedirect('/artistblog/')

def encodeURL(name):
	url = name.replace(' ', '_')
	return url

def decodeURL(url):
	name = url.replace('_', ' ')
	return name
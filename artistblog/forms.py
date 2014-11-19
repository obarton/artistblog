from django import forms
from django.contrib.auth.models import User
from artistblog.models import Artist, ArtistProfile, Blog, UserProfile

class ArtistForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Please enter the Artist name.")
	genre = forms.CharField(max_length=128, help_text="Please enter the genre.")
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	# An inline class to provide additional information on the form.
	class Meta:
		# Provide an association between the ModelForm and a model.
		model = Artist

class BlogForm(forms.ModelForm):
	title = forms.CharField(max_length=128, help_text="Please enter the title of the Blog.")
	url = forms.URLField(max_length=200, help_text="Please enter the URL of the Blog.")
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		# Provide an association between the ModelForm and a model
		model = Blog

		# What fields do we want to include in our form?
		# This way we don't need every field in the model present.
		# Some fields may allow NULL values, so we may not want to include them.
		# Here, we are hiding the foreign key.
		fields = ('title', 'url', 'views')

	def clean(self):
		cleaned_data = self.cleaned_data
		url = cleaned_data.get('url')

		# If url is not empty and doesn't start with 'http://', prepend 'http://'
		if url and not url.startswith('http://'):
			url = 'http://' + url
			cleaned_data['url'] = url

		return cleaned_data

class ArtistProfileForm(forms.ModelForm):
	website = forms.URLField(help_text="Please enter your website.", required=False)
	picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
	
	class Meta:
		model = ArtistProfile
		fields = ['website', 'picture']

class UserForm(forms.ModelForm):
	username = forms.CharField(help_text="Please enter a username.")
	email = forms.CharField(help_text="Please enter your email.")
	password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password.")

	class Meta:
		model = User
		fields = ['username', 'email', 'password']

class UserProfileForm(forms.ModelForm):
	website = forms.URLField(help_text="Please enter your website.", required=False)
	picture = forms.ImageField(help_text="Select a profile image to upload.", required=False)
	class Meta:
		model = UserProfile
		fields = ['website', 'picture']
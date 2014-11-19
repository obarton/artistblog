from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Artist(models.Model):
	name = models.CharField(max_length=128)
	genre = models.CharField(max_length=128)
	likes = models.IntegerField(default=0)
	# song_folder = models.FilePathField()

	def __unicode__(self):
		return self.name

class Blog(models.Model):
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __unicode__(self):
		return self.title

class ArtistProfile(models.Model):
	artist = models.OneToOneField(User)

	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='artist_pictures', blank=True)

	def __unicode__(self):
		return self.artist.username

class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance
	user = models.OneToOneField(User)

	# The additional attributes we wish to include.
	website = models.URLField(blank=True)
	picture = models.ImageField(upload_to='user_images',blank=True)

	# Override the __unicode__() method to return out something meaningful!
	def __unicode__(self):
		return self.user.username

def get_file_name(instance, original_filename):
	return os.path.join(MEDIA_ROOT, 'mp3', instance.artist.song_folder)

class Mp3(models.Model):
	artist = models.ForeignKey('Artist')	 
	file = models.FileField(upload_to=get_file_name)


from django.contrib import admin
from artistblog.models import Artist, ArtistProfile, Blog, UserProfile

class BlogAdmin(admin.ModelAdmin):
	list_display = ('title', 'views','url')

admin.site.register(Artist)
admin.site.register(Blog, BlogAdmin)
admin.site.register(UserProfile)
admin.site.register(ArtistProfile)
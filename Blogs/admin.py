from django.contrib import admin
from .models import categories, tags, posts, comments

# Register your models here.
admin.site.register(categories)
admin.site.register(tags)
admin.site.register(posts)
admin.site.register(comments)
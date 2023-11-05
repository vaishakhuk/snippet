from django.contrib import admin
from .models import TextSnippet, Tag
# Register your models here.

admin.site.register(TextSnippet)
admin.site.register(Tag)
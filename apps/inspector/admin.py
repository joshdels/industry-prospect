from django.contrib import admin

from .models import Prospect, Business, Tag, Industry, ProspectInput

admin.site.register(Business)
admin.site.register(Prospect)
admin.site.register(ProspectInput)
admin.site.register(Tag)
admin.site.register(Industry)

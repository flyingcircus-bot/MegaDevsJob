from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Post)
admin.site.register(Review)
admin.site.register(Apply)
admin.site.register(ApplyItem)
admin.site.register(ManageInfo)

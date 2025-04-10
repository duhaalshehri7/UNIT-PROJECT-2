from django.contrib import admin
from .models import CustomUser,DesignerPost,DesignerPostImage,DesignerProfile
# Register your models here.

admin.site.register(CustomUser)

admin.site.register(DesignerPost)
admin.site.register(DesignerPostImage)

admin.site.register(DesignerProfile)


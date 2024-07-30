from django.contrib import admin

from .models import Artisan, PortfolioPhoto, Client, Administrateur, Localisation, UserProfile, Metier, Users
# Register your models here.
from django.utils.html import format_html
admin.site.register(Artisan)
admin.site.register(PortfolioPhoto)
admin.site.register(Client)
admin.site.register(Administrateur)
admin.site.register(Localisation)

# class UserProfileAdmin(admin.ModelAdmin):
    # def thumbnail(self,Object):
    #     return format_html('<img src="{}" width="30" style= "border-raduis: 50%;" />'.format(Object.photo_de_profil.url))
    # thumbnail.short_description = ''
admin.site.register(UserProfile)

admin.site.register(Metier)
admin.site.register(Users)
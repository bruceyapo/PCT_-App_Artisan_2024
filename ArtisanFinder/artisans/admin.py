from django.contrib import admin

from .models import Artisan, PortfolioPhoto, Client, Administrateur, Localisation, UserProfile, Metier, Users
# Register your models here.
admin.site.register(Artisan)
admin.site.register(PortfolioPhoto)
admin.site.register(Client)
admin.site.register(Administrateur)
admin.site.register(Localisation)
admin.site.register(UserProfile)
admin.site.register(Metier)
admin.site.register(Users)
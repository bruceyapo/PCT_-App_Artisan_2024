from django.contrib import admin

from .models import Artisan, PortfolioPhoto, InscriptionClient
# Register your models here.
admin.site.register(Artisan)
admin.site.register(PortfolioPhoto)
admin.site.register(InscriptionClient)
from django.contrib import admin

from ArtisanFinder import settings

from .models import Artisan, ContratClientArtisan, PortfolioPhoto, Client, Administrateur, Localisation, Tache, UserProfile, Metier, Users
# Register your models here.
from django.utils.html import format_html
class ArtisanAdmin(admin.ModelAdmin):
    list_display = ('id','Nom', 'Prenom', 'genre', 'Metier', 'IdUser')
admin.site.register(Artisan, ArtisanAdmin)

class UserPortfolioPhotoAdmin(admin.ModelAdmin):
    def thumbnail(self,Object):
        return format_html('<img src="{}" width="50" style= "border-raduis: 50%;" />'.format(Object.media.url))
    thumbnail.short_description = ''
    list_display = ('user','thumbnail', 'DateAjout')
admin.site.register(PortfolioPhoto,UserPortfolioPhotoAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('Nom', 'Prenoms', 'Ville', 'Commune', 'IdUser')
admin.site.register(Client, ClientAdmin)

class ContratClientArtisanAdmin(admin.ModelAdmin):
    list_display = ('client', 'artisan', 'metier')
admin.site.register(ContratClientArtisan, ContratClientArtisanAdmin)

admin.site.register(Administrateur)

class LocalisationAdmin(admin.ModelAdmin):
    list_display = ('user', 'Longitude', 'Latitude', 'Details')
admin.site.register(Localisation, LocalisationAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        # Chemin de l'image par défaut
        default_image_url = settings.STATIC_URL + 'artisanfinder/images/Image1.png'
        
        # Vérifier si une photo de profil est associée
        if obj.photo_de_profil and obj.photo_de_profil.url:
            image_url = obj.photo_de_profil.url
        else:
            image_url = default_image_url
        
        return format_html('<img src="{}" width="50" style="border-radius: 50%;" />', image_url)
# artisans/static/artisanfinder/images/Image1.png
    thumbnail.short_description = 'Photo de Profil'
    list_display = ('thumbnail', 'user', 'Ville', 'Commune', 'Entreprise', 'Annee_experience')
admin.site.register(UserProfile, UserProfileAdmin)

class MetierAdmin(admin.ModelAdmin):
    def thumbnail(self,Object):
        return format_html('<img src="{}" width="50" style= "border-raduis: 50%;" />'.format(Object.icon.url))
    thumbnail.short_description = ''
    list_display = ('thumbnail','Nom')
admin.site.register(Metier, MetierAdmin)

class TacheAdmin(admin.ModelAdmin):
    list_display = ('metier', 'description')
admin.site.register(Tache, TacheAdmin)

class UsersAdmin(admin.ModelAdmin):
    list_display = ('Telephone', 'email', 'password', 'roles','date_joined', 'last_login', 'is_admin', 'is_staff', 'is_superadmin', 'is_active')
admin.site.register(Users, UsersAdmin)
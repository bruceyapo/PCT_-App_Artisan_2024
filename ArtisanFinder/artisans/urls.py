from django.contrib import admin
from django.urls import path
from . import views 
# from django.conf import settings
# from django.conf.urls.static import static
# # from django.contrib.auth import authenticate, login
# # from .forms import LoginForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil_view, name='home'),
    path('services/', views.services_view, name='services'),
    path('artisan/', views.trouverArtisan_view, name='artisan'),
    path('artisan/details/<int:artisan_id>/', views.artisan_details_view, name='artisan-details'),
    # path('artisan/<int:id>/details/', views.artisan_details_view, name='artisan_details'),
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('espaceArtisan/', views.espaceArtisan_view, name='espace-artisan'),
    path('contact/', views.contact_view, name='contact'),
    path('apropos/', views.apropos_view, name= 'apropos'),
    path('cgu/',views.cgu_view, name= 'cgu'),
    path('cgv/', views.cgv_view, name= 'cgv'),
    path('mentions-legales/', views.mentions_view, name= 'mentions-legales'),
    path('vieprivee/', views.vieprivee_view, name= 'vieprivee'),
    path('equipe/', views.equipe_view, name = 'equipe'),
    path('inscription/',views.inscription_view, name='inscription'),
    # path('register/', views.profile_view, name='register'),
    path('password-oublie/', views.passwor_oublie_view, name='password-oublie'),
    path('choix/', views.choix_view, name= 'choix-inscription'),
    path('clientRegistration/', views.inscription_client_view, name= 'client-inscription'),
    # path('profil/<int:artisan_id>/', views.profile_view, name='profil'),
    # path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('artisan/change-password/', views.change_password_view, name='change_password_view'),
    path('supp_portfolio/<int:portfolio_id>', views.supp_portfolio, name='supp_portfolio'),
    path('profil/', views.profilArtisan_view, name='profil'),
    path('plombier/', views.plombier_view, name= 'plombier'),
    path('menuisier/', views.menuisier_view, name= 'menuisier'),
    path('bijoutier/', views.bijoutier_view, name= 'bijoutier'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
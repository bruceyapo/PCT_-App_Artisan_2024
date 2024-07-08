from django.urls import path

from . import views 

# from .views import inscription

urlpatterns = [
    path('', views.accueil_view, name='home'),
    path('services/', views.services_view, name='services'),
    path('artisan/', views.trouverArtisan_view, name='artisan'),
    path('connexion/', views.connexion_view, name='connexion'),
    path('espaceArtisan/', views.espaceArtisan_view, name='espace-artisan'),
    path('contact/', views.contact_view, name='contact'),
    path('apropos/', views.apropos_view, name= 'apropos'),
    path('cgu/',views.cgu_view, name= 'cgu'),
    path('cgv/', views.cgv_view, name= 'cgv'),
    path('mentions-legales/', views.mentions_view, name= 'mentions-legales'),
    path('vieprivee/', views.vieprivee_view, name= 'vieprivee'),
    path('equipe/', views.equipe_view, name = 'equipe'),
    path('inscription/',views.inscription_view, name='inscription'),
    path('register/', views.inscription, name='register'),
    path('password-oublie/', views.passwor_oublie_view, name='password-oublie'),
     
    ]
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
# from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from .models import Artisan, PortfolioPhoto
from .forms import ArtisanForm, PortfolioPhotoForm,ArtisanSignUpForm, LoginForm, InscriptionClientForm
from django.contrib.auth.forms import PasswordChangeForm








# from ..auth_app.forms import ContactForm

def accueil_view(request) :
   return render(request, 'accueil.html')



def trouverArtisan_view(request) :
   return render(request, 'trouver_Artisan.html')


def services_view(request) : 
   return render(request,'services.html')

def choix_view(request) : 
   return render(request,'choix_inscription.html')

def inscriptionClient_view(request) : 
   return render(request,'inscription_client.html')

def profile_view(request) : 
   return render(request,'profil.html')

def edit_profile_view(request, artisan_id):
    artisan = get_object_or_404(Artisan, id=artisan_id)
    if request.method == 'POST':
        form = ArtisanForm(request.POST, instance=artisan)
        if form.is_valid():
            form.save()
            return redirect('profil', artisan_id=artisan.id)
    else:
        form = ArtisanForm(instance=artisan)
    return render(request, 'edit_profil.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            numero_de_telephone = form.cleaned_data['numero_de_telephone']
            mot_de_passe = form.cleaned_data['mot_de_passe']
            se_souvenir_de_moi = form.cleaned_data['se_souvenir_de_moi']
            
            user = authenticate(request, numero_de_telephone=numero_de_telephone, password=mot_de_passe)
            
            if user is not None:
                login(request, user)
                if not se_souvenir_de_moi:
                    request.session.set_expiry(0)  # Session expire à la fermeture du navigateur
                return redirect('profil', artisan_id=user.id)
            else:
                form.add_error(None, "Numéro de téléphone ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'connexion.html', {'form': form})

def contact_view(request):
   if request.method == 'POST':
      nom = request.POST.get('nom')
      prenom = request.POST.get('prenom')
      email = request.POST.get('email')
      objet = request.POST.get('objet')
      message = request.POST.get('message')
      # Construire le contenu de l'e-mail
      email_subject = f"Nouvelle demande de contact : {objet}"
      email_message = f"Nom : {nom}\nPrénom : {prenom}\nE-mail : {email}\n\nMessage :\n{message}"

        # Envoyer l'e-mail
      send_mail(
            email_subject,
            email_message,
            'your-email@example.com',  # L'adresse e-mail de l'expéditeur
            ['destination-moussa8.kone@uvci.edu.ci'],  # Liste des destinataires
            fail_silently=False,
        )

      # Traitez les données du formulaire (par exemple, en les enregistrant dans la base de données)

      return HttpResponse('Merci pour votre message !')
   return render(request, 'contact.html')
 
 
   
   

def espaceArtisan_view(request):
   return render(request,'espace_artisan.html')

def connexion_view(request):
   return render(request,'connexion.html')

def apropos_view(request):
   return render(request,'apropos.html')
   
def mentions_view(request):
   return render(request,'mentions.html')

def cgu_view(request):
   return render(request,'cgu.html')

def cgv_view(request):
   return render(request,'cgv.html')

def vieprivee_view(request):
   return render(request,'vieprivee.html')

def equipe_view(request):
   return render(request,'equipe.html')

def inscription_view(request):
   return render(request,'inscription_artisan.html')

def passwor_oublie_view(request):
   return render(request,'password_oublie.html')

def inscription_view(request):
    if request.method == 'POST':
        form = ArtisanSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_view', artisan_id=user.id)
    else:
        form = ArtisanSignUpForm()
    return render(request, 'inscription_artisan.html', {'form': form})







def inscription_client_view(request):
    if request.method == 'POST':
        form = InscriptionClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Rediriger vers une page de succès d'inscription
    else:
        form = InscriptionClientForm()

    return render(request, 'inscription_client.html', {'form': form})

@login_required
def profile_view(request, artisan_id):
    artisan = get_object_or_404(Artisan, id=artisan_id)
    return render(request, 'profil.html', {'artisan': artisan})

@login_required
def edit_profile_view(request, artisan_id):
    artisan = get_object_or_404(Artisan, id=artisan_id)
    if request.method == 'POST':
        form = ArtisanForm(request.POST, request.FILES, instance=artisan)
        if form.is_valid():
            form.save()
            return redirect('profil', artisan_id=artisan.id)
    else:
        form = ArtisanForm(instance=artisan)
    return render(request, 'edit_profil.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profil', artisan_id=request.user.id)
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'edit_password.html', {'form': form})

@login_required
def add_portfolio_photo_view(request, artisan_id):
    artisan = get_object_or_404(Artisan, id=artisan_id)
    if request.method == 'POST':
        form = PortfolioPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            artisan.portfolio_photos.add(photo)
            return redirect('profil', artisan_id=artisan.id)
    else:
        form = PortfolioPhotoForm()
    return render(request, 'add_portfolio.html', {'form': form})










# # Create your views here.
# def inscription(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('connexion')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'inscription.html', {'form': form})

# def connexion(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('acceuil')
#         else:
#             messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
#     return render(request, 'connexion.html')

# @login_required
# def acceuil(request):
#     return render(request, 'acceuil.html')

# def deconnexion(request):
#     logout(request)
#     return redirect('connexion')
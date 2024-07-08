from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm 
# from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.core.mail import send_mail


# from ..auth_app.forms import ContactForm

def accueil_view(request) :
   return render(request, 'accueil.html')



def trouverArtisan_view(request) :
   return render(request, 'trouver_Artisan.html')


def services_view(request) : 
   return render(request,'services.html')

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
   return render(request,'inscription.html')

def passwor_oublie_view(request):
   return render(request,'password_oublie.html')


def inscription(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'inscription.html', {'form': form})














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
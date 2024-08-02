import re
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm 
# from .forms import CustomUserCreationForm
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

# from .models import Artisan, PortfolioPhoto
# from .forms import ArtisanForm, PortfolioPhotoForm,ArtisanSignUpForm, LoginForm, InscriptionClientForm
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
import pandas as pd

from artisans.forms import ArtisanForm, ArtisanProfilForm, ArtisanSearchForm, LoginForm, PortfolioPhotoForm, UploadFileForm, UserForm, UserProfileForm
from artisans.models import Artisan, Localisation, Metier, PortfolioPhoto, UserProfile, Users









# from ..auth_app.forms import ContactForm

def plombier_view(request) :
   return render(request, 'services/plombier.html')


def menuisier_view(request) :
   return render(request, 'services/menuisier.html')

def bijoutier_view(request) :
   return render(request, 'services/bijoutier.html')




def accueil_view(request) :
    metier = Metier.objects.filter()[:4]
    context = {
        'metier': metier
    }
    return render(request, 'accueil.html', context)

from django.db.models import Q
from unidecode import unidecode

def normaliser_donnees():
    profiles = UserProfile.objects.all()
    for profile in profiles:
        profile.Ville = unidecode(profile.Ville)
        profile.Commune = unidecode(profile.Commune)
        profile.save()

# Exécute cette fonction pour mettre à jour les données en base

def nettoyer_chaine(chaine):
    # Remplace tout ce qui n'est pas un caractère alphabétique ou un espace par rien
    return unidecode(chaine).strip()

# def trouverArtisan_view(request):
#     metiers = Metier.objects.all()
#     artisans = Artisan.objects.all()
#     ville = request.GET.get('ville', '')
#     commune = request.GET.get('commune', '')
#     metier_id = request.GET.get('metier')
#     # Nettoyer les entrées utilisateur
#     ville = nettoyer_chaine(ville)
#     commune = nettoyer_chaine(commune)
#     if metier_id:
#         artisans = artisans.filter(Metier__id=metier_id)
#      # Filtrer les artisans en fonction de la ville et de la commune
#     if ville:
#         artisans = artisans.filter(Q(userprofile__Ville__icontains=ville))
#     if commune:
#         artisans = artisans.filter(Q(userprofile__Commune__icontains=commune))
#     context = {
#         'artisans': artisans,
#         'metiers': metiers,
#     }
        
#     return render(request, 'trouver_Artisan.html', context)


# def artisan_details_view(request, artisan_id):
#     artisan = get_object_or_404(Artisan, id=artisan_id)
#     userprofile = get_object_or_404(UserProfile, user=artisan)
#     PortPhoto = get_object_or_404(PortfolioPhoto, user=artisan)
    
#     try:
#         localisation = Localisation.objects.get(user=artisan)
#     except Localisation.DoesNotExist:
#         localisation = None
    
#     details = {
#         'name': f"{artisan.Nom} {artisan.Prenom}",
#         'metier': artisan.Metier.Nom if artisan.Metier else 'N/A',
#         'ville': userprofile.Ville if userprofile else 'N/A',
#         'commune': userprofile.Commune if userprofile else 'N/A',
#         'entreprise': userprofile.Entreprise if userprofile else 'N/A',
#         'description': userprofile.Descriptions if userprofile else 'N/A',
#         'experience': userprofile.Annee_experience if userprofile else 'N/A',
#         'photo': userprofile.photo_de_profil.url if userprofile and userprofile.photo_de_profil else None,
#         'media': PortPhoto.media.url if PortPhoto and PortPhoto.media else None,
#         'latitude': localisation.Latitude if localisation else 'N/A',
#         'longitude': localisation.Longitude if localisation else 'N/A'
#     }
    
#     return JsonResponse(details)

# def artisan_details_view(request, artisan_id):
#     artisan = get_object_or_404(Artisan, id=artisan_id)
#     print(artisan)
#     try:
#         localisation = Localisation.objects.get(user=artisan)
#     except Localisation.DoesNotExist:
#         localisation = None

#     user_profile = get_object_or_404(UserProfile, user=artisan)

#     details = {
#         'name': f'{artisan.Nom} {artisan.Prenom}',
#         'photo': user_profile.photo_de_profil.url if user_profile.photo_de_profil else '',
#         'metier': artisan.Metier.Nom if artisan.Metier else 'Non spécifié',
#         'ville': user_profile.Ville,
#         'commune': user_profile.Commune,
#         'entreprise': user_profile.Entreprise,
#         'description': user_profile.Descriptions,
#         'experience': user_profile.Annee_experience,
#         'latitude': localisation.Latitude if localisation else 'Non spécifié',
#         'longitude': localisation.Longitude if localisation else 'Non spécifié',
#     }
#     print(details)
#     return JsonResponse(details)

def artisan_details_view(request, artisan_id):
    artisan = get_object_or_404(Artisan, id=artisan_id)
    try:
        localisation = Localisation.objects.get(user=artisan)
    except Localisation.DoesNotExist:
        localisation = None
    user_profile = get_object_or_404(UserProfile, user=artisan)

    # Obtenez les compétences de l'artisan
    competencies = user_profile.Competence.all()
    details = {
        'name': f'{artisan.Nom} {artisan.Prenom}',
        'photo': user_profile.photo_de_profil.url if user_profile.photo_de_profil else '',
        'metier': artisan.Metier.Nom if artisan.Metier else 'Non spécifié',
        'telephone': artisan.IdUser.Telephone if artisan.IdUser else 'Non spécifié',
        'email': artisan.IdUser.email if artisan.IdUser else 'Non spécifié',
        'ville': user_profile.Ville,
        'commune': user_profile.Commune,
        'entreprise': user_profile.Entreprise,
        'description': user_profile.Descriptions,
        'experience': user_profile.Annee_experience,
        'latitude': localisation.Latitude if localisation else 'Non spécifié',
        'longitude': localisation.Longitude if localisation else 'Non spécifié',
        'competencies': [comp.description for comp in competencies]  # Ajouter les compétences ici
    }

    return JsonResponse(details)

# def artisan_details_view(request, id):
#     artisan = get_object_or_404(Artisan, id=id)
#     localisation = Localisation.objects.filter(user=artisan).first()
#     profile = UserProfile.objects.filter(user=artisan).first()

#     data = {
#         'name': f'{artisan.Nom} {artisan.Prenom}',
#         'activity': artisan.Metier.Nom,
#         'description': profile.Descriptions if profile else '',
#         'entreprise': profile.Entreprise if profile else '',
#         'experience': profile.Annee_experience if profile else '',
#         'photo': profile.photo_de_profil.url if profile and profile.photo_de_profil else '',
#         'portfolio': [photo.media.url for photo in PortfolioPhoto.objects.filter(user=artisan)] if profile else [],
#         'latitude': float(localisation.Latitude) if localisation else '',
#         'longitude': float(localisation.Longitude) if localisation else '',
#     }

#     return JsonResponse(data)
# def trouverArtisan_view(request):
#     print("Requête reçue")
#     metiers = Metier.objects.all()
#     artisans = Artisan.objects.all()
#     ville = request.GET.get('ville', '')
#     commune = request.GET.get('commune', '')
#     metier_id = request.GET.get('metier')

#     print("Ville:", ville)
#     print("Commune:", commune)
#     print("Métier ID:", metier_id)

#     ville = nettoyer_chaine(ville)
#     commune = nettoyer_chaine(commune)

#     if metier_id and ville and commune:
#         artisans = artisans.filter(Metier__id=metier_id, userprofile__Ville__icontains=ville, userprofile__Commune__icontains=commune)
    
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         print("Requête AJAX détectée")
#         data = []
#         for artisan in artisans:
#             try:
#                 localisation = Localisation.objects.filter(user=artisan).first()
#                 if localisation:
#                     data.append({
#                         'name': f'{artisan.Nom} {artisan.Prenom}',
#                         'lat': float(localisation.Latitude),
#                         'lng': float(localisation.Longitude),
#                         'activity': artisan.Metier.Nom
#                     })
#             except Exception as e:
#                 print('Erreur lors de la récupération de la localisation:', e)
#         return JsonResponse(data, safe=False)
    
#     context = {
#         'artisans': artisans,
#         'metiers': metiers,
#     }
#     return render(request, 'trouver_Artisan.html', context)

def trouverArtisan_view(request):
    metiers = Metier.objects.all()
    artisans = Artisan.objects.all()
    ville = request.GET.get('ville', '')
    commune = request.GET.get('commune', '')
    metier_id = request.GET.get('metier')

    ville = nettoyer_chaine(ville)
    commune = nettoyer_chaine(commune)

    if metier_id and ville and commune:
        artisans = artisans.filter(Metier__id=metier_id, userprofile__Ville__icontains=ville, userprofile__Commune__icontains=commune)
    elif metier_id:
        artisans = artisans.filter(Metier__id=metier_id)
    elif ville:
        artisans = artisans.filter(userprofile__Ville__icontains=ville)
    elif commune:
        artisans = artisans.filter(userprofile__Commune__icontains=commune)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for artisan in artisans:
            try:
                localisation = Localisation.objects.get(user=artisan)
                data.append({
                    'id': artisan.id,
                    'name': f'{artisan.Nom} {artisan.Prenom}',
                    'lat': float(localisation.Latitude),
                    'lng': float(localisation.Longitude),
                    'activity': artisan.Metier.Nom
                })
            except Localisation.DoesNotExist:
                continue
        return JsonResponse(data, safe=False)
    
    context = {
        'artisans': artisans,
        'metiers': metiers,
    }
    return render(request, 'trouver_Artisan.html', context)
def services_view(request) : 
    metier = Metier.objects.all()
    context = {
        'metier': metier
    }
    return render(request,'services.html', context)

def choix_view(request) : 
   return render(request,'choix_inscription.html')

def inscriptionClient_view(request) : 
   return render(request,'inscription_client.html')

def profile_view(request) : 
   return render(request,'profil.html')

@login_required(login_url='login')
def profilArtisan_view(request):
    user = request.user
    utilisateur = get_object_or_404(Users, id=user.id)
    artisan = get_object_or_404(Artisan, IdUser=utilisateur)
    userprofile, created = UserProfile.objects.get_or_create(user=artisan)
    if request.method == 'POST':
        # Initialiser les formulaires ici pour garantir qu'ils soient définis dans tous les cas
        user_form = ArtisanProfilForm(request.POST, instance=artisan)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile, user=artisan)
        emailform = UserForm(request.POST, instance=utilisateur)
        Portform = PortfolioPhotoForm(request.POST, request.FILES)
        if 'submit_user_form' in request.POST:
            if user_form.is_valid() and profile_form.is_valid() and emailform.is_valid():
                user_form.save()
                profile_form.save()
                normaliser_donnees()
                emailform.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('profil')
        elif 'submit_portform' in request.POST:
            
            if Portform.is_valid():
                portfolio_photo = Portform.save(commit=False)
                portfolio_photo.user = artisan
                portfolio_photo.save()
                messages.success(request, 'Ajouter avec succes')
                return redirect('profil')
            else:
                messages.error(request, 'Error updating profile')
        else:
            Portform = PortfolioPhotoForm()
    else:
        user_form = ArtisanProfilForm(instance=artisan)
        profile_form = UserProfileForm(instance=userprofile, user=artisan)
        emailform = UserForm(instance=utilisateur)
        Portform = PortfolioPhotoForm()
    
    list_port = PortfolioPhoto.objects.filter(user=artisan).order_by('DateAjout')
    competencies = userprofile.Competence.all()
    context = {
        'utilisateur': utilisateur,
        'artisan': artisan,
        'userprofile': userprofile,
        'user_form': user_form,
        'Portform': Portform,
        'competencies':competencies,
        'profile_form': profile_form,
        'emailform': emailform,
        'list_port': list_port
    }
    return render(request, 'profil_artisan.html', context)
@login_required
def supp_portfolio(request, portfolio_id):
    portfolio = PortfolioPhoto.objects.get(id=portfolio_id)
    portfolio.delete()
    messages.success(request, 'portfolio retiré avec succes')
    return redirect('profil')
# def profilArtisan_view(request) :
#     user = request.user
#     # Récupérer l'utilisateur connecté
#     utilisateur = get_object_or_404(Users, id=request.user.id)
#     # Utiliser la clé étrangère pour récupérer l'artisan associé
#     artisan = get_object_or_404(Artisan, IdUser=utilisateur)
#     # Récupérer ou créer le UserProfile associé au client
#     userprofile, created = UserProfile.objects.get_or_create(user=artisan)
#     if request.method == 'POST':
#         user_form = ArtisanProfilForm(request.POST, instance=artisan)
#         profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
#         emailform = UserForm(request.POST, instance=utilisateur)
#         if user_form.is_valid() and profile_form.is_valid() and emailform.is_valid():
#             user_form.save()
#             profile_form.save()
#             emailform.save()
#             messages.success(request, 'Profile updated successfully')
#             context ={
#                 'utilisateur': utilisateur,
#                 'artisan': artisan,
#                 # 'Portform': Portform,
#                 'userprofile':userprofile,
#                 'user_form': user_form,
#                 'profile_form': profile_form,
#                 'emailform': emailform,
#             }
#             return render(request, 'profil_artisan.html', context)
#         else:
#             messages.error(request, 'Error updating profile')
#     else:
#         user_form = ArtisanProfilForm(instance=artisan)
#         profile_form = UserProfileForm(instance=userprofile)
#         emailform = UserForm(instance=utilisateur)
        
#     # if request.method == 'POST':
#     #     Portform = PortfolioPhotoForm(request.POST, request.FILES)
#     #     if Portform.is_valid():
#     #         Portform.save()
#     #         messages.success(request, 'Ajouter avec succes')
#     #         return redirect('profil')
#     #     else:
#     #         messages.error(request, 'Error updating profile')
#     # else:
#     #     Portform = PortfolioPhotoForm()
#     context ={
#         'utilisateur': utilisateur,
#         'artisan': artisan,
#         # 'Portform': Portform,
#         'userprofile':userprofile,
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'emailform': emailform,
#     }
#     return render(request, 'profil_artisan.html', context)

def deconnexion(request):
    logout(request)
    messages.success(request,f"vous êtes déconnecté")
    return redirect('login')  # Redirige vers la page de connexion après la déconnexion
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            Telephone = form.cleaned_data['Telephone']
            password = form.cleaned_data['password']
            
            user = authenticate(request, Telephone=Telephone, password=password)
            
            if user is not None:
                login(request, user)
                # if not se_souvenir_de_moi:
                #     request.session.set_expiry(0)  # Session expire à la fermeture du navigateur
                if user.roles == 'Artisan':
                    next_url = request.GET.get('next', reverse('profil'))
                    return redirect(next_url)
                elif user.roles == 'Client':
                    next_url = request.GET.get('next', reverse('profilClient'))
                    return redirect(next_url)
            else:
                form.add_error(None, "Numéro de téléphone ou mot de passe incorrect.")
    else:
        form = LoginForm()
    context = {'form': form}
    return render(request, 'connexion.html', context)

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

from django.utils.crypto import get_random_string

from django.utils.text import slugify
def handle_uploaded_file(file):
    if file.name.endswith('.csv'):
        data = pd.read_csv(file, sep=";")
    elif file.name.endswith('.xlsx'):
        data = pd.read_excel(file)
    else:
        raise ValueError("Le fichier n'est pas un format supporté. Seuls CSV et Excel sont acceptés.")
    
    df = data.copy()

    # Afficher les noms de colonnes pour le débogage
    print(df.columns)

    # Normalisation des noms de colonnes pour éviter les erreurs de casse ou d'espaces
    df.columns = df.columns.str.strip().str.lower()

    # Vérifiez si la colonne 'Nom' (ou sa version normalisée) existe
    if 'nom' not in df.columns:
        raise KeyError("La colonne 'Nom' n'a pas été trouvée dans le fichier.")
    
    for index, row in df.iterrows():
        # Split le nom pour obtenir prenoms et nom
        name_parts = row['nom'].split(' ', 1)
        Prenom = name_parts[0]
        Nom = name_parts[1] if len(name_parts) > 1 else ''  # Gère les noms sans prénom
        Telephone = row['telephone']
        
        # Définir le rôle par défaut et le mot de passe par défaut
        roles = 'Artisan'
        password = '123456789'
        
        # Créer ou récupérer l'utilisateur
        utilisateur, created = Users.objects.get_or_create(
            Telephone=Telephone,
            defaults={
                'roles': roles,
                'is_active': True,
            }
        )
        # Créer ou récupérer le métier
        metier, created_metier = Metier.objects.get_or_create(
            Nom=row['activite'],
            defaults={'Nom': row['activite']}
        )
        if created:
            # Si l'utilisateur est créé, définir le mot de passe
            utilisateur.set_password(password)
            utilisateur.save()

        # Créer ou récupérer l'artisan
        artisan_instance, created = Artisan.objects.get_or_create(
            Nom=Nom,
            Prenom=Prenom,
            defaults={'genre': row['sexe'], 'Metier': metier, 'IdUser': utilisateur}
        )
        
        description = 'Lorem ipsum dolor sit amet consectetur adipisicing elit...'

        # Créer ou récupérer le profil utilisateur
        profile, created_user_profile = UserProfile.objects.get_or_create(
            user=artisan_instance,
            defaults={
                'Ville': row['ville'],
                'Commune': row['commune'],
                'Annee_experience': 3,
                'Descriptions': description,
            }
        )
        localisation, created_localisation = Localisation.objects.get_or_create(
            user=artisan_instance,
            defaults={
                'Longitude': row['longitude'],
                'Latitude': row['latitude'],
                'Details': description,
            }
        )      

def apropos_view(request):
    # user = request.user.id
    #  # Récupérer l'utilisateur connecté
    # utilisateur = get_object_or_404(Users, id=user)
    # artisan = get_object_or_404(Artisan, IdUser=utilisateur)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                # Traitement du fichier CSV avec Pandas
                handle_uploaded_file(file)
                messages.success(request, "enregistrée avec succès.")
                return render(request, 'apropos.html', {'form': form})

            elif file.name.endswith(('.xlsx', '.xls')):
                # Traitement du fichier Excel avec Pandas
                handle_uploaded_file(file)
                messages.success(request, "enregistrée avec succès.")
                return render(request, 'apropos.html', {'form': form})

            else:
                messages.warning(request, 'Le fichier doit être au format CSV ou excel')
    else:
        form = UploadFileForm()
    return render(request,'apropos.html', locals())
   
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

# def inscription_view(request):
#    return render(request,'inscription_artisan.html')

def passwor_oublie_view(request):
   return render(request,'password_oublie.html')

def inscription_view(request):
    if request.method == 'POST':
        form = ArtisanForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            messages.success(request, "Inscription effectuée avec succès !")
            return redirect('login')
    else:
        form = ArtisanForm()
    context = {
        'form': form
        }
    return render(request, 'inscription_artisan.html', context)







def inscription_client_view(request):
#     if request.method == 'POST':
#         form = InscriptionClientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')  # Rediriger vers une page de succès d'inscription
#     else:
#         form = InscriptionClientForm()

#     return render(request, 'inscription_client.html', {'form': form})

# @login_required
# def profile_view(request, artisan_id):
#     artisan = get_object_or_404(Artisan, id=artisan_id)
    return render(request, 'profil.html')

# @login_required
# def edit_profile_view(request, artisan_id):
#     # artisan = get_object_or_404(Artisan, id=artisan_id)
#     # if request.method == 'POST':
#     #     form = ArtisanForm(request.POST, request.FILES, instance=artisan)
#     #     if form.is_valid():
#     #         form.save()
#     #         return redirect('profil', artisan_id=artisan.id)
#     # else:
#     #     form = ArtisanForm(instance=artisan)
#     return render(request, 'edit_profil.html')

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
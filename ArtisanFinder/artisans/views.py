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

from artisans.forms import ArtisanForm, ArtisanProfilForm, ArtisanSearchForm, ClientForm, LoginForm, PortfolioPhotoForm, UploadFileForm, UserForm, UserProfileForm
from artisans.models import Artisan, Client, ContratClientArtisan, Localisation, Metier, PortfolioPhoto, Tache, UserProfile, Users









# from ..auth_app.forms import ContactForm

def plombier_view(request) :
   return render(request, 'services/plombier.html')

def normaliser_donnees():
    profiles = UserProfile.objects.all()
    for profile in profiles:
        profile.Ville = unidecode(profile.Ville)
        profile.Commune = unidecode(profile.Commune)
        profile.save()

def normaliser_donnees_client():
    clients = Client.objects.all()
    for client in clients:
        client.Ville = unidecode(client.Ville)
        client.Commune = unidecode(client.Commune)
        client.save()

# def profilClient(request):
#     user = request.user
#     utilisateur = get_object_or_404(Users, id=user.id)
#     client = get_object_or_404(Client, IdUser=utilisateur)
    
#     # Récupération des contrats associés au client
#     contrats = ContratClientArtisan.objects.filter(client=client)
#     # listArtisan = None
#     for contrat in contrats:
#         # Correction : Assurez-vous que vous filtrez avec un champ 'Metier' et non une chaîne
#         listArtisan = UserProfile.objects.filter(
#             Ville=client.Ville,
#             Commune=client.Commune,
#             user__Metier=contrat.metier  # Utilisation correcte du champ 'Metier'
#         )
#         # artisan = Artisan.objects.filter(user=listArtisan.artisan)
#         contratFinal = ContratClientArtisan.objects.get(client=client, metier=contrat.metier)
#         if contratFinal:
#             contratFinal.artisan = listArtisan.user
#             contratFinal.save()
    
#     context = {
#         'client': client,
#         'utilisateur': utilisateur,
#         'listArtisan': listArtisan,
#     }
#     return render(request, 'profil_client.html', context)
from django.views.decorators.http import require_POST

# @require_POST
# def update_artisan(request):
#     try:
#         contrat_id = request.POST.get('contrat_id')
#         artisan_id = request.POST.get('artisan_id')

#         contrat = ContratClientArtisan.objects.get(id=contrat_id)
#         artisan = UserProfile.objects.get(user_id=artisan_id)

#         contrat.artisan = artisan.user
#         contrat.save()

#         return JsonResponse({'success': True})
#     except (ContratClientArtisan.DoesNotExist, UserProfile.DoesNotExist) as e:
#         return JsonResponse({'error': str(e)}, status=400)
    
# def profilClient(request):
#     user = request.user
#     utilisateur = get_object_or_404(Users, id=user.id)
#     client = get_object_or_404(Client, IdUser=utilisateur)
    
#     # Récupération des contrats associés au client
#     contrats = ContratClientArtisan.objects.filter(client=client)
#     listArtisan = UserProfile.objects.none()  # Crée une QuerySet vide pour initialiser

#     for contrat in contrats:
#         # Filtrer les artisans basés sur la ville, la commune et le métier
#         artisans = UserProfile.objects.filter(
#             Ville=client.Ville,
#             Commune=client.Commune,
#             user__Metier=contrat.metier
#         )
#         listArtisan |= artisans  # Combine les QuerySets

#     context = {
#         'client': client,
#         'utilisateur': utilisateur,
#         'listArtisan': listArtisan,
#     }
#     return render(request, 'profil_client.html', context)


def profilClient(request):
    user = request.user
    utilisateur = get_object_or_404(Users, id=user.id)
    client = get_object_or_404(Client, IdUser=utilisateur)
    
    # Récupération des contrats associés au client
    contrats = ContratClientArtisan.objects.filter(client=client)
    listArtisan = UserProfile.objects.none()  # Crée une QuerySet vide pour initialiser

    for contrat in contrats:
        # Filtrer les artisans basés sur la ville, la commune et le métier
        artisans = UserProfile.objects.filter(
            Ville=client.Ville,
            Commune=client.Commune,
            user__Metier=contrat.metier
        )
        listArtisan |= artisans  # Combine les QuerySets
        # artisan = Artisan.objects.filter(user=listArtisan.artisan)
        # Mise à jour du champ artisan du contrat
        if artisans.exists():
            # On suppose que vous voulez associer le premier artisan trouvé
            contrat.artisan = artisans.first().user
            contrat.save()
        photos = PortfolioPhoto.objects.filter(user=artisans.first().user)
    context = {
        'client': client,
        'utilisateur': utilisateur,
        'listArtisan': listArtisan,
        'photos': photos,
    }
    return render(request, 'profil_client.html', context)


def metier_view(request, metier_id):
    taches = Tache.objects.filter(metier=metier_id)
    metier = Metier.objects.get(id=metier_id)
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            Telephone = form.cleaned_data['Telephone']
            password = form.cleaned_data['password']
            client_instance = form.save()  # Enregistrez le client
            
            # Normalisation des données du client
            normaliser_donnees_client()

            # Authentifiez l'utilisateur
            user = authenticate(request, Telephone=Telephone, password=password)

            if user is not None:
                login(request, user)

                # Récupérez les tâches sélectionnées
                selected_taches_ids = request.POST.getlist('taches')
                selected_taches = Tache.objects.filter(id__in=selected_taches_ids)

                # Créez un contrat
                Contrat = ContratClientArtisan(
                    client=client_instance,  # Assignez l'instance du client ici
                    metier_id=metier_id
                )
                Contrat.save()
                Contrat.tache.set(selected_taches)  # Assignez les tâches
                Contrat.save()

                messages.success(request, "Résultat de recherche !")
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Échec de l\'authentification'}, status=400)
        else:
            return JsonResponse({'error': 'Formulaire invalide'}, status=400)
    else:
        form = ClientForm()

    context = {
        'form': form,
        'taches': taches,
        'metier': metier,
        'metier_id': metier_id,
    }
    return render(request, 'services/metier.html', context)
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


def portfolio_photos_view(request, artisan_id):
    try:
        photos = PortfolioPhoto.objects.filter(user=artisan_id)
        
        dataMedia = {
            'portfolio': [photo.media.url for photo in photos]
        }
        return JsonResponse(dataMedia)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

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


# def trouverArtisan_view(request):
#     metiers = Metier.objects.all()
#     artisans = Artisan.objects.all()
#     ville = request.GET.get('ville', '')
#     commune = request.GET.get('commune', '')
#     metier_id = request.GET.get('metier')

#     ville = nettoyer_chaine(ville)
#     commune = nettoyer_chaine(commune)

#     if metier_id and ville and commune:
#         artisans = artisans.filter(Metier__id=metier_id, userprofile__Ville__icontains=ville, userprofile__Commune__icontains=commune)

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         data = []
#         for artisan in artisans:
#             try:
#                 localisation = Localisation.objects.get(user=artisan)
#                 data.append({
#                     'id': artisan.id,
#                     'name': f'{artisan.Nom} {artisan.Prenom}',
#                     'lat': float(localisation.Latitude),
#                     'lng': float(localisation.Longitude),
#                     'activity': artisan.Metier.Nom
#                 })
#             except Localisation.DoesNotExist:
#                 continue
#         return JsonResponse(data, safe=False)
    
#     context = {
#         'artisans': artisans,
#         'metiers': metiers,
#     }
#     return render(request, 'trouver_Artisan.html', context)


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
    # messages.success(request,f"vous êtes déconnecté")
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
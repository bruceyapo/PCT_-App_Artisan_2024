from django import forms
from .models import InscriptionClient, Artisan
from .models import Artisan, PortfolioPhoto, User, UserManager
from django.contrib.auth.forms import UserCreationForm


# Formulaire d'inscription Artisan:
class ArtisanForm(forms.ModelForm):
    class Meta:
        model = Artisan
        fields = [
            'nom', 'prenom', 'genre', 'numero_de_telephone', 'email', 'domaine_activite', 
            'ville_ou_commune', 'localisation_atelier', 'photo_de_profil', 'titres_diplomes',
            'annees_experience'
        ]

class PortfolioPhotoForm(forms.ModelForm):
    class Meta:
        model = PortfolioPhoto
        fields = ['photo']

# Formulaire de connexion :

class LoginForm(forms.Form):
    numero_de_telephone = forms.CharField(
        label='Numéro de téléphone',
        widget=forms.TextInput(attrs={'placeholder': 'Numéro de téléphone', 'class': 'form-control'})
    )
    mot_de_passe = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control'})
    )
    se_souvenir_de_moi = forms.BooleanField(
        label='Se souvenir de moi',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    

class ArtisanSignUpForm(UserCreationForm):
    mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Entrez votre mot de passe'}),
        error_messages={
            'required': "Veuillez entrer un mot de passe.",
        }
    )
    confirmer_le_mot_de_passe = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer votre mot de passe'}),
        error_messages={
            'required': "Veuillez confirmer votre mot de passe.",
        }
    )

    class Meta:
        model = Artisan
        fields = ['nom', 'prenom', 'genre', 'numero_de_telephone', 'email', 'domaine_activite', 'ville_ou_commune', 'localisation_atelier', 'photo_de_profil']
        widgets = {
            'nom': forms.TextInput(attrs={'placeholder': 'Entrez votre nom'}),
            'prenom': forms.TextInput(attrs={'placeholder': 'Entrez votre prénom'}),
            'genre': forms.Select(attrs={'placeholder': 'Genre'}),
            'numero_de_telephone': forms.TextInput(attrs={'placeholder': 'Entrez votre numéro de téléphone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'domaine_activite': forms.TextInput(attrs={'placeholder': 'Entrez votre domaine d\'activité'}),
            'ville_ou_commune': forms.TextInput(attrs={'placeholder': 'Entrez votre ville ou commune'}),
            'localisation_atelier': forms.TextInput(attrs={'placeholder': 'Précisez la localisation de votre atelier ou lieu de travail'}),
            'photo_de_profil': forms.ClearableFileInput(attrs={'placeholder': 'Photo de profil'}),
        }
        error_messages = {
            'nom': {
                'required': "Le nom est obligatoire.",
                'max_length': "Le nom ne peut pas dépasser 100 caractères."
            },
            'prenom': {
                'required': "Le prénom est obligatoire.",
                'max_length': "Le prénom ne peut pas dépasser 100 caractères."
            },
            'genre': {
                'required': "Le genre est obligatoire.",
            },
            'numero_de_telephone': {
                'required': "Le numéro de téléphone est obligatoire.",
                'max_length': "Le numéro de téléphone ne peut pas dépasser 20 caractères."
            },
            'email': {
                'required': "L'adresse email est obligatoire.",
                'invalid': "Veuillez entrer une adresse email valide.",
                'unique': "Un utilisateur avec cette adresse email existe déjà."
            },
            'domaine_activite': {
                'required': "Le métier est obligatoire.",
                'max_length': "Le métier ne peut pas dépasser 100 caractères."
            },
            'ville_ou_commune': {
                'required': "La ville ou commune est obligatoire.",
                'max_length': "La ville ou commune ne peut pas dépasser 100 caractères."
            },
            'localisation_atelier': {
                'required': "La localisation de l'atelier est obligatoire.",
                'max_length': "La localisation de l'atelier ne peut pas dépasser 200 caractères."
            },
            'photo_de_profil': {
                'invalid': "Veuillez télécharger une image valide."
            }
        }

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirmer_le_mot_de_passe = cleaned_data.get("confirmer_le_mot_de_passe")

        if mot_de_passe != confirmer_le_mot_de_passe:
            self.add_error('confirmer_le_mot_de_passe', "Les mots de passe ne correspondent pas.")
        return cleaned_data
    
    
class InscriptionClientForm(forms.ModelForm):
     mot_de_passe = forms.CharField(widget=forms.PasswordInput,required=False)
     confirmer_le_mot_de_passe = forms.CharField(widget=forms.PasswordInput,required=False)
     class Meta:
        model = InscriptionClient
        fields = ['nom', 'prenom', 'ville_ou_commune', 'numero_de_telephone','mot_de_passe','confirmer_le_mot_de_passe']
        error_messages = {
            'nom': {
                'required': "",
            },
            'prenom': {
                'required': "",
            },
            'ville_ou_commune': {
                'required': "",
            },
            'numero_de_telephone': {
                'required': "",
            },
             'mot_de_passe': {
                'required': "",
            },
             
            'confirmer_le_mot_de_passe': {
                'required': "",
            },
        }
        
     def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirmer_le_mot_de_passe = cleaned_data.get("confirmer_le_mot_de_passe")

        if mot_de_passe != confirmer_le_mot_de_passe:
            raise forms.ValidationError("Les mots de passe ne sont pas identiques")


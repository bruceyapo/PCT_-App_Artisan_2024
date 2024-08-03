from urllib import request
from django import forms
from django.shortcuts import get_object_or_404
from .models import Artisan, Client, PortfolioPhoto, Tache, UserProfile, Users,Metier
# from .models import Artisan, PortfolioPhoto, User, UserManager
# from django.contrib.auth.forms import UserCreationForm

class UploadFileForm(forms.Form):
    file = forms.FileField(label='', widget=forms.FileInput(
            attrs= {'class':'form-control li'}),
            error_messages={'required': ''}
        )
    
# # Formulaire d'inscription Artisan:

# class ArtisanForm(forms.ModelForm):
#     email = forms.EmailField(required=True, widget=forms.EmailInput(
#         {'class': 'form-control'}
#     ))
#     password = forms.CharField(widget=forms.PasswordInput(
#         {'class': 'form-control'}
#     ))
#     confirm_password = forms.CharField(widget=forms.PasswordInput(
#         {'class': 'form-control'}
#     ))

#     class Meta:
#         model = Artisan
#         fields = ['Nom', 'Prenom', 'genre', 'Telephone', 'Metier']
    
#     def __init__(self, *args, **kwargs):
#         super(ArtisanForm, self).__init__(*args, **kwargs)
#         self.fields['Nom'].widget.attrs.update({'class': 'form-control'})
#         self.fields['Prenom'].widget.attrs.update({'class': 'form-control'})
#         self.fields['genre'].widget.attrs.update({'class': 'form-control'})
#         self.fields['Telephone'].widget.attrs.update({'class': 'form-control'})
#         self.fields['Metier'].widget.attrs.update({'class': 'form-control'})

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if Users.objects.filter(email=email).exists():
#             raise forms.ValidationError("Un utilisateur avec cet email existe déjà.")
#         return email

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password and confirm_password and password != confirm_password:
#             self.add_error('confirm_password', "Les mots de passe ne correspondent pas.")

#     def save(self, commit=True):
#         instance = super(ArtisanForm, self).save(commit=False)
        
#         utilisateur = Users(
#             email=self.cleaned_data['email'],
#             username=self.cleaned_data['email'],  # Utiliser l'email comme username
#             roles='Artisan'
#         )
#         utilisateur.set_password(self.cleaned_data['password'])
        
#         if commit:
#             utilisateur.save()
#             instance.IdUser = utilisateur
#             instance.save()
        
#         return instance

    
class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['email']
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        
class ArtisanProfilForm(forms.ModelForm):
    Metier = forms.ModelChoiceField(label="Metier",queryset=Metier.objects.all(), required=True, widget=forms.Select())
    class Meta:
        model = Artisan
        fields = ['Nom', 'Prenom', 'Metier']
    
    def __init__(self, *args, **kwargs):
        super(ArtisanProfilForm, self).__init__(*args, **kwargs)
        self.fields['Nom'].widget.attrs.update({'class': 'form-control'})
        self.fields['Prenom'].widget.attrs.update({'class': 'form-control'})
        # self.fields['genre'].widget.attrs.update({'class': 'form-control'})
        self.fields['Metier'].widget.attrs.update({'class': 'form-control'})
        
# class UserProfileForm(forms.ModelForm):
#     photo_de_profil = forms.ImageField(required=False, error_messages={'invalid': ("Image file only")}, widget= forms.FileInput)
#     class Meta:
#         model = UserProfile
#         fields = ['Ville', 'Commune', 'Entreprise', 'Competence', 'Descriptions','Annee_experience', 'photo_de_profil']
    
#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         self.fields['Ville'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Commune'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Entreprise'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Competence'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Descriptions'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Annee_experience'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['photo_de_profil'].widget.attrs.update({'class': 'form-control'})
 
# class UserProfileForm(forms.ModelForm):
#     utilisateur = get_object_or_404(Users, id=user.id)
#     artisan = get_object_or_404(Artisan, IdUser=utilisateur)
#     Competence = forms.ModelMultipleChoiceField(
#         queryset=Tache.objects.filter(metier=Artisan.objects.filter(metier= artisan.Metier)),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
#     photo_de_profil = forms.ImageField(required=False, error_messages={'invalid': ("Image file only")}, widget=forms.FileInput)

#     class Meta:
#         model = UserProfile
#         fields = ['Ville', 'Commune', 'Entreprise', 'Competence', 'Descriptions', 'Annee_experience', 'photo_de_profil']

#     def __init__(self, *args, **kwargs):
        
#         metier_id = kwargs.pop('metier', None)
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         if metier_id:
#             self.fields['Competence'].queryset = Tache.objects.filter(metier=metier_id)
        
#         self.fields['Ville'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Commune'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Entreprise'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Descriptions'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Annee_experience'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['photo_de_profil'].widget.attrs.update({'class': 'form-control'})
 
# class UserProfileForm(forms.ModelForm):
#     Competence = forms.ModelMultipleChoiceField(
#         queryset=Tache.objects.none(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False
#     )
#     photo_de_profil = forms.ImageField(required=False, error_messages={'invalid': ("Image file only")}, widget=forms.FileInput)

#     class Meta:
#         model = UserProfile
#         fields = ['Ville', 'Commune', 'Entreprise', 'Competence', 'Descriptions', 'Annee_experience', 'photo_de_profil']

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         if user and hasattr(user, 'Metier'):# Suppose que le modèle Artisan a un champ metier
#             self.fields['Competence'].queryset = Tache.objects.filter(metier=user.Metier)
        
#         self.fields['Ville'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Commune'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Entreprise'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Descriptions'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['Annee_experience'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
#         self.fields['photo_de_profil'].widget.attrs.update({'class': 'form-control'})

# class searchArtisanForm(forms.ModelForm):
#     Metier = forms.ModelChoiceField(label="Metier",queryset=Metier.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
#     Ville = forms.CharField(label="Metier ou Commune", widget=forms.TextInput(attrs={'class': 'form-control'}))

class ArtisanSearchForm(forms.Form):
    metier = forms.ModelChoiceField(queryset=Metier.objects.all(), required=False, label="Métier", widget=forms.Select(attrs={'class': 'form-control'}))
    ville = forms.CharField(max_length=100, required=False, label="Metier ou Commune", widget=forms.TextInput(attrs={'placeholder': 'Entrez la ville ou la commune', 'class': 'form-control'}))
    # class Meta:
    #     model = Metier
    #     fields = ['Nom']
    
    # def __init__(self, *args, **kwargs):
    #     super(searchArtisanForm, self).__init__(*args, **kwargs)
    #     self.fields['Nom'].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    Competence = forms.ModelMultipleChoiceField(
        queryset=Tache.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    photo_de_profil = forms.ImageField(required=False, error_messages={'invalid': ("Image file only")}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ['Ville', 'Commune', 'Entreprise', 'Competence', 'Descriptions', 'Annee_experience', 'photo_de_profil']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pop user from kwargs
        super(UserProfileForm, self).__init__(*args, **kwargs)  # Correct usage of super()
        if user and hasattr(user, 'Metier'):
            self.fields['Competence'].queryset = Tache.objects.filter(metier=user.Metier)
        
        self.fields['Ville'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
        self.fields['Commune'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
        self.fields['Entreprise'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
        self.fields['Descriptions'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
        self.fields['Annee_experience'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
        self.fields['photo_de_profil'].widget.attrs.update({'class': 'form-control'})     
                   
class PortfolioPhotoForm(forms.ModelForm):
    class Meta:
        model = PortfolioPhoto
        fields = ['media']
    
    def __init__(self, *args, **kwargs):
        super(PortfolioPhotoForm, self).__init__(*args, **kwargs)
        self.fields['media'].widget.attrs.update({'placeholder': '', 'class': 'form-control'})
 
class ClientForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'id':'email'}
    ))
    Telephone = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'id':'phone'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id':'password'}
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id':'confirm_password'}
    ))
    class Meta:
        model = Client
        fields = ['Nom', 'Prenoms', 'Ville', 'Commune']
    
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['Nom'].widget.attrs.update({'class': 'form-control', 'id':'firstName'})
        self.fields['Prenoms'].widget.attrs.update({'class': 'form-control', 'id':'lastName'})
        self.fields['Ville'].widget.attrs.update({'class': 'form-control', 'id':'Ville'})
        self.fields['Commune'].widget.attrs.update({'class': 'form-control', 'id':'Commune'})

    def clean_phone(self):
        Telephone = self.cleaned_data.get('Telephone')
        if Users.objects.filter(Telephone=Telephone).exists():
            raise forms.ValidationError("Un utilisateur avec cet numéro de telephone existe déjà.")
        return Telephone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 6 caractères.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Les mots de passe ne correspondent pas.")

    def save(self, commit=True):
        instance = super(ClientForm, self).save(commit=False)
        
        utilisateur = Users(
            Telephone=self.cleaned_data['Telephone'],
            email=self.cleaned_data['email'],
            username=self.cleaned_data['email'],  # Utiliser l'email comme username
            roles='Client'
        )
        utilisateur.set_password(self.cleaned_data['password'])
        
        if commit:
            utilisateur.save()
            instance.IdUser = utilisateur
            instance.save()
        
        return instance

# class ArtisanForm(forms.ModelForm):
class ArtisanForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control'}
    ))
    Telephone = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
    Metier = forms.ModelChoiceField(label="Metier",queryset=Metier.objects.all(), required=True, widget=forms.Select())
    class Meta:
        model = Artisan
        fields = ['Nom', 'Prenom', 'genre', 'Metier']
    
    def __init__(self, *args, **kwargs):
        super(ArtisanForm, self).__init__(*args, **kwargs)
        self.fields['Nom'].widget.attrs.update({'class': 'form-control'})
        self.fields['Prenom'].widget.attrs.update({'class': 'form-control'})
        self.fields['genre'].widget.attrs.update({'class': 'form-control'})
        self.fields['Metier'].widget.attrs.update({'class': 'form-control'})
        # self.fields['Metier'].widget = forms.Select(attrs={'class': 'form-control'})

    def clean_phone(self):
        Telephone = self.cleaned_data.get('Telephone')
        if Users.objects.filter(Telephone=Telephone).exists():
            raise forms.ValidationError("Un utilisateur avec cet numéro de telephone existe déjà.")
        return Telephone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 6 caractères.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Les mots de passe ne correspondent pas.")

    def save(self, commit=True):
        instance = super(ArtisanForm, self).save(commit=False)
        
        utilisateur = Users(
            Telephone=self.cleaned_data['Telephone'],
            email=self.cleaned_data['email'],
            username=self.cleaned_data['email'],  # Utiliser l'email comme username
            roles='Artisan'
        )
        utilisateur.set_password(self.cleaned_data['password'])
        
        if commit:
            utilisateur.save()
            instance.IdUser = utilisateur
            instance.save()
        
        return instance

# class ArtisanForm(forms.ModelForm):
#     class Meta:
#         model = Artisan
#         fields = [
#             'nom', 'prenom', 'genre', 'numero_de_telephone', 'email', 'domaine_activite', 
#             'ville_ou_commune', 'localisation_atelier', 'photo_de_profil', 'titres_diplomes',
#             'annees_experience'
#         ]

# class PortfolioPhotoForm(forms.ModelForm):
#     class Meta:
#         model = PortfolioPhoto
#         fields = ['photo']

# # Formulaire de connexion :

class LoginForm(forms.Form):
    Telephone = forms.CharField(
        label='Numéro de téléphone',
        widget=forms.TextInput(attrs={'placeholder': 'Numéro de téléphone', 'class': 'form-control'})
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control'})
    )
    
    

# class ArtisanSignUpForm(UserCreationForm):
#     mot_de_passe = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Entrez votre mot de passe'}),
#         error_messages={
#             'required': "Veuillez entrer un mot de passe.",
#         }
#     )
#     confirmer_le_mot_de_passe = forms.CharField(
#         widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer votre mot de passe'}),
#         error_messages={
#             'required': "Veuillez confirmer votre mot de passe.",
#         }
#     )

#     class Meta:
#         model = Artisan
#         fields = ['nom', 'prenom', 'genre', 'numero_de_telephone', 'email', 'domaine_activite', 'ville_ou_commune', 'localisation_atelier', 'photo_de_profil']
#         widgets = {
#             'nom': forms.TextInput(attrs={'placeholder': 'Entrez votre nom'}),
#             'prenom': forms.TextInput(attrs={'placeholder': 'Entrez votre prénom'}),
#             'genre': forms.Select(attrs={'placeholder': 'Genre'}),
#             'numero_de_telephone': forms.TextInput(attrs={'placeholder': 'Entrez votre numéro de téléphone'}),
#             'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
#             'domaine_activite': forms.TextInput(attrs={'placeholder': 'Entrez votre domaine d\'activité'}),
#             'ville_ou_commune': forms.TextInput(attrs={'placeholder': 'Entrez votre ville ou commune'}),
#             'localisation_atelier': forms.TextInput(attrs={'placeholder': 'Précisez la localisation de votre atelier ou lieu de travail'}),
#             'photo_de_profil': forms.ClearableFileInput(attrs={'placeholder': 'Photo de profil'}),
#         }
#         error_messages = {
#             'nom': {
#                 'required': "Le nom est obligatoire.",
#                 'max_length': "Le nom ne peut pas dépasser 100 caractères."
#             },
#             'prenom': {
#                 'required': "Le prénom est obligatoire.",
#                 'max_length': "Le prénom ne peut pas dépasser 100 caractères."
#             },
#             'genre': {
#                 'required': "Le genre est obligatoire.",
#             },
#             'numero_de_telephone': {
#                 'required': "Le numéro de téléphone est obligatoire.",
#                 'max_length': "Le numéro de téléphone ne peut pas dépasser 20 caractères."
#             },
#             'email': {
#                 'required': "L'adresse email est obligatoire.",
#                 'invalid': "Veuillez entrer une adresse email valide.",
#                 'unique': "Un utilisateur avec cette adresse email existe déjà."
#             },
#             'domaine_activite': {
#                 'required': "Le métier est obligatoire.",
#                 'max_length': "Le métier ne peut pas dépasser 100 caractères."
#             },
#             'ville_ou_commune': {
#                 'required': "La ville ou commune est obligatoire.",
#                 'max_length': "La ville ou commune ne peut pas dépasser 100 caractères."
#             },
#             'localisation_atelier': {
#                 'required': "La localisation de l'atelier est obligatoire.",
#                 'max_length': "La localisation de l'atelier ne peut pas dépasser 200 caractères."
#             },
#             'photo_de_profil': {
#                 'invalid': "Veuillez télécharger une image valide."
#             }
#         }

#     def clean(self):
#         cleaned_data = super().clean()
#         mot_de_passe = cleaned_data.get("mot_de_passe")
#         confirmer_le_mot_de_passe = cleaned_data.get("confirmer_le_mot_de_passe")

#         if mot_de_passe != confirmer_le_mot_de_passe:
#             self.add_error('confirmer_le_mot_de_passe', "Les mots de passe ne correspondent pas.")
#         return cleaned_data
    
    
# class InscriptionClientForm(forms.ModelForm):
#      mot_de_passe = forms.CharField(widget=forms.PasswordInput,required=False)
#      confirmer_le_mot_de_passe = forms.CharField(widget=forms.PasswordInput,required=False)
#      class Meta:
#         model = InscriptionClient
#         fields = ['nom', 'prenom', 'ville_ou_commune', 'numero_de_telephone','mot_de_passe','confirmer_le_mot_de_passe']
#         error_messages = {
#             'nom': {
#                 'required': "",
#             },
#             'prenom': {
#                 'required': "",
#             },
#             'ville_ou_commune': {
#                 'required': "",
#             },
#             'numero_de_telephone': {
#                 'required': "",
#             },
#              'mot_de_passe': {
#                 'required': "",
#             },
             
#             'confirmer_le_mot_de_passe': {
#                 'required': "",
#             },
#         }
        
#      def clean(self):
#         cleaned_data = super().clean()
#         mot_de_passe = cleaned_data.get("mot_de_passe")
#         confirmer_le_mot_de_passe = cleaned_data.get("confirmer_le_mot_de_passe")

#         if mot_de_passe != confirmer_le_mot_de_passe:
#             raise forms.ValidationError("Les mots de passe ne sont pas identiques")


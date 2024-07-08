from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    mot_de_passe = forms.CharField(widget=forms.PasswordInput)
    confirmer_le_mot_de_passe = forms.CharField(widget=forms.PasswordInput)
    photo_de_profil = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['nom', 'prenom', 'sexe', 'telephone', 'email', 'metier', 'ville_ou_commune', 'localisation_atelier', 'mot_de_passe', 'confirmer_le_mot_de_passe','photo_de_profil']
           
    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get("mot_de_passe")
        confirmer_le_mot_de_passe = cleaned_data.get("confirmer_le_mot_de_passe")

        if mot_de_passe != confirmer_le_mot_de_passe:
            raise forms.ValidationError("Les mots de passe ne sont pas identiques")
        

    
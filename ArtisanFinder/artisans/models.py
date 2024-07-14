from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser




# Model de modification de profil Artisan :
class Artisan(AbstractUser):
    nom = models.CharField(max_length=50, blank=False)
    prenom = models.CharField(max_length=70, blank=False)
    genre = models.CharField(max_length=10, choices=[('Homme', 'Homme'), ('Femme', 'Femme')])
    numero_de_telephone = models.CharField(max_length=20, blank=False)
    email = models.EmailField()
    domaine_activite = models.CharField(max_length=100, blank=False)
    ville_ou_commune = models.CharField(max_length=100, blank=False)
    localisation_atelier = models.CharField(max_length=200, blank=False)
    photo_de_profil = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    portfolio_photos = models.ManyToManyField('PortfolioPhoto', blank=True)
    titres_diplomes = models.TextField(blank=True, help_text="Entrez les titres des diplômes séparés par des virgules")
    annees_experience = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class PortfolioPhoto(models.Model):
    photo = models.ImageField(upload_to='portfolio_photos/', blank=True, null=True)
    

# Model d'enregistrement client :

class InscriptionClient(models.Model):
    nom = models.CharField(max_length=50, blank=False)
    prenom = models.CharField(max_length=70, blank=False)
    ville_ou_commune = models.CharField(max_length=70, blank=False)
    numero_de_telephone = models.CharField(max_length=20, blank=False)
    mot_de_passe= models.CharField(max_length=60, null=True) 
    confirmer_le_mot_de_passe= models.CharField(max_length=60, null=True) 

# Model d'enregistrement d'artisans :

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser):
    nom = models.CharField(max_length=50, blank=False)
    prenom = models.CharField(max_length=50, blank=False)
    genre = models.CharField(max_length=10, choices=[('Homme', 'Homme'), ('Femme', 'Femme')])
    numero_de_telephone = models.CharField(max_length=20, blank=False)
    email = models.EmailField(unique=True)
    domaine_activite = models.CharField(max_length=70, blank=False)
    ville_ou_commune = models.CharField(max_length=70, blank=False)
    localisation_atelier = models.CharField(max_length=200, blank=False)
    photo_de_profil = models.ImageField(upload_to='photo_de_profil/', blank=True, null=True)
    mot_de_passe= models.CharField(max_length=60, null=True) 
    confirmer_le_mot_de_passe= models.CharField(max_length=60, null=True) 
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return self.email





    
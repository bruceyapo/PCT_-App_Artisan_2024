from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    sexe = models.CharField(max_length=10)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    metier = models.CharField(max_length=100)
    ville_ou_commune = models.CharField(max_length=100)
    localisation_atelier = models.CharField(max_length=255)
    photo_de_profil = models.ImageField(upload_to='photo_de_profil/', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return self.email


    
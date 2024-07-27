from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser

# class UserManager(BaseUserManager):
#     def create_user(self, email, username, password=None):
#         if not email:
#             raise ValueError('L\'adresse email est obligatoire')
        
#         if not username:
#             raise ValueError('Le username est obligatoire')
        
#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#         )
#         user.set_password(password)
#         user.is_active = True
#         user.save(using=self._db)
#         return user
    
#     def create_superuser(self, email, username, password):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             username=username,
#             password=password,
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superadmin = True
#         user.is_active = True
#         user.save(using=self._db)
#         return user
    

# ROLES_CHOICES = (
#     ('Administrateur', 'Administrateur'),
#     ('Artisan', 'Artisan'),
#     ('Client', 'Client')   
# )

# class Users(AbstractBaseUser):
#     username      = models.CharField(max_length=50, unique=True)
#     email         = models.EmailField(max_length=100, unique=True)
#     Telephone     = models.CharField(max_length=20, unique=True)
#     roles         = models.CharField(choices=ROLES_CHOICES, max_length=100)
#     # required
#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now_add=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_superadmin = models.BooleanField(default=False)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#     objects = UserManager()

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_admin

#     def has_module_perms(self, add_label):
#         return True

class UserManager(BaseUserManager):
    def create_user(self, Telephone, email=None, username=None, password=None):
        if not Telephone:
            raise ValueError("Le numéro de téléphone est obligatoire")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            Telephone=Telephone,
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, Telephone, password, email=None, username=None):
        user = self.create_user(
            Telephone=Telephone,
            email=email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_active = True
        user.save(using=self._db)
        return user
    

ROLES_CHOICES = (
    ('Administrateur', 'Administrateur'),
    ('Artisan', 'Artisan'),
    ('Client', 'Client')   
)

class Users(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    Telephone = models.CharField(max_length=20, unique=True)
    roles = models.CharField(choices=ROLES_CHOICES, max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'Telephone'
    REQUIRED_FIELDS = []  # Leave empty if no additional fields are required
    
    objects = UserManager()

    def __str__(self):
        return self.Telephone

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Metier(models.Model):  
    Nom  = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.Nom
# Model de modification de profil Artisan :
class Artisan(models.Model):
    Nom                     = models.CharField(max_length=50)
    Prenom                  = models.CharField(max_length=100)
    genre                   = models.CharField(max_length=10, choices=[('Homme', 'Homme'), ('Femme', 'Femme')])
    Metier                  = models.ForeignKey(Metier, on_delete=models.CASCADE, blank=True, null=True)
    IdUser                  = models.ForeignKey(Users, on_delete=models.CASCADE)
    def __str__(self):
        return self.Nom
    
class UserProfile(models.Model):  
    user                    = models.OneToOneField(Artisan, on_delete= models.CASCADE)
    Lieu_habitation         = models.CharField(max_length=100, blank=False)
    photo_de_profil         = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    Descriptions            = models.TextField(blank=True)
    Annee_experience        = models.IntegerField(blank=True)
    portfolio_photos        = models.ManyToManyField('PortfolioPhoto', blank=True)
    
    def __str__(self):
        return self.user.Nom
class Localisation(models.Model):  
    user              = models.OneToOneField(Artisan, on_delete= models.CASCADE)
    Longitude         = models.CharField(max_length=100, blank=False)
    Latitude          = models.CharField(max_length=200, blank=False)
    Details           = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.Nom

class PortfolioPhoto(models.Model):
    media = models.ImageField(upload_to='portfolio_photos/', blank=True, null=True)
    
# Model d'enregistrement client :
class Client(models.Model):
    Nom                     = models.CharField(max_length=50, blank=False)
    Prenoms                 = models.CharField(max_length=70, blank=False)
    Lieu_habitation         = models.CharField(max_length=70, blank=False)
    Telephone               = models.CharField(max_length=20, blank=False)
    IdUser                  = models.ForeignKey(Users, on_delete=models.CASCADE)
    def __str__(self):
        return self.Nom
class Administrateur(models.Model):
    Nom                     = models.CharField(max_length=50, blank=False)
    Prenoms                 = models.CharField(max_length=70, blank=False)
    Lieu_habitation         = models.CharField(max_length=70, blank=False)
    Telephone               = models.CharField(max_length=20, blank=False)
    IdUser                  = models.ForeignKey(Users, on_delete=models.CASCADE)
    def __str__(self):
        return self.Nom

# Model d'enregistrement d'artisans :

# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)



# class User(AbstractBaseUser):
#     nom = models.CharField(max_length=50, blank=False)
#     prenom = models.CharField(max_length=50, blank=False)
#     genre = models.CharField(max_length=10, choices=[('Homme', 'Homme'), ('Femme', 'Femme')])
#     numero_de_telephone = models.CharField(max_length=20, blank=False)
#     email = models.EmailField(unique=True)
#     domaine_activite = models.CharField(max_length=70, blank=False)
#     ville_ou_commune = models.CharField(max_length=70, blank=False)
#     localisation_atelier = models.CharField(max_length=200, blank=False)
#     photo_de_profil = models.ImageField(upload_to='photo_de_profil/', blank=True, null=True)
#     mot_de_passe= models.CharField(max_length=60, null=True) 
#     confirmer_le_mot_de_passe= models.CharField(max_length=60, null=True) 
    
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['nom', 'prenom']

#     def __str__(self):
#         return self.email





    
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser

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
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    def __str__(self):
        return self.Nom
class Tache(models.Model):
    metier = models.ForeignKey(Metier, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.description
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
    Ville                   = models.CharField(max_length=100, blank=True, null=True)
    Commune                 = models.CharField(max_length=100, blank=True, null=True)
    Entreprise              = models.CharField(max_length=100, blank=True, null=True)
    Competence              = models.ManyToManyField(Tache, blank=True)  # Changement ici
    photo_de_profil         = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    Descriptions            = models.TextField(blank=True)
    Annee_experience        = models.IntegerField(blank=True, null=True)
    # portfolio_photos        = models.ManyToManyField('PortfolioPhoto', blank=True)
    
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
    user = models.ForeignKey(Artisan, on_delete=models.CASCADE, null=True, blank=True) 
    media = models.ImageField(upload_to='portfolio_photos/', blank=True, null=True)
    DateAjout = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user.Nom
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




    
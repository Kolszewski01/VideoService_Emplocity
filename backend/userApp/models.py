from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.crypto import get_random_string

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Użytkownicy muszą mieć adres email')
        if not username:
            raise ValueError('Użytkownicy muszą mieć imię')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )

        user.set_password(password)
        user.activation_token = self.generate_activation_token(email)  # Dodajemy generowanie tokenu aktywacyjnego
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)

        return self.create_user(
            email,
            password=password,
            username=username,
            **extra_fields
        )

    def generate_activation_token(self, email):
        return urlsafe_base64_encode(force_bytes(get_random_string(20)))

class MyUser(AbstractBaseUser):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=35)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    id_frame = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=100, null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models

ERROR_REGEX_USERNAME = 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.'
ERROR_LENGTH_USERNAME = 'Enter a valid username. This value should be between 3 and 20 characters long.'


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user =  self.create_user(email, username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):

    class Meta:
         verbose_name = "user"

    email = models.EmailField(unique=True, max_length=100, verbose_name='email')
    username = models.CharField(unique=True, max_length=30, validators=[
        RegexValidator(regex='^[\w.@+\-]+$', message=ERROR_REGEX_USERNAME),
        MinLengthValidator(3, message=ERROR_LENGTH_USERNAME),
        ])
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return f'<User: {self.username}, Email: {self.email}>'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

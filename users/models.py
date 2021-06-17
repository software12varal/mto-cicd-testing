from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, is_staff=False, is_admin=False, is_active=True):
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError('User must have a password')
        user_obj = self.model(username=username)
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_admin = is_admin
        user_obj.is_staff = is_staff
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, password=None):
        user = self.create_user(username, password=password, is_staff=True)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username, password=password, is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=50)
    email = models.EmailField(blank=True, max_length=255)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_mto = models.BooleanField(default=True) # by default the user is an MTO.
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs):
        try:
            super(User, self).save(using='vendor_os_db')
        except:
            super(User, self).save(using='varal_job_posting_db')

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class EndUserManager(BaseUserManager):
    def create_user(self, username, phone, email, country, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            username=username,
            country=country,
        )

        user.set_password(password)
        print(user.password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone, email, country='', password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            phone=phone,
            username=username,
            country=country,
            # password=password
        )
        user.set_password(password)
        user.is_admin = True
        user.portal_admin = True
        user.save(using=self._db)
        return user


class EndUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    username = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=255, default='', blank=True)
    phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0)
    is_portal_admin = models.BooleanField(default=False) # the one who will be uplaoding the data
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255, default='', blank=True)
    shipping_address = models.CharField(max_length=255, default='', blank=True)

    objects = EndUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone', 'username']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
        


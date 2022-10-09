import random
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone, firstName, lastName, password=None, password2=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError('Users must have an Phone Number')

        user = self.model(
            phone= phone,
            firstName=firstName,
            lastName=lastName,
        )

        user.otp = random.randint(1001, 9999)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, firstName, lastName, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone,
            password=password,
            firstName=firstName,
            lastName=lastName,
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    phone = models.CharField(
        verbose_name='Phone',
        max_length=255,
        unique=True,
    )
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    otp = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName)

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
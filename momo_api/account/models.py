from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.crypto import get_random_string


def _generate_jwt_secret_key():
    """
    Create an account-specific jwt_secret_key.
    """
    jwt_secret_key_length = Account._meta.get_field('jwt_secret_key').max_length
    return get_random_string(jwt_secret_key_length, settings.SECRET_KEY_CHARACTER_SET)


class AccountManager(BaseUserManager):
    """
    Account Manager
    Extends django.contrib.auth.models.BaseUserManager
    """
    def create_user(self, username, password=None, *args, **kwargs):
        """
	Create a new Account
	Also assign the user an auth_token
	https://docs.djangoproject.com/en/dev/topics/auth/customizing/#django.contrib.auth.models.CustomUserManager.create_user
	"""
	account = self.model(
	    username=username,
	    *args,
	    **kwargs
	)

	account.save()
	account.set_password(password)
	account.save()
	return account

    def create_superuser(self, username, password, *args, **kwargs):
        account = self.create_user(
            username,
	    password=password,
	    *args,
	    **kwargs
	)

	account.is_admin = True
	account.save()
	return account


class Account(AbstractBaseUser):
    """
    Account Model
    Extends django.contrib.auth.models.AbstractBaseUser
    https://docs.djangoproject.com/en/1.10/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser
    """
    username = models.CharField(unique=True, max_length=20)
    jwt_secret_key = models.CharField(default=_generate_jwt_secret_key, max_length=30, editable=False)
    is_active = models.BooleanField(default=True)

    USER = 1
    COMPANY = 2
    ACCOUNT_TYPE_CHOICES = (
        (USER, 'User'),
	(COMPANY, 'Company'),
    )
    account_type = models.PositiveSmallIntegerField(choices=ACCOUNT_TYPE_CHOICES, default=USER)

    objects = AccountManager()

    # This is required to make email field the default identifier
    # https://docs.djangoproject.com/en/dev/topics/auth/customizing/#django.contrib.auth.models.CustomUser.USERNAME_FIELD
    USERNAME_FIELD = 'email'

    # This is required for when creating a user via the createsuperuser management command
    # https://docs.djangoproject.com/en/dev/topics/auth/customizing/#django.contrib.auth.models.CustomUser.REQUIRED_FIELDS
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """
        Return unique identifier for the account
        https://docs.djangoproject.com/en/dev/topics/auth/customizing/#django.contrib.auth.models.CustomUser.get_full_name
        """
        return self.username

    def get_short_name(self):
        """
        Return informal identifier for the user
        https://docs.djangoproject.com/en/dev/topics/auth/customizing/#djangexio.contrib.auth.models.CustomUser.get_short_name
        """
        return self.username

#    def is_active(self):
#        """
#        Return whether the user is considered active
#        https://docs.djangoproject.com/en/dev/topics/auth/customizing/#django.contrib.auth.models.CustomUser.is_active
#        """
#        return self.is_active

    def get_jwt_secret_key(self):
        """
        Sign JWTs with a combination of settings.JWT_MASTER_SECRET_KEY
        and self.jwt_secret_key
        """
        return '{}{}'.format(settings.JWT_MASTER_SECRET_KEY, self.jwt_secret_key)

    def delete(self):
        """
        Don't delete the Account
        Instead just set `is_active` to False
        """
        self.is_active = False
        self.save()
        return self

    class Meta:
        abstract = True


class UserManager(AccountManager):
    """
    User Manager
    """
    pass


class User(Account):
    """
    User Model
    """
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    avatar = models.ImageField(max_length=256, blank=True, null=True)

    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
	(FEMALE, 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)

    objects = UserManager()


class CompanyManager(AccountManager):
    """
    Company Manager
    """
    pass


class Company(Account):
    """
    Company Model
    """
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    avatar = models.ImageField(max_length=256, blank=True, null=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)

    objects = CompanyManager()


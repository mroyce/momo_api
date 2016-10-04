from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
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
    def create_user(self, username, password=None, *args, **kwargs):
        account = self.model(
            username=username,
            *args,
            **kwargs
        )

        # set password
        account.set_password(password)

        # create a profile for this account
        profile = {
            Account.USER: UserProfile(),
            Account.COMPANY: CompanyProfile(),
        }.get(account.account_type, Account.USER)
        profile.save()

        account.profile_content_type = ContentType.objects.get_for_model(profile)
        account.profile_id = profile.id
        account.save()

        return account

    def create_superuser(self, username, password, *args, **kwargs):
        account = self.create_user(
            username,
            password=password,
            *args,
            **kwargs
        )

        # set account as admin
        account.is_admin = True
        account.save()

        return account


class Account(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=20)
    jwt_secret_key = models.CharField(default=_generate_jwt_secret_key, max_length=30, editable=False)

    USER = 1
    COMPANY = 2
    ACCOUNT_TYPE_CHOICES = (
        (USER, 'User'),
        (COMPANY, 'Company'),
    )
    account_type = models.PositiveSmallIntegerField(choices=ACCOUNT_TYPE_CHOICES, default=USER)
    profile_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    profile_id = models.PositiveIntegerField(blank=True, null=True)
    profile = GenericForeignKey('profile_content_type', 'profile_id')

    objects = AccountManager()

    # This is required to make 'username' field the default identifier
    # https://docs.djangoproject.com/en/dev/topics/auth/customizing/#django.contrib.auth.models.CustomUser.USERNAME_FIELD
    USERNAME_FIELD = 'username'

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
        Return informal identifier for the account
        https://docs.djangoproject.com/en/dev/topics/auth/customizing/#djangexio.contrib.auth.models.CustomUser.get_short_name
        """
        return self.username

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
        # self.is_active = False
        # self.save()
        return self


class ProfileBase(models.Model):
    account = GenericRelation(Account, content_type_field='profile_content_type', object_id_field='profile_id')

    @property
    def get_account(self):
        """
        Get the account associated with this profile.
        Copied from http://stackoverflow.com/questions/7837330/generic-one-to-one-relation-in-django
        """
        ctype = ContentType.objects.get_for_model(self.__class__)
        try:
            account = Account.objects.get(profile_content_type__pk=ctype.id, profile_id=self.id)
        except:
            return None
        return account

    class Meta:
        abstract = True


class UserProfileManager(models.Manager):
    pass


class UserProfile(ProfileBase):
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

    objects = UserProfileManager()


class CompanyProfileManager(models.Manager):
    pass


class CompanyProfile(ProfileBase):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    avatar = models.ImageField(max_length=256, blank=True, null=True)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)

    objects = CompanyProfileManager()


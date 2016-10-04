from datetime import datetime, timedelta
from PIL import Image

from momo_api.base.utils import get_pil_image_as_django_content_file
from momo_api.account.models import (Account, UserProfile, CompanyProfile)


def create_test_image(filename='test.png', size=(160, 160), color='blue'):
    """
    Create and return a test image as a ContentFile
    """
    image = Image.new('RGBA', size, color)
    image_content_file = get_pil_image_as_django_content_file(image, 'png')
    image_content_file.name = filename
    return image_content_file


def create_test_account(username='test', password='test', **kwargs):
    """
    Create and return a test `Account` object
    """
    create_kwargs = {
        'username': username,
        'password': password,
    }

    create_kwargs.update(kwargs)
    return Account.objects.create_user(**create_kwargs)


def create_test_user_profile(username='test user', password='test', first_name='test', last_name='user', **kwargs):
    """
    Create and return a test `UserProfile` object
    """
    # create an account for this profile
    create_test_account(username, password)

    avatar = create_test_image()
    create_kwargs = {
        'avatar': avatar,
        'first_name': first_name,
        'last_name': last_name,
    }

    create_kwargs.update(kwargs)
    return UserProfile.objects.create(**create_kwargs)


def create_test_company_profile(username='test company', password='test', name='test company', **kwargs):
    """
    Create and return a test CompanyProfile object
    """
    # create an account for this profile
    create_test_account(username, password)

    avatar = create_test_image()
    create_kwargs = {
        'avatar': avatar,
        'name': name,
    }

    create_kwargs.update(kwargs)
    return CompanyProfile.objects.create(**create_kwargs)

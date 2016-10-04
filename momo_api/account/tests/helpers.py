from datetime import datetime, timedelta
from PIL import Image

from momo_api.base.utils import get_pil_image_as_django_content_file
from momo_api.account.models import (UserProfile, CompanyProfile)


def create_test_image(filename='test.png', size=(160, 160), color='blue'):
    """
    Create and return a test image as a ContentFile
    """
    image = Image.new('RGBA', size, color)
    image_content_file = get_pil_image_as_django_content_file(image, 'png')
    image_content_file.name = filename
    return image_content_file


def create_test_user_profile(username='test user', password='test', **kwargs):
    """
    Create and return a test UserProfile object
    """
    avatar = create_test_image()

    create_kwargs = {
        'username': username,
        'password': password,
        'avatar': avatar,
    }

    create_kwargs.update(kwargs)
    return UserProfile.objects.create(**create_kwargs)


def create_test_company_profile(username='test company', password='test', **kwargs):
    """
    Create and return a test CompanyProfile object
    """
    avatar = create_test_image()

    create_kwargs = {
        'username': username,
        'password': password,
        'avatar': avatar,
    }

    create_kwargs.update(kwargs)
    return CompanyProfile.objects.create(**create_kwargs)

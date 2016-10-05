import datetime
import random

from momo_api.listing.models import Listing, Event
from momo_api.base.tests.helpers import create_test_image


def create_test_listing(author, name='test listing', short_description='test', long_description='test', *kwargs):
    """
    Create and return a test `Listing` object
    """
    create_kwargs = {
        'author': author,
        'name': name,
        'short_description': short_description,
        'long_description': long_description,
        'thumbnail': create_test_image(),
    }

    create_kwargs.update(kwargs)
    return Listing.objects.create(**create_kwargs)


def create_test_event(author, listing=None, name='test event', short_description='test', long_description='test', **kwargs):
    """
    Create and return a test `Event` object
    """
    create_kwargs = {
        'author': author,
        'listing': listing,
        'name': name,
        'short_description': short_description,
        'long_description': long_description,
        'thumbnail': create_test_image(),
        'time': datetime.datetime.now() + datetime.timedelta(minutes=random.randint(1440, 525600))
    }

    create_kwargs.update(kwargs)
    return Event.objects.create(**create_kwargs)

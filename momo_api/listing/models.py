from django.conf import settings
from django.db import models

from momo_api.base.models import TrackEditsModelMixin


class Attraction(models.Model, TrackEditsModelMixin):
    """
    Abstract class for describing Listings/Events.
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255, blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(max_length=256, blank=True, null=True)
    # location unique

    class Meta:
        abstract = True


class Listing(Attraction):
    """
    Permanent listing for an attraction.
    """
    pass


class Event(Attraction):
    """
    One time event.
    """
    listing = models.ForeignKey(Listing, blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)

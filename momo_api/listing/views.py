from rest_framework import viewsets

from .models import Event, Listing
from .serializers import EventSerializer, ListingSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = ()
    filter_fields = ()


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = ()
    filter_fields = ()

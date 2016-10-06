from rest_framework import serializers

from .models import Attraction, Event, Listing


# TODO: this is an abstract Model, so we can't make a
# ModelSerializer from it.
class AttractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attraction

        fields = (
            'id',
            'author',
            'name',
            'short_description',
            'long_description',
            'thumbnail',
            # 'created_at',
            # 'edited_at',
        )


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing

        fields = (
            'id',
            # 'attraction',
            'author',
            'name',
            'short_description',
            'long_description',
            'thumbnail',
            # 'created_at',
            # 'edited_at',
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event

        fields = (
            'id',
            # 'attraction',
            'author',
            'listing',
            'name',
            'short_description',
            'long_description',
            'thumbnail',
            'time',
            # 'created_at',
            # 'edited_at',
        )

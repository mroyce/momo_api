from rest_framework import viewsets

from .models import CompanyProfile, UserProfile
from .serializers import CompanyProfileSerializer, UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = ()
    filter_fields = ()


class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    permission_classes = ()
    filter_fields = ()

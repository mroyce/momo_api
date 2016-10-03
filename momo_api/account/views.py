from rest_framework import viewsets

from .models import Company, User
from .serializers import CompanySerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = ()
    filter_fields = ()


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = ()
    filter_fields = ()

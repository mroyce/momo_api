from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework import serializers

from .jwt_authentication import create_jwt_token


class JWTLoginSerializer(serializers.Serializer):
    """
    Serializer class used to validate a username and password.
    'username' is identified by the custom UserModel.USERNAME_FIELD.
    Returns a JSON Web Token that can be used to authenticate calls to the API.

    Adapted from:
    https://github.com/GetBlimp/django-rest-framework-jwt/blob/master/rest_framework_jwt/serializers.py
    """
    username = serializers.CharField(max_length=settings.AUTH_USER_MODEL._meta.get_field('username').max_length)
    password = serializers.CharField(write_only=True, max_length=settings.AUTH_USER_MODEL._meta.get_field('password').max_length)

    MISSING_CREDENTIALS = 'Must include "username" and "password".'
    INVALID_CREDENTIALS = 'Unable to login with the provided credentials.'
    ACCOUNT_NOT_ACTIVE = 'Account is disabled.'

    def validate(self, data):
        """
        Validate a username and password
        Return an Account and the Account's JWT Token if successfuly valided
        """
        # Create credentials
        credentials = {
            'username': data.get('username'),
            'password': data.get('password'),
        }

        # Asset that all of the user credentials are present
        if not all(credentials.values()):
            raise serializers.ValidationError(self.MISSING_CREDENTIALS)

        # Attempt to authenticate the account
        account = authenticate(**credentials)

        # If the returned object is None or the account is inactive do not issue token
        if account is None:
            raise serializers.ValidationError(self.INVALID_CREDENTIALS)
        if not account.is_active:
            raise serializers.ValidationErorr(self.ACCOUNT_NOT_ACTIVE)

        # Create token and token expiration date
        token, token_expiration = create_jwt_token(account)

        # Return JSON Data
        return {
            'account': account,
            'token': token,
            'token_epxiration': token_expiration,
        }

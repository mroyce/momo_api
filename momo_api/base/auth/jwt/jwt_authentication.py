import jwt
from datetime import datetime

from django.conf import settings
from django.utils.encoding import smart_text

from rest_framework.authentication import BaseAuthentication, get_authorization_header

from momo_api.account.models import Account
from momo_api.account.serializers import AccountSerializer


LOGIN_SIGNUP_RESPONSE_ACCOUNT_KEY = 'account'
LOGIN_SIGNUP_RESPONSE_PROFILE_KEY = 'profile'
LOGIN_SIGNUP_RESPONSE_JWT_KEY = 'jwt'
LOGIN_SIGNUP_RESPONSE_JWT_EXPIRATION_KEY = 'expiration'
JWT_ACCOUNT_ID_PAYLOAD_KEY = 'sub'
JWT_EXPIRATION_PAYLOAD_KEY = 'exp'


def get_login_signup_response(account, token, token_expiration, request=None):
    """
    Return Response for login/signup endpoints
    Includes data for Account, JWT Token, and JWT Token Expiration
    ```
    {
        "account": {
            "id": 307,
            "account_type" 1,
            ...
        },
        "profile": {
            "first_name": "John",
            "last_name": "G",
            ...
        },
        "jwt": "<token>",
        "expiration": "<expiration>"
    }
    ```
    """
    # Serialize Account and Profile
    account_serialized = AccountSerializer(account, context={'request': request})

    # Get datetime in Year-Month-Day Hour:Minute:Second format
    datetime.fromtimestamp(token_expiration).strftime("%Y-%m-%d %H:%M:%S")
    token_expiration_date_time_field = token_expiration

    # Construct response
    response = {}
    response[LOGIN_SIGNUP_RESPONSE_ACCOUNT_KEY] = account_serialized.data
    # response[LOGIN_SIGNUP_RESPONSE_PROFILE_KEY] = profile
    response[LOGIN_SIGNUP_RESPONSE_JWT_KEY] = token
    response[LOGIN_SIGNUP_RESPONSE_JWT_EXPIRATION_KEY] = token_expiration_date_time_field

    return response


def create_jwt_token(account):
    """
    Create JWT token + expiration date for the given Account
    """
    # Get payload
    payload = create_account_jwt_payload(account)

    # Create token
    token = encode_jwt(payload, account)

    # Get expiration
    expiration = payload[JWT_EXPIRATION_PAYLOAD_KEY]

    return token, expiration


def create_account_jwt_payload(account):
    """
    Create JWT Payload
    The payload will contain:
    ```
    {
        'sub': account.pk,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    ```
    """
    payload = {}
    payload[JWT_ACCOUNT_ID_PAYLOAD_KEY] = account.pk
    payload[JWT_EXPIRATION_PAYLOAD_KEY] = datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
    return payload


def get_auth_header(request):
    """
    Returns the authentication header string split into
    `[auth_header_prefix, token]` or `None` if there is no authentication header.
    """
    token = get_authorization_header(request).split()
    auth_header_prefix = settings.JWT_AUTH_HEADER_PREFIX.lower()

    # If no Token was given or if prefix is not 'JWT', return None
    if not token or smart_text(token[0].lower()) != auth_header_prefix:
        return None

    # Check if length of Authorization Header is valid
    if len(token) == 1 or len(token) > 2:
        return None

    return token


def get_account_from_payload(payload):
    """
    Get the Account from the payload
    """
    # Get account id from the payload
    account_id = payload.get(JWT_ACCOUNT_ID_PAYLOAD_KEY, None)

    # Get account object with id=account_id
    account = Account.objects.get(pk=account_id)

    return account


def encode_jwt(payload, account, algorithm=settings.JWT_ALGORITHM):
    """
    Encode the given payload dictionary as a JWT token
    """
    return jwt.encode(
        payload,
        account.get_jwt_secret_key(),
        algorithm,
    ).decode('utf-8')


def decode_jwt(token, account, algorithms=[settings.JWT_ALGORITHM]):
    """
    Decode the given JWT token
    """
    return jwt.decode(
        token,
        account.get_jwt_secret_key(),
        algorithms=algorithms,
        leeway=settings.JWT_LEEWAY,
        options={'verify_exp': settings.JWT_VERIFY_EXPIRATION},
    )


class JWTAuthentication(BaseAuthentication):
    """
    Token-based authentication using the JSON Web Token standard.
    Handle encoding/decoding of JWT
    Uses Django REST Framework JWT: https://github.com/GetBlimp/django-rest-framework-jwt
    """
    def authenticate(self, request):
        """
        Returns a two-tuple of `Account` and `token` if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        auth = get_auth_header(request)

        # Check if we successfuly got a JWT
        if auth is None:
            return None

        token = auth[1]

        # Grab payload, but can't check signature yet because we need the `Account`
        payload = jwt.decode(token, options={'verify_signature': False})

        # Get the associate `Account`
        account = get_account_from_payload(payload)

        # Verify the signature
        payload = decode_jwt(token, account)

        return (account, token)

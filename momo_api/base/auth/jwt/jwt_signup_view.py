from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .jwt_authentication import create_jwt_token, get_login_signup_response
from momo_api.account.serializers import AccountSerializer


class JWTSignUpView(APIView):
    """
    Endpoint to allow a new user to register for a new account.

    Returns a dictionary detailing the created user including a 'token' key
    with a JWT access token and JWT token expiration date.
    """
    # don't need to be authenticated or have permissions to create a new user
    authentication_classes = ()
    permission_classes = ()
    serializer_class = AccountSerializer

    def post(self, request, format=None):
        """
        The endpoint processes `POST` requests with the required data: `username` and `password`.

        Given the valid data, creates a new `Account` and returns a 201 with serialized session
        data and a JWT access token.

        If not valid, returns a 400.
        """
        # Assert we have a valid new Account object with new_account_serializer.is_valid()
        new_account_serializer = self.serializer_class(data=request.data)
        new_account_serializer.is_valid(raise_exception=True)

        # Save the new Account
        new_account = new_account_serializer.save()

        # Create a token for the new Account
        token, token_expiration = create_jwt_token(new_account)

        # Construct Response
        response_data = get_login_signup_response(new_account, token, token_expiration, request=request)
        return Response(response_data, status=HTTP_201_CREATED)

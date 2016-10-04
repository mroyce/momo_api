from rest_framework.response import Response
from rest_framework.views import APIView

from .jwt_authentication import get_login_signup_response
from .jwt_login_serializer import JWTLoginSerializer


class JWTLoginView(APIView):
    """
    API View that receivs a POST witha  user's username and password.
    Returns a JSON Web Token that can be used for authenticated requests.
    """
    # don't need to be authenticated or have permissions to login
    permission_classes = ()
    authentication_classes = ()
    serializer_class = JWTLoginSerializer

    def post(self, request):
        """
        Returns an `Account` and an `auth_token` string that can be used for authenticated requests.
        """
        # Validate
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the validated_data from the serializer
        account = serializer.validated_data['account']
        token = serializer.validated_data['token']
        token_expiration = serializer.validated_data['token_expiration']

        # Construct Response
        response_data = get_login_signup_response(account, token, token_expiration, request=request)
        return Response(response_data)

import logging
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions, status
from dj_rest_auth.views import UserDetailsView, LoginView
from dj_rest_auth.utils import jwt_encode
from dj_rest_auth.jwt_auth import set_jwt_cookies
from dj_rest_auth.serializers import JWTSerializer
# dj-rest-auth bug fix workaround
from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)
from positive_api.permissions import CustomJWTCookieAuthentication

logger = logging.getLogger(__name__)


@api_view()
def root_route(request):
    return Response({
        'message': 'Welcome to the Positive API',
    })

# dj-rest-auth bug fix workaround
@api_view(['POST'])
def logout_route(request):
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response


class CustomUserDetailsView(UserDetailsView):
    authentication_classes = [CustomJWTCookieAuthentication]
    permission_classes = (
        permissions.AllowAny,
    )
    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        """
        return get_user_model().objects.none()


class CustomLoginView(LoginView):

    def login(self):
        self.user = self.serializer.validated_data['user']
        logger.info(f"El usuario es {self.user}")
        self.access_token, self.refresh_token = jwt_encode(self.user)
        logger.info(f"El access token es {self.access_token} el refresh es {self.refresh_token}")

    def get_response(self):

        data = {
            'user': self.user,
            'access': self.access_token,
            'refresh': self.refresh_token
        }
        logger.info(f"El access token es del tipo {type(self.access_token)}")
        logger.info(f"La data es {data}")

        serializer = JWTSerializer(
            instance=data,
            context=self.get_serializer_context(),
        )
        response = Response(serializer.data, status=status.HTTP_200_OK)
        set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response
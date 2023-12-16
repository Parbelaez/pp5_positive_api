import logging
from django.contrib.auth import get_user_model

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from dj_rest_auth.views import UserDetailsView
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
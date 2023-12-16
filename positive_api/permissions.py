import logging

from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.conf import settings
from rest_framework import exceptions, permissions
from rest_framework.authentication import CSRFCheck


logger = logging.getLogger(__name__)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    # This method is called every time a request is made to the API
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # SAFE_METHODS is a tuple containing GET, HEAD and OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        # obj.owner is the owner of the profile
        return obj.owner == request.user


class CustomJWTCookieAuthentication(JWTCookieAuthentication):
    def enforce_csrf(self, request):
        """
        Enforce CSRF validation for session based authentication.
        """

        def dummy_get_response(request):  # pragma: no cover
            return None

        check = CSRFCheck(dummy_get_response)
        # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        logger.info(f"Razon de la chota es {reason}")
        if reason:
            # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied(f"CSRF Failed: {reason}")

    def authenticate(self, request):
        logger.info("En authentica de esta monda")
        cookie_name = settings.JWT_AUTH_COOKIE
        logger.info(f"Cookie name is {cookie_name}")
        header = self.get_header(request)
        if header is None:
            logger.info("Header is none")
            if cookie_name:
                raw_token = request.COOKIES.get(cookie_name)
                if (
                    settings.JWT_AUTH_COOKIE_ENFORCE_CSRF_ON_UNAUTHENTICATED
                ):  # True at your own risk
                    self.enforce_csrf(request)
                elif raw_token is not None and settings.JWT_AUTH_COOKIE_USE_CSRF:
                    self.enforce_csrf(request)
            else:
                return None
        else:
            logger.info(f"Header is not none {header}")
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            logger.info("El token se fue a la puta")
            return None

        logger.info(f"Antes de get validated_token {raw_token}")
        validated_token = self.get_validated_token(raw_token)
        logger.info(f"El token valido es {validated_token}")
        return self.get_user(validated_token), validated_token

    def get_validated_token(raw_token):
        try:
            logger.info(f"Raw token es {raw_token}")
            return AccessToken(raw_token)
        except TokenError as e:
            logger.exception(f"Token invalido {str(e)}")
            raise

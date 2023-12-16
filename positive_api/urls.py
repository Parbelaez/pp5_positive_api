from django.contrib import admin
from django.urls import path, include
# dj-rest-auth bug fix workaround... add the logut_route import
from .views import root_route, logout_route

urlpatterns = [
    path('', root_route),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # dj-rest-auth bug fix workaround
    path('dj-rest-auth/logout/', logout_route),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    # end of dj-rest-auth bug fix workaround
    path(
        'dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')
    ),
    path('', include('profiles.urls')),
    path('', include('posts.urls')),
    path('', include('likes.urls')),
    path('', include('places.urls')),
]

from django.urls import path
from places import views


urlpatterns = [
    path('places/', views.PlaceList.as_view()),
    path('places/<int:pk>/', views.PlaceDetail.as_view()),
]
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

# Import token libraries
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register('users', views.UserSet, basename='user')
router.register('groups', views.GroupSet, basename='group')
router.register('elections', views.ElectionSet, basename='election')

urlpatterns = [
    path('', views.baseResponse),

    path('groups/<str:pk>/users/', views.getAllUsersFromGroup),

    path('users/<str:pk>/elections/', views.getAllElectionsFromUser),

    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AuthViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', AuthViewSet.as_view({'post': 'register'}), name='register'),
    path('login/', AuthViewSet.as_view({'post': 'login'}), name='login'),
    path('logout/', AuthViewSet.as_view({'post': 'logout'}), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
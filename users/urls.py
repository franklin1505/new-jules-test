from django.urls import path
from .views import RegisterView, CustomLoginView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

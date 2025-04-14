from django.urls import path
from .views import RegisterView, LoginView, RefreshView, LogoutView, CheckTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check/', CheckTokenView.as_view()),
]
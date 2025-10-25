# from django.urls import path
# from .views import RegisterView, LoginView, LogoutView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
# ]



from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView,
    ProfileView, UpdateProfileView, ChangePasswordView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Profile endpoints
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
]

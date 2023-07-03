from django.urls import path
from . views import profile, Login, RegisterView, EmailVerificationView
from users import views as user_views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='products/index.html'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile, name='profile'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
]
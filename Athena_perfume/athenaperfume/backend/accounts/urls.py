from django.urls import path
#from . import views
#from django.contrib.auth import views as auth_views

#urlpatterns = [
 #   path('register/', views.register_view, name='register'),
  #  path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
   # path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
#]
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

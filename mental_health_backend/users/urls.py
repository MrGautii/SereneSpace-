from django.urls import path
from .views import signup, login_view, verify_email

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('verify-email/', verify_email, name='verify_email'),

]
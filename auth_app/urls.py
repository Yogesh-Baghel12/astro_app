from django.urls import path
from .views import SendOTPView, VerifyOTPView, FocusAreaView, ProfileView

urlpatterns = [
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('focus-area/', FocusAreaView.as_view(), name='focus-area'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
import random
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer, UserSerializer, ProfileSerializer

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            country_code = serializer.validated_data['country_code']
            phone_number = serializer.validated_data['phone_number']
            full_phone_number = f"{country_code}{phone_number}"
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            print(f"TEST OTP for {full_phone_number}: {otp}")
            expires_at = timezone.now() + timedelta(minutes=5)
            OTP.objects.update_or_create(
                phone_number=full_phone_number,
                defaults={'otp': otp, 'expires_at': expires_at}
            )
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']
            try:
                otp_record = OTP.objects.get(phone_number=phone_number)
                if otp_record.expires_at < timezone.now():
                    return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
                if otp_record.otp != otp:
                    return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
                user, created = User.objects.get_or_create(
                    phone_number=phone_number,
                    defaults={'username': phone_number, 'country_code': phone_number[:3]}
                )
                refresh = RefreshToken.for_user(user)
                otp_record.delete()
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            except OTP.DoesNotExist:
                return Response({'error': 'No OTP found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
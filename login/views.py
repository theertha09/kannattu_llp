from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from login.models import Account
from roles.models import Role
from hr.models import hr
from hr.serializers import hrSerializer
from .serializers import RegisterSerializer, LoginSerializer, ForgotPasswordSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            # Fetch HR associated with this account
            try:
                hr_instance = hr.objects.get(account=user)
                hr_data = hrSerializer(hr_instance).data
            except hr.DoesNotExist:
                hr_data = None

            return Response({
                "user": {
                    "role": user.role.name,
                    "hr": hr_data
                },
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response(serializer.errors, status=400)

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Password reset successfully"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

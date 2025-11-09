from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError  # اصلاح: from اضافه شد

from .models import CustomUser
from .serializers import RegisterSerializer


# Register endpoint
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAdminUser]  # فقط ادمین!

    def perform_create(self, serializer):
        # فقط ادمین می‌تونه role='admin' بسازه
        data = serializer.validated_data
        if not self.request.user.is_staff:
            data['role'] = 'user'
        serializer.save(**data)


# Login endpoint (custom)
@api_view(['POST'])
def login_view(request):
    """
    Accepts: { "identifier": "...", "password": "..." }
    identifier can be phone OR email OR username
    Response: { access, role } + refresh in httpOnly cookie
    """
    identifier = request.data.get('identifier') or request.data.get('username') or request.data.get('email')
    password = request.data.get('password')

    if not identifier or not password:
        return Response({"detail": "identifier and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # try to find user by phone or email or username
        user = CustomUser.objects.filter(
            Q(phone=identifier) | Q(email=identifier) | Q(username=identifier)
        ).first()
    except Exception:
        user = None

    if user is None:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    # Response فقط access و role (refresh در cookie)
    response = Response({
        "access": str(refresh.access_token),
        "role": user.role
    })

    # set refresh در httpOnly cookie
    response.set_cookie(
        'refresh',
        str(refresh),
        httponly=True,
        secure=False,  # در لوکال False، در production True کن
        samesite='Lax',
        max_age=60 * 60 * 24 * 7  # 7 روز
    )

    return response


# Protected userinfo (to check role)
class UserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "role": user.role
        })


# Refresh endpoint (از cookie)
@api_view(['POST'])
def refresh_view(request):
    """
    Renew access token from httpOnly refresh cookie
    """
    refresh_cookie = request.COOKIES.get('refresh')
    if not refresh_cookie:
        return Response({"detail": "No refresh token found"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        refresh = RefreshToken(refresh_cookie)
        response = Response({
            "access": str(refresh.access_token),
        })
        # آپدیت refresh cookie (rotate)
        response.set_cookie(
            'refresh',
            str(refresh),
            httponly=True,
            secure=False,  # True در production
            samesite='Lax',
            max_age=60 * 60 * 24 * 7  # 7 روز
        )
        return response
    except TokenError:
        response = Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        response.delete_cookie('refresh')
        return response


# Logout endpoint (پاک کردن cookie)
@api_view(['POST'])
def logout_view(request):
    """
    Invalidate session by deleting refresh cookie
    """
    response = Response({"detail": "Logged out successfully"})
    response.delete_cookie('refresh')
    return response
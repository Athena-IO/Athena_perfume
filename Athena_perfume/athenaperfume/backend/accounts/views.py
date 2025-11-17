from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import CustomUser, LoginLog
from .serializers import RegisterSerializer, LoginLogSerializer


# ---------------------------
# گرفتن آی‌پی کاربر
# ---------------------------
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


# ---------------------------
# Register (فقط ادمین)
# ---------------------------
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        data = serializer.validated_data
        if not self.request.user.is_staff:
            data['role'] = 'user'
        serializer.save(**data)


# ---------------------------
# Login (با ثبت لاگ)
# ---------------------------
@api_view(['POST'])
def login_view(request):
    identifier = request.data.get('identifier') or request.data.get('username') or request.data.get('email')
    password = request.data.get('password')

    if not identifier or not password:
        return Response({"detail": "identifier and password required"}, status=status.HTTP_400_BAD_REQUEST)

    user = CustomUser.objects.filter(
        Q(phone=identifier) | Q(email=identifier) | Q(username=identifier)
    ).first()

    ip = get_client_ip(request)
    ua = request.META.get('HTTP_USER_AGENT', '')

    # کاربر پیدا نشد
    if user is None:
        LoginLog.objects.create(
            user=None,
            username_attempt=identifier,
            ip_address=ip,
            user_agent=ua,
            success=False,
        )
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # رمز اشتباه باشد
    if not user.check_password(password):
        LoginLog.objects.create(
            user=user,
            username_attempt=identifier,
            ip_address=ip,
            user_agent=ua,
            success=False,
        )
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # ورود موفق
    refresh = RefreshToken.for_user(user)

    LoginLog.objects.create(
        user=user,
        username_attempt=identifier,
        ip_address=ip,
        user_agent=ua,
        success=True,
    )

    response = Response({
        "access": str(refresh.access_token),
        "role": user.role
    })

    response.set_cookie(
        'refresh',
        str(refresh),
        httponly=True,
        secure=False,  # برای لوکال
        samesite='Lax',
        max_age=60 * 60 * 24 * 7
    )

    return response


# ---------------------------
# گرفتن اطلاعات کاربر لاگین‌شده
# ---------------------------
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


# ---------------------------
# Refresh Token
# ---------------------------
@api_view(['POST'])
def refresh_view(request):
    refresh_cookie = request.COOKIES.get('refresh')
    if not refresh_cookie:
        return Response({"detail": "No refresh token found"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        refresh = RefreshToken(refresh_cookie)

        response = Response({
            "access": str(refresh.access_token)
        })

        response.set_cookie(
            'refresh',
            str(refresh),
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=60 * 60 * 24 * 7
        )
        return response

    except TokenError:
        response = Response({"detail": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        response.delete_cookie('refresh')
        return response


# ---------------------------
# Logout
# ---------------------------
@api_view(['POST'])
def logout_view(request):
    response = Response({"detail": "Logged out successfully"})
    response.delete_cookie('refresh')
    return response


# ---------------------------
# لیست لاگ‌های ورود (فقط ادمین)
# ---------------------------
class LoginLogListView(ListAPIView):
    queryset = LoginLog.objects.all().order_by('-timestamp')
    serializer_class = LoginLogSerializer
    permission_classes = [permissions.IsAdminUser]

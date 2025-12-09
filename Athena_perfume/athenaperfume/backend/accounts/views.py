from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import CustomUser
from .serializers import RegisterSerializer

# Register endpoint (List + Create: GET لیست عمومی، POST فقط ادمین)
class RegisterView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all().order_by('-id')  # لیست جدیدترین کاربران
    serializer_class = RegisterSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            # فقط ادمین create کنه
            permission_classes = [permissions.IsAdminUser]
        else:
            # GET لیست عمومی (بدون جزئیات حساس)
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            # برای GET، فیلدهای حساس رو مخفی کن
            class SafeSerializer(RegisterSerializer):
                class Meta(RegisterSerializer.Meta):
                    fields = ['id', 'username', 'email', 'phone', 'role', 'date_joined']
                    extra_kwargs = {'password': {'write_only': True}}
            return SafeSerializer
        return RegisterSerializer

    def perform_create(self, serializer):
        # فقط ادمین role='admin' بسازه
        data = serializer.validated_data
        if not self.request.user.is_staff:
            data['role'] = 'user'
        serializer.save(**data)

# Login endpoint (custom)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    identifier = request.data.get('identifier') or request.data.get('username') or request.data.get('email')
    password = request.data.get('password')

    if not identifier or not password:
        return Response({"detail": "identifier and password required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.filter(
            Q(phone=identifier) | Q(email=identifier) | Q(username=identifier)
        ).first()
    except Exception:
        user = None

    if user is None:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({"detail": "User account is disabled"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(password):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    response = Response({
        "access": str(refresh.access_token),
        "role": user.role
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

# Protected userinfo
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

# Refresh endpoint
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def refresh_view(request):
    refresh_cookie = request.COOKIES.get('refresh')
    if not refresh_cookie:
        return Response({"detail": "No refresh token found"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        refresh = RefreshToken(refresh_cookie)
        response = Response({
            "access": str(refresh.access_token),
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

# Logout endpoint
@api_view(['POST']) 
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    response = Response({"detail": "Logged out successfully"})
    response.delete_cookie('refresh')
    return response

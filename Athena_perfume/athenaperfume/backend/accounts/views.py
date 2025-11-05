from django.db.models import Q
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import RegisterSerializer

# Register endpoint
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


# Login endpoint (custom)
@api_view(['POST'])
def login_view(request):
    """
    Accepts: { "identifier": "...", "password": "..." }
    identifier can be phone OR email OR username
    Response: { access, refresh, role }
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
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "role": user.role
    })


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

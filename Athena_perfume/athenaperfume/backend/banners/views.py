from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import Banner
from .serializers import BannerSerializer

class BannerListCreateView(generics.ListCreateAPIView):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        if Banner.objects.count() >= 4:
            raise ValidationError("حداکثر ۴ بنر مجاز است.")
        serializer.save()

class BannerDeleteView(generics.DestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAdminUser]
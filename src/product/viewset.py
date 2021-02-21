from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView


from .serializers import ProductCreateSerializer
from .models import Product
from .permissions import IsSeller, IsVerified


class ProductCreateViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    # permission_classes = [IsAuthenticated, IsSeller, IsVerified]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serilizer):
        serilizer.save(user=self.request.user)

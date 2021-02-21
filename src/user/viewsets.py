from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from . import serializers as user_serializer
from .models import User, Company
from .permissions import UpdateOwnDetail
from .utils import get_tokens_for_user
from . import permissions


class UserRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = user_serializer.UserRegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            get_tokens_for_user(User.objects.get(mobile_no=request.data['mobile_no'])),
            status=status.HTTP_201_CREATED)


class AdminRegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    # TODO : permission set
    permission_classes = [permissions.IsSuperAdmin]
    serializer_class = user_serializer.AdminRegistrationSerailizer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'message': "Successfully Created Admin"},
                        status=status.HTTP_201_CREATED)

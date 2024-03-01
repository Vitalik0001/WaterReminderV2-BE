from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserCreateSerializer, UserProfileSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UserProfileCreateView(CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return self.request.user

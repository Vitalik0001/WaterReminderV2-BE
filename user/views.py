from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from user.models import UserProfile
from user.serializers import (
    UserCreateSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UserProfileCreateView(CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserProfileUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        email = self.request.user.email
        return UserProfile.objects.get(user__email=email)

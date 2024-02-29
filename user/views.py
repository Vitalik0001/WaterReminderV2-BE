from rest_framework.generics import CreateAPIView

from user.serializers import UserCreateSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserCreateSerializer

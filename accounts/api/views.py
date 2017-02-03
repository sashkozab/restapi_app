from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import serializers

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination





User = get_user_model()


from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer
    )

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

class UserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    print("Just inside class UserLoginAPIView")
    
    def post(self, request, *args, **kwargs):
        data = request.data
        recieved_pass = data["password"]
        print("data from post UserLoginAPIView: ", data["password"])
        serializer = UserLoginSerializer(data=data)
        print("data from post UserLoginAPIView AFTER serializer: ", serializer.initial_data)
        if serializer.is_valid(raise_exception=True):
            print("User?: ", request.user, "new_data: ", serializer.data)
            new_data = serializer.data
            print("Pass from data: ")
            # new_data["password"] = recieved_pass
            print("User==>after?: ", request.user, "new_data: ", new_data)
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)





















from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    )
from .serializers import (
    # PostCreateUpdateSerializer, 
    # PostDetailSerializer, 
    PostListSerializer
    )
from posts.models import Post


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
from rest_framework import generics

from .models import Post, MediaFile
from .serializers import PostSerializer, MediaSerializer


class MediaCreate(generics.CreateAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaSerializer


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user.id)


class UserPostList(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(owner_id=user_id).order_by('-created')


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


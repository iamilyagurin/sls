from rest_framework import generics, permissions

from .models import Post, MediaFile
from .serializers import PostSerializer, MediaSerializer
from .bl import process_media


class MediaCreate(generics.CreateAPIView):
    queryset = MediaFile.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        media_obj = serializer.save(owner=self.request.user)
        process_media(media_obj)


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

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



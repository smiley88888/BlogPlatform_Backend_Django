from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Post, session
from .schemas import UserCreate, UserLogin, PostCreate, PostDelete
from pydantic import ValidationError
from django.core.cache import cache
from rest_framework import status

class SignupView(APIView):
    def post(self, request):
        try:
            data = UserCreate(**request.data)
            user = User(email=data.email, password=data.password)
            session.add(user)
            session.commit()
            token = RefreshToken.for_user(user)
            return Response({'token': str(token.access_token)}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        try:
            data = UserLogin(**request.data)
            user = session.query(User).filter_by(email=data.email, password=data.password).first()
            if user:
                token = RefreshToken.for_user(user)
                return Response({'token': str(token.access_token)}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)

class AddPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = PostCreate(**request.data)
            user = request.user
            new_post = Post(user_id=user.id, text=data.text)
            session.add(new_post)
            session.commit()
            return Response({'postID': new_post.id}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)

class GetPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cache_key = f'user_posts_{user.id}'
        posts = cache.get(cache_key)
        if not posts:
            posts = session.query(Post).filter_by(user_id=user.id).all()
            posts_data = [{'id': post.id, 'text': post.text} for post in posts]
            cache.set(cache_key, posts_data, timeout=300)
        return Response(posts, status=status.HTTP_200_OK)

class DeletePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            data = PostDelete(**request.data)
            user = request.user
            post = session.query(Post).filter_by(id=data.post_id, user_id=user.id).first()
            if post:
                session.delete(post)
                session.commit()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, session
from .schemas import UserCreate, UserLogin, PostCreate, PostDelete
from pydantic import ValidationError
from rest_framework import status
from .decorators import token_required
from django.core.cache import cache



class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = UserCreate(**request.data)
            user = User(email=data.email, password=data.password)
            session.add(user)
            session.commit()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = UserLogin(**request.data)
            user = session.query(User).filter_by(email=data.email, password=data.password).first()
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)

# In-memory storage for posts
post_storage = {}

class AddPostView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(token_required)
    def post(self, request):
        try:
            if len(request.body) > 1024 * 1024:  # 1 MB limit
                return Response({'error': 'Payload too large'}, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
            
            data = PostCreate(**request.data)
            user = request.user
            post_id = len(post_storage) + 1
            post_storage[post_id] = {'user_id': user.id, 'text': data.text}
            return Response({'postID': post_id}, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)

class GetPostsView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(token_required)
    def get(self, request):
        user = request.user
        cache_key = f'user_posts_{user.id}'
        posts = cache.get(cache_key)
        
        if not posts:
            posts = [{'id': post.id, 'text': post.text} for post in Post.query.filter_by(user_id=user.id).all()]
            cache.set(cache_key, posts, timeout=300)  # Cache for 5 minutes
        
        return Response(posts, status=status.HTTP_200_OK)
    

# In-memory storage for posts
post_storage = {}

class DeletePostView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(token_required)
    def delete(self, request):
        try:
            data = PostDelete(**request.data)
            user = request.user
            post = post_storage.get(data.post_id)
            if post and post['user_id'] == user.id:
                del post_storage[data.post_id]
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Post not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response(e.errors(), status=status.HTTP_400_BAD_REQUEST)
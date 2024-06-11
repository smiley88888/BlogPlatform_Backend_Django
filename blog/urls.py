from django.urls import path
from .views import SignupView, LoginView, AddPostView, GetPostsView, DeletePostView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('addpost/', AddPostView.as_view(), name='addpost'),
    path('getposts/', GetPostsView.as_view(), name='getposts'),
    path('deletepost/', DeletePostView.as_view(), name='deletepost'),
]
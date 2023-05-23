from django.urls import path
from posts.views import *

urlpatterns = [
    path('posts/', PostList.as_view()),
    path('posts/<int:id>/', PostDetail.as_view()),
    path('comments/', CommentList.as_view()),
    path('comments/<int:id>/', CommentDetail.as_view()),
]

"""
    #path('', hello_world, name = 'hello_world'),
    path('introduction', introduction, name = 'introduction'),
    path('<int:post_id>/', post_detail, name = 'post_detail'),
    #path('post_detail/', get_post_all, name = 'post_all'),
    path('new/', create_post, name = "create_post"),
    path('newcomment/<int:post_id>/', create_comment, name = "create_comment"),
    path('', get_post_all, name = "get_post_all"),
    path('comment/<int:post_id>/', get_comment, name = 'get_comment')
"""
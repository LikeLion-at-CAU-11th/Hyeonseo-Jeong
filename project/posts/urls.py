from django.urls import path, include
from posts.views import *
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()    # DefaultRouter 인스턴스 생성
router.register('', views.PostViewSet)  # ViewSet이 기본 경로(/)에서 처리됨

urlpatterns = [
    # 기본 경로(/)에선 router가 처리
    # router.urls는 등록된 ViewSet에 대한 URL 패턴을 자동으로 생성
    path('', include(router.urls)),
]

urlpatterns = [
    path('posts/', views.post_list),
    path('post/<int:pk>/', views.post_detail),
    path('comments/', views.comment_list),
    path('comment/<int:pk>/', views.comment_detail),    

    # path('posts/', PostListGenericAPIView.as_view()),
    # path('posts/<int:pk>/', PostDetailGenericAPIView.as_view()),
    # path('comments/', CommentListMixins.as_view()),
    # path('comments/<int:pk>/', CommentDetailMixins.as_view()),

    # path('posts/', PostListMixins.as_view()),
    # path('posts/<int:pk>/', PostDetailMixins.as_view()),
    # path('comments/', CommentListMixins.as_view()),
    # path('comments/<int:pk>/', CommentDetailMixins.as_view())

    # # (Class Name).as_view() 방식으로 view를 연동
    # path('', PostList.as_view()),
    # path('<int:id>/', PostDetail.as_view()),
    # path('comments/', CommentList.as_view()),
    # path('comments/<int:id>/', CommentDetail.as_view()),

    # path('', hello_world, name = 'hello_world'),
    # path('introduction', introduction, name = 'introduction'),
    # path('<int:post_id>/', post_detail, name = 'post_detail'),
    # path('post_detail/', get_post_all, name = 'post_all'),
    # path('new/', create_post, name = "create_post"),
    # path('newcomment/<int:post_id>/', create_comment, name = "create_comment"),
    # path('', get_post_all, name = "get_post_all"),
    # path('comment/<int:post_id>/', get_comment, name = 'get_comment')
]
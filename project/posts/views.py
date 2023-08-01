from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.views.decorators.http import require_http_methods
from .models import Post, Comment
from django.db import models
import json

# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '메시지 전달 성공!',
            'data' : "Hello world",
        })
    
def introduction(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'succes' : True,
            'message' : '메세지 전달 성공!',
            'data':[
                {
                    "name" : "정현서",
                    "age" : 26,
                    "major" : "소프트웨어학부"
                },
                {
                    "name" : "양희철",
                    "age" : 24,
                    "major" : "산업보안학과",
                }
            ]            
        })
    
@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, post_id):
    if request.method == "GET":
        post = get_object_or_404(Post, pk = post_id)

        category_json = {
            "id"        : post.post_id,
            "writer"    : post.writer,
            "content"   : post.content,
            "category"  : post.category,
        }

        return JsonResponse({
            'status'    : 200,
            'message'   : '게시글 조회 성공',
            'data'      : category_json
        })
    
    elif request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        update_post = get_object_or_404(Post, pk = post_id)

        update_post.content = body['content']
        update_post.category = body['category']
        update_post.save()

        update_post_json = {
            "id": update_post.post_id,
            "writer": update_post.writer,
            "content": update_post.content,
            "category": update_post.category,
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 수정 성공',
            'data': update_post_json
        })
    
    elif request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk = post_id)
        delete_post.delete()

        return JsonResponse({
            'status': 200,
            'message': '게시글 삭제 성공',
            'data': None
        })

@require_http_methods(["GET"])
def get_post_all(request):
    posts = Post.objects.all()

    post_list = list(posts.values())

    return JsonResponse({
        'status'    : 200,
        'message'   : '모든 게시글 조회 성공',
        'data'      : post_list
    })

@require_http_methods(["POST"])
def create_post(request):
    # 데이터는 주로 body
    body = json.loads(request.body.decode('utf-8'))
    image_file = request.FILES.get('image')

    # ORM을 통해 새로운 데이터를 DB에 생성함
    new_post = Post.objects.create(
        writer = body['writer'],
        content = body['content'],
        category = body['category'],
    )

    # Response에서 보여질 데이터 내용을 Json 형태로 만듦
    new_post_json = {
        "id": new_post.post_id,
        "writer": new_post.writer,
        "content": new_post.content,
        "category": new_post.category,
    }

    return JsonResponse({
        'status': 200,
        'message': '게시글 목록 조회 성공',
        'data': new_post_json
    })

@require_http_methods(["GET"])
def get_post_all(request):
    post_all = Post.objects.all()

    post_json_all = []
    for post in post_all:
        post_json = {
            "id": post.post_id,
            "writer": post.writer,
            "category": post.category
        }

        post_json_all.append(post_json)

    return JsonResponse({
        'status': 200,
        'message': '게시글 목록 조회 성공',
        'data': post_json_all
    })

@require_http_methods(["GET"])
def get_comment(request, post_id):
    comments = Comment.objects.filter(post = post_id)

    comment_json_list = []
    for comment in comments:
        comment_json = {
            'writer': comment.writer,
            'content': comment.content
        }

        comment_json_list.append(comment_json)

    return JsonResponse({
        'status': 200,
        'message': '댓글 읽어오기 성공!',
        'data': comment_json_list
    })

@require_http_methods(["POST"])
def create_comment(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    body = json.loads(request.body.decode('utf-8'))

    new_comment = Comment.objects.create(
        writer = body['writer'],
        content = body['content'],
        post = post
    )

    new_comment_json = {
        "writer": new_comment.writer,
        "content": new_comment.content,
    }

    return JsonResponse({
        'status': 200,
        'message': '댓글 생성 성공!',
        'data': new_comment_json
    })

# 8주 차
from .serializers import PostSerializer, CommentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Create: 게시글 작성하기
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        posts = Post.objects.all()

        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)       
    
class PostDetail(APIView):
    def get(self,request, id):
        post = get_object_or_404(Post, id = id)
        
        serializer = PostSerializer(post)

        return Response(serializer.data)
    
    def put(self, request, id):
        post = get_object_or_404(Post, id=id)

        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)

        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)     

class CommentList(APIView):
    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, format=None):
        comments = Comment.objects.all()

        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)

class CommentDetail(APIView):
    def get(self, request, id):
        comment = get_object_or_404(Comment, id=id)

        serializer = CommentSerializer(comment)

        return Response(serializer.data)

    def put(self, request, id):
        comment = get_object_or_404(Comment, id=id)

        serializer = CommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        comments = get_object_or_404(Comment, id=id)

        comments.delete()

        return Response(stauts = status.HTTP_204_NO_CONTENT)


# 9주 차

# Mixin
from rest_framework.response import Response
from rest_framework import generics, mixins
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostListMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()   # 모든 게시물 가져옴
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):    # HTTP GET 요청 처리
        return self.list(request)   # 모든 게시물 반환
    
    def post(self, request, *args, **kwargs):   # HTTP POST 요청 처리
        return self.create(request, *args, **kwargs)    # 새 게시물 생성
    
class PostDetailMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()   # 모든 게시물 가져옴
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):    # HTTP GET 요청 처리
        return self.retrieve(request, *args, **kwargs)  # 특정 게시물 반환
    
    def put(self, request, *args, **kwargs):    # HTTP PUT 요청 처리
        return self.update(request, *args, **kwargs)    # 게시물 업데이트
    
    def delete(self, request, *args, **kwargs): # HTTP DELETE 요청 처리
        # delete() 대신 mixins.DestroyModelMixin의 destroy() 사용 
        return self.destroy(request, *args, **kwargs)    # 게시물 삭제
    

# challenge (1)
class CommentListMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request)
    
    def post(self, requset, *args, **kwargs):
        return self.create()

class CommentDetailMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Concrete Generic Views
from rest_framework import generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostListGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()   # API View가 처리할 대상 객체를 지정한다.
    serializer_class = PostSerializer   # API View가 사용할 Serializer를 지정한다.

class PostDetailGenericAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()   # 이 API View가 처리할 대상 객체를 지정한다.
    serializer_class = PostSerializer   # API View가 사용할 Serializer를 지정한다.


# challenge (2)
class CommentListGenericAPIView():
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailGenericAPIView():
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# ViewSet
from django.shortcuts import render
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()   # API View가 처리할 대상 객체를 지정한다.
    serializer_class = PostSerializer   # API View가 사용할 Serializer를 지정한다.

# post_list View
post_list = PostViewSet.as_view({
    'get': 'list',  # GET 요청: list 메서드 호출
    'post': 'create',   # POST 요청: create 메서드 호출
})

# post_detail View
post_detail = PostViewSet.as_view({
    'get': 'retrieve',  # GET 요청: retrieve 메서드 호출(개별 Post 객체 조회)
    'put': 'update',    # PUT 요청: update 메서드 호출
    'patch': 'partial_update',  # PATCH 요청: partial_update 메서드 호출(개별 Post 객체의 일부 수정)
    'delete': 'destroy',    # DELETE 요청: destroy 메서드 호출
})


# challenge (3)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})


# # @action decorator
# from rest_framework.decorators import action
# from rest_framework.response import Response

# class YourModelViewSet(viewsets.ModelViewSet):
#     queryset = YourModel.objects().all()    # ViewSet이 처리할 모델 객체들의 queryset
#     serializer_class = YourModelSerializer

#     # @action을 통해 custom_action이라는 이름의 추가적인 action 정의
#     # detail=True: 이 action이 개별 모델 인스턴스에 대해 수행됨
#     # method=['post']: 이 action이 POST 요청에 응답하도록 함
#     @action(detail=True, methods=['post'])
#     def custom_action(self, request, pk=None):
#         return Response("Custom action executed!")
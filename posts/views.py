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

    # ORM을 통해 새로운 데이터를 DB에 생성함
    new_post = Post.objects.create(
        writer = body['writer'],
        content = body['content'],
        category = body['category']
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


# DRF(Django REST Framework)
from .serializers import PostSerializer, CommentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status   # 상태 코드를 넘겨줌
from django.http import Http404

class PostList(APIView):
    # Create: 게시글 작성하기
    def post(self, request, format=None):
        # request.data를 이용하여 PostSerializer 인스턴스 생성
        serializer = PostSerializer(data=request.data)

        # 데이터 유효성 검사 및 저장
        if serializer.is_vaild():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # 데이터가 유효하지 않다면, serializer.errors를 이용하여 에러 정보 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Read: 게시글 불러오기
    def get(self, request, format=None):
        posts = Post.objects.all()  # DB에서 모든 Post 객체를 QuerySet 객체로 받아 옴
        serializer = PostSerializer(posts, many=True)   # Post 객체 직렬화(many=True: 여러 개의 객체 직렬화)

        return Response(serializer.data)
    
class PostDetail(APIView):
    # Read: 게시글 불러오기    
    def get(self, request, id):
        post = get_object_or_404(Post, post_id=id)   # 해당 id를 갖는 게시물에 대한 객체 반환(없다면 에러 반환)
        serializer = PostSerializer(post)   # 찾은 객체를 직렬화

        return Response(serializer.data)
    
    # Update: 게시글 수정하기
    def put(self, request, id): # put은 게시물 전체 정보를 포함해야 함(일부라면 patch)
        post = get_object_or_404(Post, post_id=id)
        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
    # Delete: 게시글 삭제하기    
    def delete(self, request, id):
        post = get_object_or_404(Post, post_id=id)   # 해당 id를 갖는 게시물에 대한 객체 반환(없다면 에러 반환)
        
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)  # 삭제 후 HTTP_204_NO_CONTENT 상태 코드만 반환
    

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
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
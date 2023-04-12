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


# 아래는 삭제
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
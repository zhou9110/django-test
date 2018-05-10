from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.core import serializers


# /post/posts/
@api_view(['GET'])
def post_posts(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        posts = Post.objects.filter(user_id=request.user.id)
        response = []
        for post in posts:
            serializer = PostSerializer(post)
            response.append(serializer.data)
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_POSTS_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/posts/<uid>/
@api_view(['GET'])
def post_posts_by_uid(request, uid):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        posts = Post.objects.filter(user_id=uid)
        response = []
        for post in posts:
            serializer = PostSerializer(post)
            response.append(serializer.data)
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_POSTS_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/post/<id>/
@api_view(['GET'])
def post_post(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_POSTS_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/create/
@api_view(['POST'])
def post_create(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        data = request.data
        post = Post.objects.create(
            user=request.user,
            text=data['text'],
            images=data['images'],
            location=data['location']
        )
        post.save()
        if ('tags' in data):
            for tag in data['tags']:
                t = Tag.objects.filter(name=tag)
                if (not len(t)):
                    new_tag = Tag.objects.create(name=tag)
                    post.tags.add(new_tag)
                else:
                    old_tag = Tag.objects.get(name=tag)
                    post.tags.add(old_tag)
        return JsonResponse({
                "command"   :   "CREATE_POST_SUCCESS"
            }, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "CREATE_POST_FAILED",
                "info"      :   str(e)
            }, status=400)
    
# /post/update/<id>/
@api_view(['PUT'])
def post_update(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        post = Post.objects.get(pk=pk, user_id=request.user.id)
        data = request.data
        data['user'] = request.user.id
        tags = []
        if ('tags' in data):
            for tag in data['tags']:
                t = Tag.objects.filter(name=tag)
                if (not len(t)):
                    new_tag = Tag.objects.create(name=tag)
                    tags.append(new_tag.id)
                else:
                    old_tag = Tag.objects.get(name=tag)
                    tags.append(old_tag.id)
        data['tags'] = tags
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        return JsonResponse({
                "command"   :   "UPDATE_POST_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/comment/<id>/
@api_view(['POST'])
def post_comment(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        data = request.data
        post = Post.objects.get(pk=pk)
        comment = Comment.objects.create(
            post=post, 
            user=request.user,
            text=data['text']
        )
        comment.save()
        return JsonResponse({
                "command"   :   "COMMENT_SUCCESS"
            }, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "COMMENT_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/like/<id>/
@api_view(['POST'])
def post_like(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        data = request.data
        post = Post.objects.get(pk=pk)
        like = Comment.objects.create(
            post=post, 
            user=request.user
        )
        like.save()
        return JsonResponse({
                "command"   :   "LIKE_SUCCESS"
            }, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "LIKE_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/tag/<id>/
@api_view(['GET'])
def post_tag(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        tag = Tag.objects.get(pk=pk)
        serializer = TagSerializer(tag)
        return JsonResponse(serializer.data)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_TAG_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/convert_tags/
@api_view(['POST'])
def post_convert_tags(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        data = request.data
        response = []
        for i in data['tags']:
            tag = Tag.objects.get(pk=i)
            serializer = TagSerializer(tag)
            response.append(serializer.data)
        return JsonResponse(response, safe=False)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_TAGS_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/create_tag/
@api_view(['POST'])
def post_create_tag(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        data = request.data
        tag = Comment.objects.create(
            name=data['name']
        )
        tag.save()
        return JsonResponse({
                "command"   :   "CREATE_TAG_SUCCESS"
            }, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "CREATE_TAG_FAILED",
                "info"      :   str(e)
            }, status=400)

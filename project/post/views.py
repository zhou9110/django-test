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
        return JsonResponse(response, safe=False)
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
        return JsonResponse(response, safe=False)
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
                "command"   :   "GET_POST_FAILED",
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

# /post/create_comment/<id>/
@api_view(['POST'])
def post_create_comment(request, pk):
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

# /post/comments/<pid>/
@api_view(['GET'])
def post_comments(request, pid):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        comments = Comment.objects.filter(post_id=pid)
        response = []
        for comment in comments:
            serializer = CommentSerializer(comment)
            response.append(serializer.data)
        return JsonResponse(response, safe=False)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_COMMENTS_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/create_like/<id>/
@api_view(['POST'])
def post_create_like(request, pk):
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

# /post/likes/<pid>/
@api_view(['GET'])
def post_likes(request, pid):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        likes = Like.objects.filter(post_id=pid)
        response = []
        for like in likes:
            serializer = LikeSerializer(like)
            response.append(serializer.data)
        return JsonResponse(response, safe=False)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_LIKES_FAILED",
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

# /post/create_collection/
@api_view(['POST'])
def post_create_collection(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        data = request.data
        collection = Collection.objects.create(
            user=request.user,
            name=data['name']
        )
        collection.save()
        return JsonResponse({
                "command"   :   "CREATE_COLLECTION_SUCCESS"
            }, status=200)
    except Exception as e:
        return JsonResponse({
                "command"   :   "CREATE_COLLECTION_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/collection/<id>/
@api_view(['GET'])
def post_collection(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        collection = Collection.objects.get(pk=pk)
        serializer = CollectionSerializer(collection)
        return JsonResponse(serializer.data)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_COLLECTION_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/collections/
@api_view(['GET'])
def post_collections(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        collections = Collection.objects.filter(user_id=request.user.id)
        response = []
        for collection in collections:
            serializer = CollectionSerializer(collection)
            response.append(serializer.data)
        return JsonResponse(response, safe=False)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_COLLECTIONS_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/collections/<uid>/
@api_view(['GET'])
def post_collections_by_uid(request, uid):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        collections = Collection.objects.filter(user_id=uid)
        response = []
        for collection in collections:
            serializer = CollectionSerializer(collection)
            response.append(serializer.data)
        return JsonResponse(response, safe=False)
    except Exception as e:
        return JsonResponse({
                "command"   :   "GET_COLLECTIONS_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/update_collection/append/<id>/
@api_view(['PUT'])
def post_update_collection_append(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        data = request.data
        collection = Collection.objects.get(pk=ok)
        # append post to collection here ...
        serializer = CollectionSerializer(collection)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        return JsonResponse({
                "command"   :   "UPDATE_COLLECTION_APPEND_FAILED",
                "info"      :   str(e)
            }, status=400)

# /post/update_collection/remove/<id>/
@api_view(['PUT'])
def post_update_collection_remove(request, pk):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        data = request.data
        collection = Collection.objects.get(pk=ok)
        # delete post from collection here ...
        serializer = CollectionSerializer(collection)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        return JsonResponse({
                "command"   :   "UPDATE_COLLECTION_REMOVE_FAILED",
                "info"      :   str(e)
            }, status=400)

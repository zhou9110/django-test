from django.shortcuts import render


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

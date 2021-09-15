from django.shortcuts import render
from rest_framework import serializers
from ..posts import posts
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.response import Response
from ..models import Post,Review
from ..serializers import PostSerializer

from rest_framework import status

@api_view(['GET'])
def getPosts(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''
    posts= Post.objects.filter(name__icontains=query).order_by('-createdAt')
    page = request.query_params.get('page')
    paginator = Paginator(posts, 3)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    print('Page:', page)
    serializer = PostSerializer(posts, many=True)
    return Response({'posts': serializer.data, 'page': page, 'pages': paginator.num_pages})

@api_view(['GET'])
def getPost(request, pk):
    post = Post.objects.get(_id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deletePost(request, pk):
    post = Post.objects.get(_id=pk)
    post.delete()
    return Response('Post Deleted')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createPost(request):
    user = request.user

    post = Post.objects.create(
        user=user,
        name='Sample Name',
        price=0,
        category='Sample Category',
        description=''
    )

    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updatePost(request, pk):
    data = request.data
    post = Post.objects.get(_id=pk)

    post.name = data['name']
    post.price = data['price']
    post.category = data['category']
    post.description = data['description']

    post.save()

    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def uploadImage(request):
    data = request.data

    post_id = data['post_id']
    post = Post.objects.get(_id=post_id)

    post.image = request.FILES.get('image')
    post.save()

    return Response('Image was uploaded')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createPostReview(request, pk):
    user = request.user
    post = Post.objects.get(_id=pk)
    data = request.data

    # 1 - Review already exists
    alreadyExists = post.review_set.filter(user=user).exists()
    if alreadyExists:
        content = {'detail': 'post already reviewed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 - Create review
    else:
        review = Review.objects.create(
            user=user,
            post=post,
            name=user.first_name,
            title=data['title'],
            comment=data['comment'],
        )

        reviews = post.review_set.all()
        post.numReviews = len(reviews)
        post.save()

        return Response('Review Added')

@api_view(['GET'])
def getTopPosts(request):
    posts = Post.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyPosts(request):
    user = request.user
    posts = user.post_set.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
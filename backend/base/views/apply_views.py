from django.db.models.fields import PositiveSmallIntegerField
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from rest_framework.response import Response
from ..models import Post, Apply, ApplyItem,ManageInfo
from ..serializers import PostSerializer, ApplySerializer,ApplyItemSerializer

from rest_framework import status
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addApplyItems(request):
    user =request.user
    data=request.data
    applyItems = data['applyItems']

    if applyItems and len(applyItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        #Create apply
        for i in applyItems:
            post = Post.objects.get(_id=i['post'])
            apply=Apply.objects.create(
                user=user,
                post=post,
                paymentMethod=data['paymentMethod'],
                cartnumber=data['cartnumber'],
                cartname=data['cartname'],
                date=data['date'],
                securitycode=data['securitycode'],

            )
        #Create manageInfo
        manageinfo = ManageInfo.objects.create(
            apply=apply,
            message=data['manageInfo']['message'],
            cv=data['manageInfo']['cv'],
        )
        #create applyıtems and set apply to apply ıtems relationship
        for i in applyItems:
            post = Post.objects.get(_id=i['post'])

            item = ApplyItem.objects.create(
                post=post,
                apply=apply,
                name=post.name,
                price=i['price'],
                image=post.image.url,
            )

        #update stock
        post.save()
    serializer=ApplySerializer(apply, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getApplyById(request,pk):
    user = request.user
    try:
        apply = Apply.objects.get(_id=pk)
       
        serializer = ApplySerializer(apply, many=False)
        return Response(serializer.data)
    
    except:
        return Response({'detail': 'Apply does not exist'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateApplyToPaid(request, pk):
    apply = Apply.objects.get(_id=pk)

    apply.isPaid = True
    apply.paidAt = datetime.now()
    apply.save()

    return Response('Order was paid')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyApplies(request):
    user = request.user
    applies = user.apply_set.all()
    serializer = ApplySerializer(applies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getApplies(request):
    applies = Apply.objects.all()
    serializer = ApplySerializer(applies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPostApplies(request):
    user = request.user
    posts = user.post_set.all()
    applies = Apply.objects.all().filter(post__in=posts).order_by('-createdAt')
    serializer = ApplySerializer(applies, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateApplyToDelivered(request, pk):
    apply = Apply.objects.get(_id=pk)
    apply.isNotDelivered = False

    apply.isDelivered = True
    
    apply.save()

    return Response('Apply has been accepted')


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateApplyToNotDelivered(request, pk):
    apply = Apply.objects.get(_id=pk)
    apply.isDelivered = False

    apply.isNotDelivered = True
    
    apply.save()

    return Response('Apply has declined')



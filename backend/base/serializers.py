from django.db.models import manager
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Apply,ApplyItem,ManageInfo,Review
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin']
    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff 

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name

class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class PostSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class ManageInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManageInfo
        fields = ['_id', 'message', 'cv']


class ApplyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyItem
        fields = '__all__'

class ApplySerializer(serializers.ModelSerializer):
    applyItems = serializers.SerializerMethodField(read_only=True)
    manageInfo = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Apply
        fields = '__all__'

    def get_applyItems(self, obj):
        items = obj.applyitem_set.all()
        serializer =ApplyItemSerializer(items, many=True)
        return serializer.data

    def get_manageInfo(self, obj):
        try:
            address= ManageInfoSerializer(obj.manageinfo, many=False).data
        except:
            address =False
        return address

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
       

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
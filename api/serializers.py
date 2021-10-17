from rest_framework.serializers import ModelSerializer
from backend.models import Post, ProductReview, MediaManager


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'


class MediaSerializer(ModelSerializer):
    class Meta:
        model = MediaManager
        fields = '__all__'

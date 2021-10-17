from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from django.http import Http404


@api_view(['GET'])
def api_preview(request):
    context = {
        'Post Page': [
            '/api/page',
            '/api/page/<pk>'
        ],
        'Product Page': [
            '/api/product',
            '/api/product/<pk>'
        ],
        'Media API': [
            '/api/media',
            '/api/media/<pk>'
        ]
    }
    return Response(context)


class PostEndPoint(APIView):
    def get(self, format=None):
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    def post(self, format=None):
        serializer = PostSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail_end_point(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
    except Post.DoesNotExist:
        return Http404

    if request.method == 'GET':
        serializer = PostSerializer(post, many=False)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = PostSerializer(post, many=False, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class ProductEndPoint(APIView):
    def get(self, format=None):
        pro = ProductReview.objects.all()
        serializer = ProductSerializer(pro, many=True)
        return Response(serializer.data)

    def post(self, format=None):
        serializer = ProductSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_end_point(request, pk):
    try:
        product = get_object_or_404(ProductReview, pk=pk)
    except ProductReview.DoesNotExist:
        return Http404

    if request.method == 'GET':
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, many=False, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class MediaEndPoint(APIView):
    def get(self, format=None):
        media = MediaManager.objects.all()
        serializer = MediaSerializer(media, many=True)
        return Response(serializer.data)

    def post(self, format=None):
        serializer = MediaSerializer(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def media_detail_emd_point(request, pk):
    try:
        media = get_object_or_404(MediaManager, pk=pk)
    except MediaManager.DoesNotExist:
        return Http404

    if request.method == 'GET':
        serializer = MediaSerializer(media, many=False)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        media.delete()
        return Response(status.HTTP_204_NO_CONTENT)

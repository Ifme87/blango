from rest_framework import generics, viewsets
from blango_auth.models import User
from blog.api.serializers import (
    PostSerializer, 
    UserSerializer, 
    PostDetailSerializer,
    TagSerializer,
)
from blog.models import Post, Tag
from rest_framework.authentication import SessionAuthentication
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()

    #to use Different serializers for Different views
    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return PostSerializer
        return PostDetailSerializer


class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    @action(methods=["get"], detail=True, name="Posts with the Tag")
    def posts(self, request, pk=None):
        tag = self.get_object()
        post_serializer = PostSerializer(
            tag.posts, many=True, context={"request": request}
        )
        return Response(post_serializer.data)

# Just for info. Different ways to implement the same api views:

'''
import json
from http import HTTPStatus
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from blog.api.serializers import PostSerializer
from blog.models import Post
'''

#  with and w/o serializers:

'''
#def post_to_dict(post):
#    return {
#        "pk": post.pk,
#        "author_id": post.author_id,
#        "created_at": post.created_at,
#        "modified_at": post.modified_at,
#        "published_at": post.published_at,
#        "title": post.title,
#        "slug": post.slug,
#        "summary": post.summary,
#        "content": post.content,
#    }


@csrf_exempt
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all()
        # w/o serializers:
        #
        #posts_as_dict = [post_to_dict(p) for p in posts]
        #return JsonResponse({"data": posts_as_dict})
        return JsonResponse({"data": PostSerializer(posts, many=True).data})
    elif request.method == "POST":
        post_data = json.loads(request.body)
        # w/o serializers:
        #
        #post = Post.objects.create(**post_data)
        serializer = PostSerializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return HttpResponse(
            status=HTTPStatus.CREATED,
            headers={"Location": reverse("api_post_detail", args=(post.pk,))},
        )

    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "GET":
        # w/o serializers:
        #return JsonResponse(post_to_dict(post))
        return JsonResponse(PostSerializer(post).data)
    elif request.method == "PUT":
        post_data = json.loads(request.body)
        #for field, value in post_data.items():
        #    setattr(post, field, value)
        #post.save()
        serializer = PostSerializer(post, data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)
    elif request.method == "DELETE":
        post.delete()
        return HttpResponse(status=HTTPStatus.NO_CONTENT)

    return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])
'''

# with a use of 'api_view' decorator

'''
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET", "POST"])
def post_list(request, format=None):
    if request.method == "GET":
        posts = Post.objects.all()
        return Response({"data": PostSerializer(posts, many=True).data})
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(
                status=HTTPStatus.CREATED,
                headers={"Location": reverse("api_post_detail", args=(post.pk,))},
            )
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def post_detail(request, pk, format=None):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=HTTPStatus.NOT_FOUND)

    if request.method == "GET":
        return Response(PostSerializer(post).data)
    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
    elif request.method == "DELETE":
        post.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
'''

# with a use of APIView class

'''
class PostDetail(APIView):
    @staticmethod
    def get_post(pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk, format=None):
        post = self.get_post(pk)
        return Response(PostSerializer(post).data)

    def put(self, request, pk, format=None):
        post = self.get_post(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_post(pk)
        post.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
'''

# with a use of mixins and generics

'''
from rest_framework import mixins
from rest_framework import generics


class PostList(
    mixins.ListModelMixin, 
    mixins.CreateModelMixin, 
    generics.GenericAPIView
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
'''

# with mixins and generics, shorter version, with authentication and permissions

'''
class PostList(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
'''
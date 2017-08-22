from django.contrib.auth.models import User
from restfulapi.permissions import IsOwnerOrReadOnly
from restfulapi.serializers import UserSerializer
from .models import Snippet
from .serializers import SnippetSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets




class UserViewSet(viewsets.ModelViewSet):
    """
    this viewset automatically provides 'list' and detail actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer



class SnippetViewSet(viewsets.ModelViewSet):
    """
        this viewset automatically provides 'list' and detail actions
        additionaly we provide an extra highlight action
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
"""
MIXIN BASED VIEWS

from .models import Snippet
from .serializers import SnippetSerializer
from rest_framework import mixins
from rest_framework import generics


class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)




class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""


"""
Class based Api Views

from django.http.response import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from restfulapi.models import Snippet
from restfulapi.serializers import SnippetSerializer


class SnippetList(APIView):
    #list all or create new code snippet
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SnippetDetail(APIView):
    #retrieve or update,delete a a code snippet
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)

        except Snippet.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request,pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            #save the object instance for the user called meth
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""

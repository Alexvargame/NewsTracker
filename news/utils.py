import datetime

from django.shortcuts import render,redirect, reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action


from .models import NewsThemes
from .serializers import NewsThemesSerializer,NewsThemesCreateSerializer
from django.contrib.auth.models import User

def main_page(request):
    return render(request, 'news/main_page.html')

class ObjectListMixin:
    serializer = None
    template = None
    template_name = None
    model = None
    def get(self,request):
        objs=self.model.objects.all()
        serializer=self.serializer(objs,many=True)
        return Response({self.model.__name__.lower():objs})

class ObjectCreateMixin:
    serializer = None
    template = None
    template_name = None
    model = None
    def get(self,request):
        serializer = self.serializer()
        return Response({'serializer':serializer})

    def post(self,request):
        serializer=self.serializer(data=request.data)
        if serializer.is_valid():
            new_obj=serializer.save()
            return redirect(new_obj)
        else:
            return Response({'serializer':serializer})

class ObjectUpdateMixin:
    serializer = None
    serializer_update=None
    template = None
    template_name = None
    model = None
    def get(self,request,pk):
        obj=self.model.objects.get(id=pk)
        serializer=self.serializer(obj)
        return Response({'serializer':serializer, self.model.__name__.lower()[:-1]:obj})

    def post(self,request,pk):
        obj=self.model.objects.get(id=pk)
        serializer=self.serializer(obj,data=request.data)
        if serializer.is_valid():
            new_obj=serializer.save()
            return redirect(new_obj)
        else:
            return Response({'serializer':serializer, self.model.__name__.lower()[:-1]:new_obj})

class ObjectDetailMixin:
    serializer = None
    serializer_comments = None
    template = None
    template_name = None
    model = None
    def get(self, request, pk):

        obj = self.model.objects.get(id=pk)
        serializer = self.serializer(obj)
        serializer_comments = self.serializer_comments
        return Response({'serializer_comments':serializer_comments,self.model.__name__.lower()[:-1]:obj})

class ObjectDeleteMixin:
    serializer = None
    template = None
    template_name = None
    model = None
    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        return render(request, self.template_name, context={self.model.__name__.lower()[:-1]: obj})
    def post(self,request,pk):
        obj=self.model.objects.get(id=pk)
        obj.delete()
        return redirect(reverse(self.template))

class ViewModelSetMixin:
    serializer = None
    serializer_create = None
    template_dict = None
    model = None

    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return self.serializer_create
        else:
            return self.serializer

    # def get_template_names(self):
    #     return [self.template_dict[self.action]]

    def list(self, request):
        serializer = self.serializer(self.get_queryset(), many=True)
        return Response(serializer.data)#{'serializer':serializer, self.model.__name__.lower():self.get_queryset()[:10]})

    def create(self, request):
        serializer = self.serializer_create(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=401)

    def retrieve(self, request, pk=None):
        obj = self.model.objects.get(id=pk)
        serializer = self.serializer(obj)
        return Response(serializer.data)#{'serializer':serializer, self.model.__name__.lower()[:-1]:obj})

    def update(self, request, pk=None):
        new = self.model.objects.get(id=pk)
        serializer = self.serializer_create(new, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(status=401)

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        new = self.model.objects.get(id=pk)
        new.delete()
        news=self.model.objects.all()
        serialiser=self.serializer(news, many=True)
        return Response(serialiser.data)
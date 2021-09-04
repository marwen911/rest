from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics,mixins,viewsets
from rest_framework.filters import SearchFilter


# 1 without Rest and no model query FBV
def no_rest_no_model(requset):
    guests=[
        {
        'id':1,
        'name':'marwen',
        'mobile':54741
        },
    {
        'id': 2,
        'name': 'majd',
        'mobile': 54742
    }
    ]
    return JsonResponse(guests,safe=False)
# 2 model data default without Rest
def no_rest_from_model(requset):
    data =Guest.objects.all()
    responce={
        'guests':list(data.values('name','mobile'))
    }
    return JsonResponse(responce)

#list=GET
#create==POST

#Pk query==GET
#Upadate ==PUT
#Delete==DELETE


# function based views
#3.1 GET POST
@api_view(['GET','POST'])
def Fbv_list(request):

    #GET
    if request.method=='GET':
        gustes=Guest.objects.all()
        serializer=GuestSerializers(gustes,many=True)
        return Response(serializer.data)
    # POST
    elif request.method=='POST':
        serializer=GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

#3.2 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def Fbv_pk(request,pk):

    try:
        g=Guest.objects.get(pk=pk)

    except Guest.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    # GET
    if request.method == 'GET':
        serializer = GuestSerializers(g)
        return Response(serializer.data)
    # PUT
    if request.method=='PUT':
        serializer = GuestSerializers(g,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method=='DELETE':
        g.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

#4 CBV class base viems
#4.1 List and create ==GET and POST
class CBV_list(APIView):
    def get (self,request):
        gustes=Guest.objects.all()
        serializer=GuestSerializers(gustes,many=True)
        return Response(serializer.data)
    def post (self,request):
        serializer=GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

#4.2 GET PUT DELETE class based views --pk
class CBV_pk(APIView):
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
    def get(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializers(guest)
        return Response(serializer.data)
    def put(self,request,pk):
        guest=self.get_object(pk)
        serializer = GuestSerializers(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,reqest,pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# 5 mixins
# 5.1 mixins list
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class=GuestSerializers
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)
# 5.2 mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class=GuestSerializers
    def get(self,request,pk):
        return self.retrieve(request)
    def put(self,request,pk):
        return self.update(request)
    def delete(self,request,pk):
        return self.destroy(request)

#6 generics
#6.1 get and post
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
#6.1 get and post
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers

# 7 viewsets
class viewset_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializers
class viewset_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers
    filters_backends=[filters.SearchFilter]
    search_fields=['movie']

class viewset_reservations(viewsets.ModelViewSet):
    queryset = Reservations.objects.all()
    serializer_class = ReservationsSerializers


@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    serializer = MovieSerializers(movies, many= True)
    return Response(serializer.data)
@api_view(['POST'])
def new_reservation(request):

    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservations()
    reservation.guest = guest
    reservation.movie = movie

    reservation.save()

    return Response(status=status.HTTP_201_CREATED)
from rest_framework import serializers
from tickets.models import *

class MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields='__all__'


class ReservationsSerializers(serializers.ModelSerializer):
    class Meta:
        model=Reservations
        fields='__all__'

class GuestSerializers(serializers.ModelSerializer):
    class Meta:
        model=Guest
        fields=['pk','reservations','name','mobile']
from .models import Dht
from .serializers import DHTserialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import rest_framework

@api_view(["GET","POST"])
def dhtser(request):
    if request.method=="GET":
        all=Dht.objects.all()
        dataSer=DHTserialize(all,many=True)
        return Response(dataSer.data)
    elif request.method=="POST":
        serial=DHTserialize(data=request.data)
        if serial.is_valid():
            serial.save()
            return Response(serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serial.id, status=status.HTTP_400_CREATED)
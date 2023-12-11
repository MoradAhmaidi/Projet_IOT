from rest_framework import serializers
from .models import Dht
class DHTserialize(serializers.ModelSerializer) :
 class Meta :
  model = Dht
  fields ='__all__'
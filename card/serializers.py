# serializers.py
from rest_framework import serializers
from .models import Cartao,LoteCartoes

class CartaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartao
        fields = '__all__'

class CartaoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cartao
        fields = ['numero', 'lote']

class LoteCartoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoteCartoes
        fields = '__all__'

class UploadCartaoFileSerializer(serializers.Serializer):
    file = serializers.FileField()

from rest_framework import serializers


class ViolationSerializer(serializers.Serializer):
    placa_patente = serializers.CharField(max_length=25)
    timestamp = serializers.DateTimeField()
    comentarios = serializers.CharField()
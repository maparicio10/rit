from rest_framework import serializers

from core.models import Violation, Vehicle


class ViolationSerializer(serializers.Serializer):
    placa_patente = serializers.CharField(max_length=25)
    timestamp = serializers.DateTimeField()
    comentarios = serializers.CharField()


class VehicleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["license_plate", "brand", "color"]


class ViolationListSerializer(serializers.ModelSerializer):
    officer_fullname = serializers.SerializerMethodField()
    vehicle = VehicleDetailSerializer(read_only=True)

    class Meta:
        model = Violation
        fields = ["timestamp", "comments", "vehicle", "officer_fullname"]
        depth = 1

    def get_officer_fullname(self, obj):
        return obj.officer.fullname

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Vehicle, Officer, Violation, Person
from core.serializers import ViolationSerializer, ViolationListSerializer


# Create your views here.
class AddViolationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ViolationSerializer(data=request.data)
        if serializer.is_valid():
            license_plate = serializer.validated_data['placa_patente']
            timestamp = serializer.validated_data['timestamp']
            comments = serializer.validated_data['comentarios']

            try:
                officer = Officer.objects.get(username=request.user.username)
                vehicle = Vehicle.objects.get(license_plate=license_plate)

                violation = Violation.objects.create(
                    timestamp=timestamp,
                    comments=comments,
                    vehicle=vehicle,
                    officer=officer
                )
                violation.save()
                return Response({"message": "Infracción cargada exitosamente."}, status=status.HTTP_200_OK)
            except Vehicle.DoesNotExist:
                return Response({"error": "Vehículo no encontrado con la placa patente proporcionada."},
                                status=status.HTTP_404_NOT_FOUND)
            except Officer.DoesNotExist:
                return Response({"error": "Oficial no encontrado."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


cargar_infraccion = AddViolationAPIView.as_view()


class ViolationReportAPIView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "El correo electrónico es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            return Response({"error": "El correo electrónico proporcionado no es válido."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            person = Person.objects.get(email=email)
            vehicles = person.vehicle_set.all()
            violations = Violation.objects.filter(vehicle__in=vehicles)
            serializer = ViolationListSerializer(violations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response({"error": "Persona no encontrada."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Error inesperado: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


generar_informe = ViolationReportAPIView.as_view()

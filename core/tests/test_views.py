from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.utils import timezone
from core.models import Person, Officer, Vehicle, Violation
import uuid


class AddViolationAPITest(APITestCase):
    def setUp(self):
        self.person = Person.objects.create(
            first_name="John", last_name="Doe", email="john.doe@example.com"
        )
        self.officer = Officer.objects.create_user(
            username="officer1",
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
        )
        self.officer.identification_number = uuid.uuid4().int % 10**10
        self.officer.save()
        self.vehicle = Vehicle.objects.create(
            license_plate="ABC123", brand="Toyota", color="Red", person=self.person
        )

        self.token = str(RefreshToken.for_user(self.officer).access_token)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_cargar_infraccion(self):
        data = {
            "placa_patente": "ABC123",
            "timestamp": timezone.now(),
            "comentarios": "Speeding",
        }
        response = self.client.post(reverse("cargar_infraccion"), data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Infracción cargada exitosamente.")

    def test_cargar_infraccion_vehicle_not_found(self):
        data = {
            "placa_patente": "XYZ999",
            "timestamp": timezone.now(),
            "comentarios": "Speeding",
        }
        response = self.client.post(reverse("cargar_infraccion"), data, format="json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["error"],
            "Vehículo no encontrado con la placa patente proporcionada.",
        )


class ViolationReportAPITest(APITestCase):
    def setUp(self):
        self.person = Person.objects.create(
            first_name="John", last_name="Doe", email="john.doe@example.com"
        )
        self.officer = Officer.objects.create_user(
            username="officer1",
            password="testpassword",
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
        )
        self.officer.identification_number = uuid.uuid4().int % 10**10
        self.officer.save()
        self.vehicle = Vehicle.objects.create(
            license_plate="ABC123", brand="Toyota", color="Red", person=self.person
        )
        self.violation = Violation.objects.create(
            timestamp=timezone.now(),
            comments="Speeding",
            vehicle=self.vehicle,
            officer=self.officer,
        )

    def test_generar_informe(self):
        url = reverse("generar_informe")
        response = self.client.post(
            url, {"email": "john.doe@example.com"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["comments"], "Speeding")
        self.assertEqual(response.data[0]["officer_fullname"], "Jane Doe")

    def test_generar_informe_person_not_found(self):
        url = reverse("generar_informe")
        response = self.client.post(
            url, {"email": "notfound@example.com"}, format="json"
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "Persona no encontrada.")

    def test_generar_informe_missing_email(self):
        url = reverse("generar_informe")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"], "El correo electrónico es obligatorio."
        )

    def test_generar_informe_invalid_email(self):
        url = reverse("generar_informe")
        response = self.client.post(url, {"email": "invalid-email"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"], "El correo electrónico proporcionado no es válido."
        )

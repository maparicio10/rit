from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Person, Officer, Vehicle, Violation
import uuid
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your tests here.
class PersonModelTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com")

    def test_fullname(self):
        self.assertEqual(self.person.fullname, "John Doe")

    def test_str(self):
        self.assertEqual(str(self.person), "John Doe")


class OfficerModelTest(TestCase):
    def setUp(self):
        self.officer = Officer.objects.create_user(username="officer1", first_name="Jane", last_name="Doe",
                                                   email="jane.doe@example.com")
        self.officer.identification_number = uuid.uuid4().int % 10 ** 10
        self.officer.save()

    def test_fullname(self):
        self.assertEqual(self.officer.fullname, "Jane Doe")

    def test_str(self):
        self.assertEqual(str(self.officer), "Jane Doe")

    def test_identification_number(self):
        self.assertTrue(self.officer.identification_number)


class VehicleModelTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.vehicle = Vehicle.objects.create(license_plate="ABC123", brand="Toyota", color="Red", person=self.person)

    def test_str(self):
        self.assertEqual(str(self.vehicle), "ABC123 - Toyota - Red")

    def test_vehicle_relationship(self):
        self.assertEqual(self.vehicle.person, self.person)


class ViolationModelTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.officer = Officer.objects.create_user(username="officer1", first_name="Jane", last_name="Doe",
                                                   email="jane.doe@example.com")
        self.officer.identification_number = uuid.uuid4().int % 10 ** 10
        self.officer.save()
        self.vehicle = Vehicle.objects.create(license_plate="ABC123", brand="Toyota", color="Red", person=self.person)
        self.violation = Violation.objects.create(timestamp=timezone.now(), comments="Speeding", vehicle=self.vehicle,
                                                  officer=self.officer)

    def test_str(self):
        self.assertTrue(str(self.violation).startswith("Violation"))

    def test_violation_relationships(self):
        self.assertEqual(self.violation.vehicle, self.vehicle)
        self.assertEqual(self.violation.officer, self.officer)


class ReferentialIntegrityTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.officer = Officer.objects.create_user(username="officer1", first_name="Jane", last_name="Doe", email="jane.doe@example.com")
        self.officer.identification_number = uuid.uuid4().int % 10**10
        self.officer.save()
        self.vehicle = Vehicle.objects.create(license_plate="ABC123", brand="Toyota", color="Red", person=self.person)

    def test_create_violation_with_nonexistent_vehicle(self):
        with self.assertRaises(ValidationError):
            violation = Violation(timestamp=timezone.now(), comments="Speeding", vehicle_id=999, officer=self.officer)
            violation.full_clean()

    def test_create_violation_with_nonexistent_officer(self):
        with self.assertRaises(ValidationError):
            violation = Violation(timestamp=timezone.now(), comments="Speeding", vehicle=self.vehicle, officer_id=999)
            violation.full_clean()

    def test_delete_person_cascades_to_vehicle(self):
        self.person.delete()
        with self.assertRaises(Vehicle.DoesNotExist):
            Vehicle.objects.get(id=self.vehicle.id)

    def test_delete_vehicle_cascades_to_violation(self):
        violation = Violation.objects.create(timestamp=timezone.now(), comments="Speeding", vehicle=self.vehicle, officer=self.officer)
        self.vehicle.delete()
        with self.assertRaises(Violation.DoesNotExist):
            Violation.objects.get(id=violation.id)

    def test_delete_officer_cascades_to_violation(self):
        violation = Violation.objects.create(timestamp=timezone.now(), comments="Speeding", vehicle=self.vehicle, officer=self.officer)
        self.officer.delete()
        with self.assertRaises(Violation.DoesNotExist):
            Violation.objects.get(id=violation.id)

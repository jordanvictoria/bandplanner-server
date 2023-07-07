import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from bandplannerapi.models import Event, BandUser, EventType

class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'event', 'eventtype', 'banduser']

    def setUp(self):
        self.banduser = BandUser.objects.first()
        token = Token.objects.get(user=self.banduser.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_event(self):
        """
        Ensure we can create a new event.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/events"

        # Define the request body
        data = {
            "event_type": 1,
            "title": "new event",
            "date": "2023-06-22",
            "time": "19:00:00",
            "description": "cool event",
            "user": self.banduser.id
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "new event")
        self.assertEqual(json_response["date"], "2023-06-22")
        self.assertEqual(json_response["time"], "19:00:00")
        self.assertEqual(json_response["description"], "cool event")

    def test_get_event(self):
        """
        Ensure we can get an existing event.
        """

        # Seed the database with a event
        event = Event()
        e_type = EventType.objects.get(pk=1)
        event.event_type = e_type
        event.title = "Monopoly"
        event.date = "2023-06-23"
        event.time = "19:00:00"
        event.description = "cool event"
        event.user = self.banduser

        event.save()

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the event was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["title"], "Monopoly")
        self.assertEqual(json_response["date"], "2023-06-23")
        self.assertEqual(json_response["time"], "19:00:00")
        self.assertEqual(json_response["description"], "cool event")

    def test_change_event(self):
        """
        Ensure we can change an existing event.
        """
        event = Event()
        e_type = EventType.objects.get(pk=1)
        event.event_type = e_type
        event.title = "Monopoly"
        event.date = "2023-06-23"
        event.time = "19:00:00"
        event.description = "cool event"
        event.user = self.banduser

        event.save()

        # DEFINE NEW PROPERTIES FOR EVENT
        data = {
            "event_type": 1,
            "title": "Sorry",
            "date": "2023-06-30",
            "time": "20:00:00",
            "description": "yahoo",
            "user": self.banduser.id
        }

        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET event again to verify changes were made
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["title"], "Sorry")
        self.assertEqual(json_response["date"], "2023-06-30")
        self.assertEqual(json_response["time"], "20:00:00")
        self.assertEqual(json_response["description"], "yahoo")

    def test_delete_event(self):
        """
        Ensure we can delete an existing event.
        """
        event = Event()
        e_type = EventType.objects.get(pk=1)
        event.event_type = e_type
        event.title = "Monopoly"
        event.date = "2023-06-23"
        event.time = "19:00:00"
        event.description = "cool event"
        event.user = self.banduser

        event.save()

        # DELETE the event you just created
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the event again to verify you get a 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

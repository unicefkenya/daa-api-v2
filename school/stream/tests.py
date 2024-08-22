from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse

from core.tests import BaseAPITest


class StreamTests(BaseAPITest):
    def test_creating_stream(self):
        resp = self.create_stream(name="TeStream", base_class="1", school=1)
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

        resp = self.create_stream(name="TeStream", base_class="2", school=1)
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

        resp = self.create_stream(name="testream", base_class="1", school=1)
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.create_stream(name="TeStream", base_class="1", school=1)
        # self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listing_streams(self):
        self.set_authenticated_user(2)
        resp = self.auth_client.get(reverse("list_create_streams"))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_retrieving_stream(self):
        # Id 2 beacause id is automatically created on creating a stream
        resp = self.auth_client.get(reverse("retrieve_update_destroy_stream", kwargs={"pk": 1}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "TheStream")

    @tag("upst")
    def test_updating_stream(self):
        resp = self.auth_client.patch(reverse("retrieve_update_destroy_stream", kwargs={"pk": 1}), data={"name": "Hello"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "Hello")

        resp = self.auth_client.patch(reverse("retrieve_update_destroy_stream", kwargs={"pk": 1}), data={"name": ""})
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        # self.assertEquals(resp.data["name"], "Hello")

    # def test_confirm_stream_on_school_creation(self):
    #     resp=self.client.get(reverse("retrieve_update_destroy_stream",kwargs={"pk":1}))
    #     ##Confirm is admin and non-delete
    #     self.assertEquals(resp.status_code,200)
    # print(resp.json())

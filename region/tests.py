from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.reverse import reverse

from core.tests import BaseAPITest


class RegionTests(BaseAPITest):
    def test_creating_region(self):
        resp = self.create_region(name="TeRegion")
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

    def test_retrieving_region(self):
        resp = self.client.get(reverse("retrieve_update_destroy_region", kwargs={"pk": 1}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "TheRegion")

    def test_updating_region(self):
        resp = self.client.patch(reverse("retrieve_update_destroy_region", kwargs={"pk": 1}), data={"name": "Hello"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "Hello")

    def test_listing_region_districts(self):
        resp = self.auth_client.get(reverse("list_region_districts", kwargs={"pk": 1}))
        self.assertEquals(resp.data["count"], 1)
        self.assertEquals(resp.status_code, 200)

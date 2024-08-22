from rest_framework import status
from rest_framework.reverse import reverse

from core.tests import BaseAPITest


class DistrictTests(BaseAPITest):
    def test_creating_district(self):
        resp = self.create_district(name="TeDistrict")
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

    def test_listing_districts(self):
        # self.set_authenticated_user(2)
        resp = self.auth_client.get(reverse("list_create_districts"))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_retrieving_district(self):
        resp = self.client.get(reverse("retrieve_update_destroy_district", kwargs={"pk": 1}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "TheDistrict")

    def test_updating_district(self):
        resp = self.client.patch(reverse("retrieve_update_destroy_district", kwargs={"pk": 1}), data={"name": "Hello"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "Hello")

    def test_listing_district_villages(self):
        resp = self.auth_client.get(reverse("list_district_villages", kwargs={"pk": 1}))
        # print(resp.json())
        self.assertEquals(resp.data["count"], 1)
        self.assertEquals(resp.status_code, 200)

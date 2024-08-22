from rest_framework import status
from rest_framework.reverse import reverse
from core.tests import BaseAPITest


class CountyTests(BaseAPITest):
    def setUp(self):
        super(CountyTests, self).setUp()
        # self.create_county()

    def test_creating_county(self):
        resp = self.create_county(name="madC")
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listing_county(self):
        resp = self.auth_client.get(reverse("list_create_countys"))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_retrieving_county(self):
        resp = self.auth_client.get(reverse("retrieve_update_destroy_county", kwargs={"pk": 1}))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "madC")

    def test_updating_county(self):
        resp = self.auth_client.patch(reverse("retrieve_update_destroy_county", kwargs={"pk": 1}), data={"name": "madC"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "madC")

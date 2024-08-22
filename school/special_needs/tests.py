from rest_framework import status
from rest_framework.reverse import reverse
from core.tests import BaseAPITest


class SpecialNeedTests(BaseAPITest):
    def setUp(self):
        super(SpecialNeedTests, self).setUp()
        # self.create_special_need()

    def test_creating_special_need(self):
        resp = self.create_special_need(name="madC")
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listing_special_need(self):
        resp = self.auth_client.get(reverse("list_create_special_needs"))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_retrieving_special_need(self):
        resp = self.auth_client.get(reverse("retrieve_update_destroy_special_need", kwargs={"pk": 1}))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "madC")

    def test_updating_special_need(self):
        resp = self.auth_client.patch(reverse("retrieve_update_destroy_special_need", kwargs={"pk": 1}), data={"name": "madC"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "madC")

from rest_framework import status
from rest_framework.reverse import reverse
from core.tests import BaseAPITest


class SupportRequestTests(BaseAPITest):
    def create_support_request(self, school="1", email="micha@micah.com", name="madC", subject="madC", body="1", phone="madC"):
        data = {"school": school, "email": email, "name": name, "subject": subject, "body": body, "phone": phone}
        return self.auth_client.post(reverse("list_create_support_requests"), data=data)

    def setUp(self):
        super(SupportRequestTests, self).setUp()
        self.create_support_request()

    def test_creating_support_request(self):
        resp = self.create_support_request(email="micha@micah.com")
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

    def test_listing_support_request(self):
        resp = self.auth_client.get(reverse("list_create_support_requests"))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_retrieving_support_request(self):
        resp = self.auth_client.get(reverse("retrieve_update_destroy_support_request", kwargs={"pk": 1}))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["email"], "micha@micah.com")

    def test_updating_support_request(self):
        resp = self.auth_client.patch(reverse("retrieve_update_destroy_support_request", kwargs={"pk": 1}), data={"email": "micha@micah.com"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["email"], "micha@micah.com")

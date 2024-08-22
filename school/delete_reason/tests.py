from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse

from core.tests import BaseAPITest


class DeleteReasonTests(BaseAPITest):
    def test_creating_delete_reason(self):
        resp = self.create_delete_reason(name="TeDeleteReason")
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

        resp = self.create_delete_reason(name="TeDeleteReason")
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listing_delete_reasons(self):
        self.set_authenticated_user(2)
        resp = self.auth_client.get(reverse("list_create_delete_reasons"))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_retrieving_delete_reason(self):
        # Id 2 beacause id is automatically created on creating a delete_reason
        resp = self.auth_client.get(reverse("retrieve_update_destroy_delete_reason", kwargs={"pk": 1}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "TheDeleteReason")

    def test_updating_delete_reason(self):
        resp = self.auth_client.patch(reverse("retrieve_update_destroy_delete_reason", kwargs={"pk": 1}), data={"name": "Hello"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "Hello")

    @tag("stds")
    def test_students_delete_reason_stats(self):
        self.create_delete_reason(name="error")
        resp = self.create_delete_reason(name="other")
        # print(resp.json())
        resp = self.auth_client.delete("{}?reason=1&description=Nothing happens".format(reverse("retrieve_update_destroy_student", kwargs={"pk": 1})))
        resp = self.auth_client.delete("{}?reason=2&descriptionSecond for deletion".format(reverse("retrieve_update_destroy_student", kwargs={"pk": 2})))
        resp = self.auth_client.delete("{}?reason=3&description=Noma sana".format(reverse("retrieve_update_destroy_student", kwargs={"pk": 3})))
        resp = self.auth_client.delete("{}?reason=3&description=Wacha tu".format(reverse("retrieve_update_destroy_student", kwargs={"pk": 4})))
        # print(resp.data)
        self.assertEquals(resp.status_code, 204)

        url = reverse("list_dynamic_student_delete_reasonss_statistics", kwargs={"type": "gender"})
        resp = self.auth_client.get(url)
        # print(resp.json())
        self.assertEquals(resp.status_code, 200)

        url = reverse("list_dynamic_student_delete_reasonss_statistics", kwargs={"type": "id"})
        resp = self.auth_client.get(url)
        # print(resp.json())
        print(resp.json()["results"][0])
        self.assertEquals(resp.status_code, 200)

        url = reverse("list_dynamic_student_delete_reasonss_statistics", kwargs={"type": "reason"})
        resp = self.auth_client.get(url)
        # print(resp.json()["results"][0])
        # print(resp.json())
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json()["count"], 3)

        url = reverse("list_dynamic_student_delete_reasonss_statistics", kwargs={"type": "reason-description"})
        resp = self.auth_client.get(url)
        # print(resp.json()["results"][0])
        # print(resp.json())
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json()["count"], 4)

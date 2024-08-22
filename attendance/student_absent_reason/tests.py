from rest_framework import status
from rest_framework.reverse import reverse

from core.tests import BaseAPITest


class StudentAbsentReasonTests(BaseAPITest):
    def test_creating_student_absent_reason(self):
        resp = self.create_student_absent_reason(description="TeStudentAbsentReason")
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listing_student_absent_reasons(self):
        self.set_authenticated_user(2)
        resp = self.auth_client.get(reverse("list_create_student_absent_reasons"))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_retrieving_student_absent_reason(self):
        # Id 2 beacause id is automatically created on creating a student_absent_reason
        resp = self.client.get(reverse("retrieve_update_destroy_student_absent_reason", kwargs={"pk": 1}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["description"], "TheStudentAbsentReason")

    def test_updating_student_absent_reason(self):
        resp = self.client.patch(reverse("retrieve_update_destroy_student_absent_reason", kwargs={"pk": 1}), data={"description": "Hello"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["description"], "Hello")

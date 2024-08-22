from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse

from core.tests import BaseAPITest


class AbsentReasonTests(BaseAPITest):
    def test_creating_absent_reason(self):
        resp = self.create_absent_reason(name="TeAbsentReason")
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

        resp = self.create_absent_reason(name="TeAbsentReason")
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listing_absent_reasons(self):
        self.set_authenticated_user(2)
        resp = self.auth_client.get(reverse("list_create_absent_reasons"))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_retrieving_absent_reason(self):
        # Id 2 beacause id is automatically created on creating a absent_reason
        resp = self.client.get(reverse("retrieve_update_destroy_absent_reason", kwargs={"pk": 1}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "TheAbsentReason")

    def test_updating_absent_reason(self):
        resp = self.client.patch(reverse("retrieve_update_destroy_absent_reason", kwargs={"pk": 1}), data={"name": "Hello"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "Hello")

    @tag("stda")
    def test_students_absent_reason_stats(self):
        self.create_absent_reason(name="error")
        resp = self.create_absent_reason(name="other")
        # print(resp.json())
        resp = self.create_student_absent_reason(reason=1, description="TeStudentAbsentReason1", student=1, date="2019-09-09")
        resp = self.create_student_absent_reason(reason=2, description="TeStudentAbsentReason2", student=2, date="2014-09-09")
        resp = self.create_student_absent_reason(reason=3, description="TeStudentAbsentReason3", student=3, date="2013-09-09")
        resp = self.create_student_absent_reason(reason=3, description="TeStudentAbsentReason4", student=4, date="2014-09-09")

        self.assertEquals(resp.status_code, 201)

        url = reverse("list_dynamic_student_absent_reasons_statistics", kwargs={"type": "gender"})
        resp = self.auth_client.get(url)
        # print(resp.json())
        self.assertEquals(resp.status_code, 200)

        url = reverse("list_dynamic_student_absent_reasons_statistics", kwargs={"type": "id"})
        resp = self.auth_client.get(url)
        # print(resp.json())
        print(resp.json()["results"][0])
        self.assertEquals(resp.status_code, 200)

        url = reverse("list_dynamic_student_absent_reasons_statistics", kwargs={"type": "reason"})
        resp = self.auth_client.get(url)
        # print(resp.json()["results"][0])
        # print(resp.json())
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json()["count"], 3)

        url = reverse("list_dynamic_student_absent_reasons_statistics", kwargs={"type": "reason-description"})
        resp = self.auth_client.get(url)
        print(resp.json()["results"][0])
        # print(resp.json())
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.json()["count"], 4)

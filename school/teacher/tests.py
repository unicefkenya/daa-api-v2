from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse

from client.models import MyUser
from core.tests import BaseAPITest
from school.models import School


class TeacherTests(BaseAPITest):
    def test_creating_teacher(self):
        resp = self.create_teacher(first_name="TeTeacher", phone="986")
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

        self.set_authenticated_user(resp.data["user"])
        resp = self.auth_client.get(reverse("Retrieve_client"))
        self.assertEquals(resp.data["teacher"], 4)

    @tag("tdt")
    def test_deleting_teacher_with_creds(self):
        resp = self.create_teacher(first_name="TeTeacher", phone="986", school=2)
        print(resp.json())
        teacher_id = 3
        resp = self.auth_client.get(reverse("retrieve_update_destroy_teacher", kwargs={"pk": teacher_id}))
        # print(resp.json())
        user = resp.data["user"]
        self.assertEqual(MyUser.objects.filter(id=user).exists(), True)
        resp = self.auth_client.delete(reverse("retrieve_update_destroy_teacher", kwargs={"pk": teacher_id}))

        self.assertEqual(MyUser.objects.filter(id=user).exists(), False)

    def test_listing_teachers(self):
        self.set_authenticated_user(2)
        resp = self.create_teacher(first_name="Micha", phone="987")
        resp = self.create_teacher(first_name="Mash", phone="988")
        url = "{}?name=ma mich".format(reverse("list_create_teachers"))
        resp = self.auth_client.get(url)
        self.assertEqual(resp.data["count"], 1)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_retrieving_teacher(self):
        # Id 2 beacause id is automatically created on creating a teacher
        resp = self.auth_client.get(reverse("retrieve_update_destroy_teacher", kwargs={"pk": 3}))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["first_name"], "TheTeacher")

    def test_updating_teacher(self):
        resp = self.auth_client.patch(reverse("retrieve_update_destroy_teacher", kwargs={"pk": 1}), data={"first_name": "Hello"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["first_name"], "Hello")

    def test_confirm_teacher_on_school_creation(self):
        resp = self.auth_client.get(reverse("retrieve_update_destroy_teacher", kwargs={"pk": 1}))
        ##Confirm is admin and non-delete
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.data["is_school_admin"], True)
        self.assertEquals(resp.data["is_non_delete"], True)
        # print(resp.json())

    def test_retrieving_teacher_school_info(self):
        self.set_authenticated_user(3)
        resp = self.auth_client.get(reverse("user_teacher_school_info"))
        self.assertEquals(resp.status_code, 200)
        # print(resp.data["streams"])
        self.assertEquals("streams" in resp.data, True)
        self.assertEquals("teachers" in resp.data, True)
        # print(resp.json())

    def test_deleting_school_wwith_teacher(self):
        resp = self.auth_client.get(reverse("retrieve_update_destroy_teacher", kwargs={"pk": 1}))
        school = resp.data["school"]
        teach_id = resp.data["id"]
        user = resp.data["user"]
        self.assertEqual(MyUser.objects.filter(id=user).exists(), True)
        self.assertEqual(School.objects.filter(id=school).exists(), True)

        resp = self.client.get(reverse("retrieve_update_destroy_school", kwargs={"pk": school}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        resp = self.client.delete(reverse("retrieve_update_destroy_school", kwargs={"pk": school}))
        self.assertEquals(resp.status_code, status.HTTP_204_NO_CONTENT)

        resp = self.auth_client.get(reverse("retrieve_update_destroy_teacher", kwargs={"pk": 1}))
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(MyUser.objects.filter(id=user).exists(), False)
        self.assertEqual(School.objects.filter(id=school).exists(), False)

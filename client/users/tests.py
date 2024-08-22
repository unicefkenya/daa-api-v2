from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from client.models import MyUser, SCHOOL_ADMIN, SCHOOL_TEACHER, SUB_COUNTY_ADMIN, COUNTY_ADMIN
from core.tests import BaseAPITest


class SystemUsersCountyTests(BaseAPITest):
    admin_id = None

    def setUp(self):
        super(SystemUsersCountyTests, self).setUp()
        # self.create_county()
        self.admin_id = self.create_super_user_my()

    def create_super_user_my(self):
        return MyUser.objects.create_superuser("madmin112", "madmin1112@gmail.com", "m")

    def create_user(self, role="SCHA", county=1, sub_county=1, school=1, username="mad"):
        user = {"first_name": "Test", "gender": "M", "county": county, "sub_county": sub_county, "last_name": "Doe", "school": school, "username": username, "password": "m", "role": role}
        cl = APIClient()
        cl.force_authenticate(user=self.admin_id)
        return cl.post(reverse("list_create_system_users"), user)

    @tag("cul")
    def test_listing_system_users(self):
        # self.set_authenticated_user(2)
        resp = self.auth_client.get(reverse("list_create_system_users"))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    @tag("cu")
    def test_creating_systemc_user(self):
        resp = self.create_user(role=SCHOOL_ADMIN)
        print()

        print(resp.json())
        print()
        self.assertEqual(resp.status_code, 201)

        resp = self.create_user(role=SCHOOL_TEACHER, username="ad")
        # print(resp.json())
        self.assertEqual(resp.status_code, 201)

        resp = self.create_user(role=SUB_COUNTY_ADMIN, username="sub_county")
        # print(resp.json())
        self.assertEqual(resp.status_code, 201)

        resp = self.create_user(role=COUNTY_ADMIN, username="county")
        self.assertEqual(resp.status_code, 201)

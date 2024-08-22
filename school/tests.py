import os
from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.reverse import reverse

from core.tests import BaseAPITest
import sys
from unittest import skip, skipIf
from django.test import TestCase, tag
from django.conf import settings


class SchoolTests(BaseAPITest):
    def test_creating_school(self):
        resp = self.create_school(name="TeSchool", emis_code="3452")
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

    @tag("rsh")
    def test_retrieving_school(self):
        resp = self.client.get(reverse("retrieve_update_destroy_school", kwargs={"pk": 1}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        print(resp.json())
        self.assertEquals(resp.data["name"], "TheSchool")

    def test_updating_school(self):
        resp = self.client.patch(reverse("retrieve_update_destroy_school", kwargs={"pk": 1}), data={"name": "Hello"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["name"], "Hello")

    def create_custom_export(self, name="monthly", title="Hello Zanzibar", description="Okay there", start_date="", end_date=""):
        data = {"name": name, "title": title, "description": description}
        return self.auth_client.post(reverse("list_create_custom_exports"), data=data)

    @tag("tce")
    @skipIf("--tag=tce" not in sys.argv, "Skipping ")
    def test_creating_custom_export(self):
        resp = self.create_custom_export(name="overall")
        # print(resp.json())
        id = resp.json()["id"]

        resp = self.auth_client.get(reverse("retrieve_update_destroy_export", kwargs={"pk": id}))
        # print(resp.json())

    @skipIf("--tag=mai" not in sys.argv, "Skipping ")
    @tag("mai")
    def test_main_report(self):
        url = "{}?name=sch".format(reverse("test_pdf_export"))
        data = {"name": "test", "type": "pdf"}
        resp = self.auth_client.post(url, data=data)
        # print(resp.json())

    # def test_listing_school_districts(self):
    #     resp = self.auth_client.get(reverse("list_school_districts", kwargs={"pk": 1}))
    #     self.assertEquals(resp.data["count"],1)
    #     self.assertEquals(resp.status_code,200)

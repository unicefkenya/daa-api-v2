from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.reverse import reverse

from core.tests import BaseAPITest


class SupportQuestionTests(BaseAPITest):
    def test_creating_support_question(self):
        resp = self.create_support_question(title="TeSupportQuestion")
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

    def test_retrieving_support_question(self):
        resp = self.client.get(reverse("retrieve_update_destroy_support_question", kwargs={"pk": 1}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["title"], "TheSupportQuestion")

    def test_updating_support_question(self):
        resp = self.client.patch(reverse("retrieve_update_destroy_support_question", kwargs={"pk": 1}), data={"title": "Hello"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["title"], "Hello")

    # def test_listing_support_question_districts(self):
    #     resp = self.auth_client.get(reverse("list_support_question_districts", kwargs={"pk": 1}))
    #     self.assertEquals(resp.data["count"],1)
    #     self.assertEquals(resp.status_code,200)

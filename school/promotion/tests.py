from django.test import TestCase

# Create your tests here.
from rest_framework.reverse import reverse

from core.tests import BaseAPITest
from school.models import Stream, GraduatesStream
from school.promotion.models import PromoteSchool


class StudentTests(BaseAPITest):
    def test_creating_promotions(self):
        stream_promotions = [{"next_class": 2, "prev_class": 1}]
        data = {"stream_promotions": stream_promotions, "school": 1, "year": 1990}
        # Create the promotion
        resp = self.auth_client.post(reverse("list_create_promotions"), data=data, format="json")
        prev = Stream.objects.get(id=1).students.count()
        next = Stream.objects.get(id=2).students.count()
        self.assertEquals(prev == 4, True)
        self.assertEquals(next == 0, True)
        gstreams = GraduatesStream.objects.all().count()
        self.assertEquals(gstreams == 1, True)

        # Complete the promotions
        data = {"action": "complete"}
        resp = self.auth_client.post(reverse("retrieve_complete_undo_promotion", kwargs={"pk": 1}), data=data, format="json")
        prev = Stream.objects.get(id=1).students.count()
        next = Stream.objects.get(id=2).students.count()
        self.assertEquals(prev == 0, True)
        self.assertEquals(next == 4, True)

        # Complete the promotions
        data = {"action": "undo"}
        resp = self.auth_client.post(reverse("retrieve_complete_undo_promotion", kwargs={"pk": 1}), data=data, format="json")
        prev = Stream.objects.get(id=1).students.count()
        next = Stream.objects.get(id=2).students.count()
        self.assertEquals(PromoteSchool.objects.all().count() == 0, True)
        self.assertEquals(prev == 4, True)
        self.assertEquals(next == 0, True)

        gstreams = GraduatesStream.objects.all().count()
        self.assertEquals(gstreams == 0, True)
        # print(resp.json())

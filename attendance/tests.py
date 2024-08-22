import time
from django.test import TestCase, tag

# Create your tests here.
from rest_framework import status
from rest_framework.reverse import reverse

from attendance.models import Attendance, TeacherAttendance
from core.tests import BaseAPITest


class AttendanceTests(BaseAPITest):
    #

    def test_fetching_attendances(self):
        resp = self.auth_client.get(reverse("list_create_attendances"))
        self.assertEquals(resp.status_code, 200)
        # print(resp.json())

    @tag("lft")
    def test_filter_attendances(self):
        url = reverse("list_dynamic_attendances_statistics", kwargs={"type": "id"})
        resp = self.auth_client.get(f"{url}?no_special_needs=false")
        # print(resp.json()["count"])
        self.assertGreater(resp.json()["count"], 0)

        resp = self.auth_client.get(f"{url}?no_special_needs=true")
        # print(f"{url}?has_special_needs=false")
        self.assertEquals(resp.json()["count"], 0)

        resp = self.auth_client.get(f"{url}?special_needs=1")
        # print(resp.json())
        self.assertEquals(resp.json()["count"], 2)

        resp = self.auth_client.get(f"{url}?special_needs=2")

        # print(resp.json())
        self.assertEquals(resp.json()["count"], 1)

        resp = self.auth_client.get(f"{url}?special_needs=2")
        self.assertEquals(resp.json()["cache"], True)

        # print(resp.json())
        self.assertEquals(resp.json()["count"], 1)
        self.assertEquals(resp.json()["cache"], True)
        self.assertEquals("cache" in resp.json(), True)

        resp = self.auth_client.get(f"{url}?special_needs=2")
        # print(resp.json())
        self.assertEquals(resp.json()["count"], 1)
        self.assertEquals(resp.json()["cache"], True)
        time.sleep(2)
        resp = self.auth_client.get(f"{url}?special_needs=2")
        self.assertEquals("cache" in resp.json(), True)
        self.assertEquals(resp.json()["count"], 1)

        resp = self.auth_client.get(f"{url}?special_needs=2")
        # print(resp.json())
        self.assertEquals(resp.json()["count"], 1)
        self.assertEquals(resp.json()["cache"], True)

        resp = self.auth_client.get(f"{url}?special_needs=2&ignore_cache=true")
        # print(resp.json())
        self.assertEquals(resp.json()["count"], 1)
        self.assertEquals(resp.json().get("cache"), None)

        resp = self.auth_client.get(f"{url}?special_needs=2&ignore_cache=true")
        # print(resp.json())
        self.assertEquals(resp.json()["count"], 1)
        self.assertEquals(resp.json().get("cache"), None)

        resp = self.auth_client.get(f"{url}?special_needs=2&ignore_cache=false")
        # print(resp.json())
        self.assertEquals(resp.json()["count"], 1)
        self.assertEquals(resp.json().get("cache"), None)

        resp = self.auth_client.get(f"{url}?special_needs=2&ignore_cache=false")
        # print(resp.json())
        self.assertEquals(resp.json()["count"], 1)
        self.assertEquals(resp.json().get("cache"), True)
        self.assertEquals(resp.json().get("cache_timeout"), 60)

    @tag("lft1")
    def test_cache_timeout(self):
        url = reverse("list_dynamic_attendances_statistics", kwargs={"type": "id"})
        resp = self.auth_client.get(f"{url}?special_needs=1&cache_timeout=59")
        # print(resp.json())
        self.assertEquals(resp.json()["count"], 2)
        self.assertEquals(resp.json().get("cache"), None)

        resp = self.auth_client.get(f"{url}?special_needs=1&cache_timeout=59")
        self.assertEquals(resp.json()["count"], 2)
        self.assertEquals(resp.json().get("cache"), True)
        self.assertEquals(resp.json().get("cache_timeout"), 59)

    @tag("takeAtt")
    def test_creating_attendance(self):
        resp = self.take_attendance(date="2019-09-05")
        resp = self.take_attendance(date="2019-09-05")
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

    @tag("takeT")
    def test_creating_teacher_attendance(self):
        resp = self.take_attendance(date="2019-09-05", present=[1], absent=[], stream="teachers")
        self.assertEquals(resp.status_code, 201)
        attendance = TeacherAttendance.objects.values("teacher_id", "status")
        self.assertEquals(len(attendance), 1)
        self.assertEquals(attendance[0]["status"], 1)

        resp = self.take_attendance(date="2019-09-05", present=[], absent=[1], stream="teachers")
        print(resp.json())
        self.assertEquals(resp.status_code, 201)
        attendance = TeacherAttendance.objects.values("teacher_id", "status")
        self.assertEquals(len(attendance), 1)
        self.assertEquals(attendance[0]["status"], 0)

    def test_retrieving_attendance(self):
        resp = self.client.get(reverse("retrieve_update_destroy_attendance", kwargs={"pk": "201909091"}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["id"], "201909091")

    def test_updating_attendance(self):
        resp = self.client.patch(
            reverse("retrieve_update_destroy_attendance", kwargs={"pk": "201909091"}),
            data={"date": "2019-07-01T12:0:00"},
        )
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["date"], "2019-07-01T12:00:00+03:00")

    @tag("stats")
    def test_attendance_dynamic_stats_only_field_fetching_list(self):
        url = reverse("list_dynamic_attendances_statistics", kwargs={"type": "class"})
        urlid = reverse("list_dynamic_attendances_statistics", kwargs={"type": "id"})
        query_param = "only_and_filter_field=absent_males&order=ASC"
        resp = self.auth_client.get(f"{url}?{query_param}")
        self.assertEquals(resp.json()["count"], 1)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

        resp = self.auth_client.get(f"{urlid}?{query_param}")
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.json()["count"], 1)

    @tag("stats")
    def test_attendance_dynamic_stats_only_field_wrong_field(self):
        url = reverse("list_dynamic_attendances_statistics", kwargs={"type": "day"})
        resp = self.auth_client.get(f"{url}?only_and_filter_field=present_maleas&only_and_filter_field=present_femaleas&order=ASC")
        print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.json()["count"], 1)
        resp_obj = {
            "value": "2019-09-09",
            "day": "2019-09-09",
            "present_males": 1,
            "absent_males": 1,
            "present_females": 0,
            "absent_females": 0,
            "total_attendances_taken": 2,
        }
        self.assertDictEqual(resp.json()["results"][0], resp_obj)

    @tag("stats1")
    def test_attendance_dynamic_stats_only_field(self):
        url = reverse("list_dynamic_attendances_statistics", kwargs={"type": "day"})
        resp = self.auth_client.get(f"{url}?only_and_filter_field=present_males&only_and_filter_field=present_females&order=ASC")
        print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        resp_obj = {
            "value": "2019-09-09",
            "day": "2019-09-09",
            "present_males": 1,
            "present_females": 0,
        }
        self.assertDictEqual(resp.json()["results"][0], resp_obj)

    # @tag("stats")
    def test_attendance_dynamic_stats_only_and_filter_field(self):
        url = reverse("list_dynamic_attendances_statistics", kwargs={"type": "student"})
        resp = self.auth_client.get(f"{url}")
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        # print(resp.json())
        self.assertEquals(resp.json()["count"], 2)
        # print(resp.json()["results"][0])
        self.assertTrue("present_count" in resp.json()["results"][0])

        resp = self.auth_client.get(f"{url}?only_and_filter_field=absent_count&date=2019-09-09")
        # print(resp.json())
        self.assertEquals(resp.json()["count"], 1)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertFalse("present_count" in resp.json()["results"][0])

    def test_listing_statistics(self):
        self.take_attendance(date="2019-09-06")
        self.take_attendance(date="2019-09-07")
        #
        self.create_school(name="school_2", emis_code="45")
        resp = self.create_stream(base_class="3", school=2)
        stream_id = resp.data["id"]
        resp = self.create_student(
            first_name="micha",
            stream=stream_id,
        )
        student_id = resp.data[0]["id"]
        resp = self.take_attendance_for_student(student=student_id, stream=stream_id)
        url = reverse("list_dynamic_attendances_statistics", kwargs={"type": "id"})
        resp = self.auth_client.get(url)
        # print(url)
        # print(resp.json()["results"][0])
        resp = self.auth_client.get(reverse("list_dynamic_attendances_statistics", kwargs={"type": "student"}))
        print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

        resp = self.auth_client.get(reverse("list_dynamic_attendances_statistics", kwargs={"type": "gender"}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(reverse("list_create_attendance_statistics", kwargs={"type": "yearly"}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(reverse("list_create_attendance_statistics", kwargs={"type": "stream"}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(reverse("list_create_attendance_statistics", kwargs={"type": "class"}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(reverse("list_create_attendance_statistics", kwargs={"type": "gender"}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        resp = self.client.get(reverse("list_create_attendance_statistics", kwargs={"type": "monthly"}))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(reverse("list_create_attendance_statistics", kwargs={"type": "school"}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

        resp = self.client.get(reverse("list_create_attendance_statistics", kwargs={"type": "village"}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        # print(resp.json())
        #
        resp = self.client.get(reverse("list_create_attendance_statistics", kwargs={"type": "school"}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        # print(resp.json())

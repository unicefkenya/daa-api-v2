from django.test import tag
from rest_framework import status
from rest_framework.reverse import reverse

from client.models import MyUser
from core.tests import BaseAPITest
from school.models import Student, Stream


class StudentTests(BaseAPITest):
    @tag("createStud")
    def test_creating_student(self):
        stream_id = 1
        resp = self.create_student(first_name="TeStudent", last_name="1", stream=stream_id)
        # print(resp.data[0]["school_name"])
        # print(resp.json())
        student_id = resp.json()[0]["id"]
        # print(student_id)
        # print(ser.data)
        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)

        resp = self.auth_client.get("{}".format(reverse("list_create_students")))

        self.assertEquals(resp.data["count"], 8)
        # print("All....", resp.data["count"])
        # for stud in resp.data["results"]:
        #     print(stud["first_name"],stud["middle_name"],stud["last_name"])
        #
        # print(resp.json()["results"])
        resp = self.auth_client.get("{}?name=mi ke".format(reverse("list_create_students")))
        self.assertEquals(resp.data["count"], 2)
        # print("FILTERED....", resp.data["count"])
        # for stud in resp.data["results"]:
        #     print(stud)
        #
        # for stud in resp.data["results"]:
        #     print(stud["first_name"], stud["middle_name"], stud["last_name"])
        school_emis_code = Stream.objects.get(id=stream_id).school.emis_code
        user = MyUser.objects.get(username=school_emis_code)
        self.set_authenticated_user(user.id)
        resp = self.auth_client.get(reverse("user_teacher_school_info"))
        student = resp.json()["streams"][0]["students"][0]
        fields = ["county_name", "sub_county_name", "guardian_county_name", "guardian_status_display"]
        # for field in student:
        #   print(field,student[field])
        for field in fields:
            # print(student[field])
            self.assertTrue(field in student)

        # print(student)

    def test_listing_absent_students(self):
        resp = self.create_student_absent_reason(description="TeStudentAbsentReason", student=2, date="2019-09-09")
        # print(resp.json())
        url = "{}?page_size=10&date=2019-09-09".format(reverse("list_absent_students"))
        # print(url)
        resp = self.auth_client.get(url)
        # print(resp.json())
        self.assertEquals(resp.status_code, 200)
        # print(resp.json())

    @tag("lstds")
    def test_listing_students(self):
        self.set_authenticated_user(2)
        resp = self.auth_client.get(reverse("list_create_students"))
        # print(resp.json())
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_retrieving_student(self):
        # Id 2 beacause id is automatically created on creating a student
        resp = self.auth_client.get(reverse("retrieve_update_destroy_student", kwargs={"pk": 1}))
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["first_name"], "TheStudent")

    def test_updating_student(self):
        resp = self.auth_client.patch(reverse("retrieve_update_destroy_student", kwargs={"pk": 1}), data={"first_name": "Hello"})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data["first_name"], "Hello")

    def test_deleting_student(self):
        self.create_delete_reason(name="error")
        resp = self.auth_client.delete("{}?reason=1&description=Nothing happens".format(reverse("retrieve_update_destroy_student", kwargs={"pk": 1})))
        # print(resp.data)
        self.assertEquals(resp.status_code, 204)

        resp = self.auth_client.get(reverse("list_dropout_students"))
        self.assertEquals(resp.data["count"], 1)
        # print(resp.json())

    @tag("tsn")
    def test_filtering_special_need(self):
        url=reverse("list_create_students")
        resp = self.auth_client.get(f"{url}?no_special_needs=true")
        # print(resp.json()["count"])
        self.assertEquals(resp.json()["count"],0)
        
        resp = self.auth_client.get(f"{url}?no_special_needs=false")
        self.assertEquals(resp.json()["count"],9)
        

    def test_creating_bulk_students(self):
        first_name = "TheStudent"
        stream = 1
        date_enrolled = "2019-06-06"
        date_of_birth = "2017-06-06"
        last_name = "lastName"
        st1 = {"active": True, "special_needs": [1, 2], "date_of_birth": date_of_birth, "first_name": first_name, "stream": stream, "date_enrolled": date_enrolled, "last_name": last_name}
        data = [st1, st1]
        resp = self.auth_client.post(reverse("list_create_bulk_students"), data=data, format="json")
        # print(resp.json())
        self.assertEquals(resp.status_code, 201)

    @tag("ste")
    def test_students_enrollment_duplicate(self):
        self.test_creating_bulk_students()
        url = reverse("list_students_enrollments", kwargs={"type": "duplicate"})
        resp = self.auth_client.get(f"{url}?is_training_school=false&export=false")
        print(resp.json())
        self.assertEquals(resp.status_code, 200)

        resp = self.auth_client.get(f"{url}?is_training_school=false&export=true")
        print(resp.json())
        self.assertEquals(resp.status_code, 201)

    @tag("st")
    def test_students_enrollments(self):
        url = reverse("list_students_enrollments", kwargs={"type": "year"})
        resp = self.auth_client.get(f"{url}?is_training_school=false&export=true")

        # print(resp.json()["results"][0])
        resp = self.auth_client.get(reverse("list_students_enrollments", kwargs={"type": "class"}))
        # print(resp.json())
        self.assertEquals(resp.status_code, 200)
        resp = self.auth_client.get(reverse("list_students_enrollments", kwargs={"type": "month"}))
        self.assertEquals(resp.status_code, 200)

        resp = self.auth_client.get(reverse("list_students_enrollments", kwargs={"type": "year"}))
        self.assertEquals(resp.status_code, 200)

        resp = self.auth_client.get(reverse("list_students_enrollments", kwargs={"type": "school"}))
        self.assertEquals(resp.status_code, 200)

        resp = self.auth_client.get(reverse("list_students_enrollments", kwargs={"type": "gender"}))
        self.assertEquals(resp.status_code, 200)
        #
        #         resp = self.auth_client.get(reverse("list_students_enrollments", kwargs={"type": "village"}))
        #         # print(resp.json())
        # self.assertEquals(resp.status_code, 200)

        resp = self.auth_client.get(reverse("list_students_enrollments", kwargs={"type": "school"}))
        # print(resp.json())
        self.assertEquals(resp.status_code, 200)

        # print(resp.json())

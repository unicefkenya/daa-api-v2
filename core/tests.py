from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from attendance.models import Attendance
from client.models import MyUser
from school.models import Student


class BaseAPITest(APITestCase):
    username = "michameiu@gmail.com"
    password = "micha"
    client_id = "iuyutyutuyctua"
    client_secret = "lahkckagkegigciegvjegvjhv"
    speaker = None

    def setUp(self):
        user = MyUser.objects.create(username=self.username)
        self.client = APIClient()
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=user)
        self.user = user
        self.user.set_password(self.password)
        self.user.save()

        ####Create a hospital staff Staff Amdin #user id 2
        resp = self.create_user()
        # print(resp.json())
        resp = self.assertEqual(resp.status_code, 401)
        # print(resp.json())

        
        resp = self.create_county()
        resp = self.create_sub_county()

  

        resp = self.create_special_need()
        resp = self.create_special_need(name="Health")

        resp = self.create_school()
        resp = self.create_school(name="SCh2", emis_code="PADD")

        resp = self.create_teacher()
        resp = self.create_stream()
        resp = self.create_stream(name="North", base_class="8")
        stresp = self.create_stream(name="North", base_class="5", school=2)
        # print(resp.json())
        resp = self.create_student()
        resp = self.create_student(first_name="Miah", stream=3)
        # print(resp.json())
        resp = self.create_delete_reason()
        resp = self.take_attendance()
        resp = self.create_support_question()
        resp = self.create_absent_reason()
        resp = self.create_student_absent_reason()
        # print(resp.json())

    def create_sub_county(self, county="1", name="madC"):
        data = {"county": county, "name": name}
        return self.auth_client.post(reverse("list_create_sub_countys"), data=data)

    def create_special_need(self, name="madC"):
        data = {"name": name}
        return self.auth_client.post(reverse("list_create_special_needs"), data=data)

    def create_county(self, name="madC"):
        data = {"name": name}
        return self.auth_client.post(reverse("list_create_countys"), data=data)


    def create_user(self):
        self.set_authenticated_user(1)
        user = {"first_name": "Test", "school": "1", "last_name": "Doe", "username": "mfa", "password": "m", "role": "SCHT"}
        return self.client.post(reverse("list_create_system_users"), user)

    def set_authenticated_user(self, user_id=2):
        self.auth_client.force_authenticate(user=MyUser.objects.get(id=user_id))

    def create_school(self, name="TheSchool", emis_code="345", sub_county=1):
        data = {"name": name, "emis_code": emis_code, "village": 1, "sub_county": sub_county}
        return self.auth_client.post(reverse("list_create_schools"), data=data)

    def create_teacher(self, first_name="TheTeacher", last_name="Micha", phone="675", school=1):
        data = {"first_name": first_name, "phone": phone, "school": school, "last_name": last_name}
        return self.auth_client.post(reverse("list_create_teachers"), data=data)

    def create_stream(self, name="TheStream", base_class="7", school=1):
        data = {"school": school, "name": name, "base_class": base_class}
        return self.auth_client.post(reverse("list_create_streams"), data=data)

    def create_student(
        self,
        first_name="TheStudent",
        stream=1,
        moe_extra_info={"district_id": 10, "state_id": 11, "region_id": 12, "blood_group_id": 13, "section_id": 14},
        date_enrolled="2019-06-06",
        date_of_birth="2017-06-06",
        admission_no=123,
        guardina_name="Micha",
        guardian_phone="072267537",
        last_name="lastName",
    ):
        std1 = {
            "active": True,
            "special_needs": [1, 2],
            "moe_extra_info": moe_extra_info,
            "first_name": first_name,
            "admission_no": admission_no,
            "stream": stream,
            "date_enrolled": date_enrolled,
            "last_name": last_name,
            "guardian_name": guardina_name,
            "guardian_phone": guardian_phone,
            "date_of_birth": date_of_birth,
        }
        std2 = {"active": True, "special_needs": [1], "moe_extra_info": moe_extra_info, "first_name": first_name, "stream": stream, "date_enrolled": date_enrolled, "last_name": last_name}
        data = [std1, std2]
        return self.auth_client.post(reverse("list_create_bulk_students"), data=data, format="json")

    def take_attendance_for_student(self, date="2019-09-20", stream=1, student=1):
        dat = {"date": date, "present": [student], "absent": [], "stream": stream}
        data = [dat]
        return self.auth_client.post(reverse("list_create_attendances"), data=data, format="json")

    def take_attendance(self, date="2019-09-09", present=[1], absent=[2], stream=1):
        # print(Student.objects.get(id=1))
        self.create_student(first_name="micgha", last_name="kelvin")
        dat = {"date": date, "present": present, "absent": absent, "stream": stream}
        data = [dat]
        return self.auth_client.post(reverse("list_create_attendances"), data=data, format="json")

    def create_delete_reason(self, name="TheDeleteReason"):
        data = {"name": name, "description": "{} Descrip".format(name)}
        return self.auth_client.post(reverse("list_create_delete_reasons"), data=data)

    def create_support_question(self, title="TheSupportQuestion"):
        data = {"title": title, "description": "Go to hell"}
        return self.auth_client.post(reverse("list_create_support_questions"), data=data)

    def create_absent_reason(self, name="TheAbsentReason"):
        data = {"name": name, "description": f"{name} DescAbsent"}
        return self.auth_client.post(reverse("list_create_absent_reasons"), data=data)

    def create_student_absent_reason(self, description="TheStudentAbsentReason", reason=1, student=1, date="2019-05-09"):
        data = {"student": student, "reason": reason, "description": description, "date": date}
        url = reverse("list_create_student_absent_reasons")
        return self.auth_client.post(url, data=data)

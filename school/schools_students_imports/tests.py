from os import path

import openpyxl
from django.test import tag
from openpyxl import Workbook
from rest_framework import status
from rest_framework.reverse import reverse
from core.tests import BaseAPITest
from school.models import SchoolsStudentsImport, Student
from wvapi.settings import STATIC_ROOT
from django.contrib.staticfiles import finders


def create_an_empty_workbook(rows_count):
    # headers=["school","school nemis code","county","subcounty","first name","last name","gender","class","special_needs",
    #          "status","guardian name","guardian county","guardian subcounty","guardian email","date_enrolled"]
    pass


class SchoolsStudentsImportTests(BaseAPITest):
    def create_schools_students_import(
        self,
        user="1",
        step="Q",
        rows_count="1",
        nemis_group_id=None,
        nemis_institution_level=None,
        raw_data=None,
        imported_rows_count="1",
        name="madC",
        import_type="F",
        file_name="test_excel.xlsx",
        should_import=True,
    ):
        if import_type == "F":
            filePath = finders.find(file_name)
            with open(filePath, "rb") as import_file:
                data = {"user": user, "step": step, "rows_count": rows_count, "imported_rows_count": imported_rows_count, "name": name, "import_file": import_file, "should_import": should_import}
                return self.auth_client.post(reverse("list_create_schools_students_imports"), data=data, format="multipart")
        else:
            data = {
                "user": user,
                "step": step,
                "import_type": import_type,
                "rows_count": rows_count,
                "imported_rows_count": imported_rows_count,
                "name": name,
                "should_import": should_import,
            }
            if nemis_group_id:
                data["nemis_group_id"] = nemis_group_id

            if raw_data:
                data["raw_data"] = raw_data

            if nemis_institution_level:
                data["nemis_institution_level"] = nemis_institution_level
            return self.auth_client.post(reverse("list_create_schools_students_imports"), data=data, format="json")

    def setUp(self):
        super(SchoolsStudentsImportTests, self).setUp()
        print(Student.objects.all().count())
        # resp = self.create_schools_students_import()

    @tag("tn")
    def test_creating_schools_with_nemis(self):
        raw_data = [
            {
                "Institution_Code": "23NQ",
                "Institution_Name": "KATERIT PRIMTRY",
                "County_Name": "Baringo",
                "County_Code": "130",
                "Sub_County_Name": "MOGOTIO",
                "Sub_County_Code": "1006",
                "Institution_Level_Code": "2",
                "Institution_Type": "Public",
                "UPI": "SRY5BB",
                "Surname": "RUTO",
                "FirstName": "FAITH",
                "OtherNames": "JEROP",
                "DOB": "2018-03-29",
                "Gender": "F",
                "Birth_Cert_No": "0421709077",
                "Country_Name": "Kenya",
                "Class_Name": "Class 8   ",
                "Special_Medical_Condition": "0",
                "Father_Name": "JAMES KIPRUTO KIMUGE",
                "Father_IDNo": "23471975",
                "Father_Contacts": "0716115320",
                "Father_Email": "",
                "Mother_Name": "AGNES JEPKOGEI KOECH",
                "Mother_IDNo": "25312617",
                "Mother_Contacts": "0700576678",
                "Mother_Email": "",
                "Date_Captured": "2018-03-29",
                "Guardian_Name": "",
                "Guardian_IDNo": "",
                "Guardian_Contacts": "",
                "Guardian_Email": "",
                "Status": None,
                "Photo": None,
            }
        ]
        resp = self.create_schools_students_import(raw_data=raw_data, import_type="JS")
        # print("The response is ")
        # print(resp.json())

    @tag("trf")
    def test_excel_with_references(self):
        file_name = "test_references.xlsx"
        resp = self.create_schools_students_import(file_name=file_name)
        print(resp.json())

    @tag("tec")
    def test_excel_with_empty_cells(self):
        file_name = "empty_rows.xlsx"
        resp = self.create_schools_students_import(file_name=file_name)
        print(resp.json())

    @tag("tndne")
    def test_no_date_of_birth_no_enroll(self):
        file_name = "test_no_birth_no_enroll.xlsx"
        # file_name = "test_excel.xlsx"
        before_stud_count = Student.objects.all().count()

        resp = self.create_schools_students_import(file_name=file_name)

        stud_count = Student.objects.all().count()
        # print(f"from {before_stud_count} to {stud_count}")
        self.assertEquals(stud_count, before_stud_count + 7)
        # print(resp.json())

    @tag("tndne2")
    def test_no_date_of_birth_no_enroll_2(self):
        file_name = "test_no_birth_no_enroll_2.xlsx"
        # file_name = "test_excel.xlsx"
        before_stud_count = Student.objects.all().count()

        resp = self.create_schools_students_import(file_name=file_name)
        stud_count = Student.objects.all().count()
        # print(f"from {before_stud_count} to {stud_count}")
        self.assertEquals(stud_count, before_stud_count + 7)

    @tag("tndne3")
    def test_wrong_date_of_birth_wrong_enroll(self):
        file_name = "test_data_wrong_date_format.xlsx"
        # file_name = "test_excel.xlsx"
        before_stud_count = Student.objects.all().count()

        resp = self.create_schools_students_import(file_name=file_name)
        stud_count = Student.objects.all().count()
        print(f"from {before_stud_count} to {stud_count}")
        # self.assertEquals(stud_count, before_stud_count + 8)
        self.assertEquals(stud_count, before_stud_count + 20)

    # @tag("tn")
    def test_creating_schools_with_nemis_county_url(self):
        return
        # 1087
        resp = self.create_schools_students_import(nemis_group_id=123, nemis_institution_level=2, import_type="NMC")
        print("The response is ")
        id = resp.json()["id"]
        print(resp.json())

    @tag("tn")
    def test_creating_schools_with_nemis_url(self):
        return
        # 1087
        resp = self.create_schools_students_import(nemis_group_id=1291, nemis_institution_level=2, import_type="NMSC")
        print("The response is ")
        import_id = resp.json()["id"]
        import_task = SchoolsStudentsImport.objects.get(id=import_id)
        print(import_task.name)
        print(resp.json())

    # @tag("tn")
    def test_creating_schools_with_nemis_url_many(self):
        return
        # resp = self.create_schools_students_import(nemis_group_id=1087, nemis_institution_level=2, import_type="NMSC")
        print("The response is ")
        print(resp.json())

    @tag("cic")
    def test_creating_schools_students_import(self):
        resp = self.create_schools_students_import(name="madC", should_import=False)
        # print(resp.json())
        resp = self.create_schools_students_import(
            name="madC",
        )

        resp = self.create_schools_students_import(name="madC", file_name="main_sample.xlsx")

        id = resp.json()["id"]

        # print(resp.json())

        resp = self.auth_client.get(reverse("retrieve_update_destroy_schools_students_import", kwargs={"pk": id}))

        print(resp.json())
        resp = self.auth_client.get(reverse("list_create_schools_students_imports"))
        # print(resp.json())
        # for data in resp.json()["results"]:
        #     # print(data)
        #     print("")
        #     pass
        # self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        print(Student.objects.all().count())
        self.assertLessEqual(Student.objects.all().count(), 46)

    def test_listing_schools_students_import(self):
        resp = self.auth_client.get(reverse("list_create_schools_students_imports"))
        # print(resp.json())
        # self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_retrieving_schools_students_import(self):
        resp = self.auth_client.get(reverse("retrieve_update_destroy_schools_students_import", kwargs={"pk": 1}))
        # print(resp.json())
        # self.assertEquals(resp.status_code, status.HTTP_200_OK)
        # self.assertEquals(resp.data["name"], None)

    def test_updating_schools_students_import(self):
        resp = self.auth_client.patch(reverse("retrieve_update_destroy_schools_students_import", kwargs={"pk": 1}), data={"name": "madC"})
        # self.assertEquals(resp.status_code, status.HTTP_200_OK)
        # self.assertEquals(resp.data["name"], "madC")

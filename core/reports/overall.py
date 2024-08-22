from asyncio import constants
from urllib import response
from stats.models import Export
from reports.utils import BaseCustomReport
from rest_framework import serializers
from django.utils import timezone
from stats.exports.serializers import CustomExportSerializer
from django.utils import timezone
from stats.utils import get_grouped_by_data, my_order_by, get_formatted_filter_set, get_model_stats_definitions

from core.reports.get_data import get_any_stats
from datetime import datetime


class OverAllReportSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(default="Sample Title")
    subtitle = serializers.ReadOnlyField(default="Sample Subtlte")
    generated_on = serializers.ReadOnlyField(default=timezone.now())
    start_date = serializers.ReadOnlyField(required=False)
    end_date = serializers.ReadOnlyField(
        required=False,
    )
    
    overall_stats = serializers.SerializerMethodField(method_name="get_overall_stats")
    all_enrollment = serializers.SerializerMethodField(method_name="get_all_enrollment")
    all_attendances = serializers.SerializerMethodField(method_name="get_all_attendances")

    counties_enrollment = serializers.SerializerMethodField(method_name="get_counties_enrollment")
    top_county_enrollment = serializers.ReadOnlyField(default=None)
    top_county_top_school_enrollment = serializers.ReadOnlyField(default=None)
    top_county_total_schools_enrollment = serializers.ReadOnlyField(default=None)
    total_counties_enrollment = serializers.ReadOnlyField(default=None)

    sub_counties_enrollment = serializers.SerializerMethodField(method_name="get_sub_counties_enrollment")
    top_sub_county_enrollment = serializers.ReadOnlyField(default=None)
    total_sub_counties_enrollment = serializers.ReadOnlyField(default=None)

    schools_enrollment = serializers.SerializerMethodField(method_name="get_schools_enrollment")
    top_school_enrollment = serializers.ReadOnlyField(default=None)
    total_schools_enrollment = serializers.ReadOnlyField(default=None)

    status_enrollment = serializers.SerializerMethodField(method_name="get_status_enrollment")
    oosc_enrollment = serializers.ReadOnlyField(default=None)
    new_enrollment = serializers.ReadOnlyField(default=None)

    counties_attendances = serializers.SerializerMethodField(method_name="get_counties_attendances")
    top_county_attendance = serializers.ReadOnlyField(default=None)
    top_county_top_school_attendance = serializers.ReadOnlyField(default=None)
    top_county_total_schools_attendance = serializers.ReadOnlyField(default=None)

    total_counties_attendance = serializers.ReadOnlyField(default=None)

    sub_counties_attendances = serializers.SerializerMethodField(method_name="get_sub_counties_attendances")
    top_sub_county_attendance = serializers.ReadOnlyField(default=None)
    total_sub_counties_attendance = serializers.ReadOnlyField(default=None)

    schools_attendances = serializers.SerializerMethodField(method_name="get_schools_attendances")
    top_school_attendance = serializers.ReadOnlyField(default=None)
    total_schools_attendance = serializers.ReadOnlyField(default=None)

    cache_data = {}

    class Meta:
        model = Export
        fields = "__all__"

    def get_query_parms(self, obj):
        query_params = {}

        if obj.start_date:
            query_params["start_date"] = obj.start_date.strftime("%Y-%m-%d")

        if obj.end_date:
            query_params["end_date"] = obj.end_date.strftime("%Y-%m-%d")

        query_params["page_size"] = obj.list_size if obj.list_size else 100
        return query_params

    def to_representation(self, instance):
        data = super(OverAllReportSerializer, self).to_representation(instance)
        data["top_county_enrollment"] = self.context.get("top_county_enrollment")
        data["total_counties_enrollment"] = self.context.get("total_counties_enrollment")
        data["top_school_enrollment"] = self.context.get("top_school_enrollment")
        data["total_schools_enrollment"] = self.context.get("total_schools_enrollment")
        data["top_sub_county_enrollment"] = self.context.get("top_sub_county_enrollment")
        data["total_sub_counties_enrollment"] = self.context.get("total_sub_counties_enrollment")

        data["top_county_attendance"] = self.context.get("top_county_attendance")
        data["total_counties_attendance"] = self.context.get("total_counties_attendance")
        data["top_sub_county_attendance"] = self.context.get("top_sub_county_attendance")
        data["total_sub_counties_attendance"] = self.context.get("total_sub_counties_attendance")
        data["top_school_attendance"] = self.context.get("top_school_attendance")
        data["total_schools_attendance"] = self.context.get("total_schools_attendance")
        data["oosc_enrollment"] = self.context.get("oosc_enrollment")
        data["new_enrollment"] = self.context.get("new_enrollment")
        data["top_county_top_school_attendance"] = self.context.get("top_county_top_school_attendance")
        data["top_county_top_school_enrollment"] = self.context.get("top_county_top_school_enrollment")
        data["top_county_total_schools_enrollment"] = self.context.get("top_county_total_schools_enrollment")
        data["top_county_total_schools_attendance"] = self.context.get("top_county_total_schools_attendance")
        data["generated_on"] = timezone.now()
        return data

    def get_all_enrollment(self, instance):
        response = get_any_stats("all_students", grouping="", user=self.instance.user, query_params=self.get_query_parms(instance))
        # print(response)
        return response

    def get_all_attendances(self, instance):
        response = get_any_stats("all_attendances", grouping="", user=self.instance.user, query_params=self.get_query_parms(instance))
        # print("n\n\n\n\nGOt it all ")
        # print(response)
        if response:
            total_males = response["present_males"] + response["absent_males"]
            total_females = response["present_females"] + response["absent_females"]
            response["total_males_att"] = total_males
            response["total_females_att"] = total_females

            response["females_percentage"] = 0 if total_females < 1 else response["present_females"] * 100.0 / total_females
            response["males_percentage"] = 0 if total_males < 1 else response["present_males"] * 100.0 / total_males
        return response

    def get_overall_stats(self, instance):
        response = get_any_stats("all", grouping="", user=self.instance.user, query_params={})
        # print(response)
        return response

    def get_status_enrollment(self, obj):
        res = get_any_stats("students", grouping="student-status", user=self.instance.user, query_params=self.get_query_parms(obj))
        # print(res)
        count = res["count"]
        response = res["results"]
        # oosc_enrollment
        oosc_enrollment = {"males": 0, "females": 0, "total_students": 0}
        new_enrollment = {"males": 0, "females": 0, "total_students": 0}

        if count > 0:
            # oosc_enrollment
            for item in response:
                if item["value"] == "OOSC":
                    oosc_enrollment = item
                elif item["value"] == "NE":
                    new_enrollment = item

        self.context["oosc_enrollment"] = oosc_enrollment
        self.context["new_enrollment"] = new_enrollment

        return response

    def get_counties_attendances(self, obj):
        # print(self.instance.user)
        res = get_any_stats("attendances", grouping="county", user=self.instance.user, query_params=self.get_query_parms(obj))
        count = res["count"]
        response = res["results"]

        self.context["total_counties_attendance"] = self.get_value_count(response)

        if count > 0:
            county_one = response[0]
            self.context["top_county_attendance"] = county_one
            county_id = county_one["value"]
            try:
                params = self.get_query_parms(obj)
                params["school_county"] = county_id
                res1 = get_any_stats("attendances", grouping="school", user=self.instance.user, query_params=params)
                coun = res1["count"]
                resp = res1["results"]

                self.context["top_county_total_schools_attendance"] = coun
                if coun > 0:
                    school_one_county = resp[0]
                    self.context["top_county_top_school_attendance"] = school_one_county

            except Exception as e:
                print(e)

        return response

    def get_sub_counties_attendances(self, obj):
        # print(self.instance.user)
        res = get_any_stats("attendances", grouping="sub-county", user=self.instance.user, query_params=self.get_query_parms(obj))
        count = res["count"]
        response = res["results"]

        self.context["total_sub_counties_attendance"] = self.get_value_count(response)

        if count > 0:
            sub_county_one = response[0]
            self.context["top_sub_county_attendance"] = sub_county_one
        return response

    def get_schools_attendances(self, obj):
        # print(self.instance.user)
        res = get_any_stats("attendances", grouping="school", user=self.instance.user, query_params=self.get_query_parms(obj))
        count = res["count"]
        self.context["total_schools_attendance"] = count
        response = res["results"]

        if count > 0:
            school_one = response[0]
            self.context["top_school_attendance"] = school_one
        return response

    def get_counties_enrollment(self, obj):
        # print(self.instance.user)
        res = get_any_stats("students", grouping="county", user=self.instance.user, query_params=self.get_query_parms(obj))
        count = res["count"]
        response = res["results"]

        self.context["total_counties_enrollment"] = self.get_value_count(response)

        if count > 0:
            county_one = response[0]
            self.context["top_county_enrollment"] = county_one
            county_id = county_one["value"]
            try:
                params = self.get_query_parms(obj)
                params["school_county"] = county_id
                res1 = get_any_stats("students", grouping="school", user=self.instance.user, query_params=params)
                coun = res1["count"]
                resp = res1["results"]

                self.context["top_county_total_schools_enrollment"] = coun

                if coun > 0:
                    school_one_county = resp[0]
                    self.context["top_county_top_school_enrollment"] = school_one_county

            except Exception as e:
                print(e)

        return response

    def get_value_count(self, response):
        try:
            filtered_values = list(filter(lambda x: x["value"] is not None, response))
            return len(filtered_values)
        except Exception as E:
            return 0

    def get_sub_counties_enrollment(self, obj):
        # print(self.instance.user)
        res = get_any_stats("students", grouping="sub-county", user=self.instance.user, query_params=self.get_query_parms(obj))
        count = res["count"]
        response = res["results"]

        self.context["total_sub_counties_enrollment"] = self.get_value_count(response)

        if count > 0:
            sub_county_one = response[0]
            self.context["top_sub_county_enrollment"] = sub_county_one
        return response

    def get_schools_enrollment(self, obj):
        # print(self.instance.user)
        res = get_any_stats("students", grouping="school", user=self.instance.user, query_params=self.get_query_parms(obj))
        count = res["count"]
        self.context["total_schools_enrollment"] = count
        response = res["results"]
        if count > 0:
            school_one = response[0]
            self.context["top_school_enrollment"] = school_one
        return response


class OverAllReport(BaseCustomReport):
    def __init__(self, template) -> None:
        super(OverAllReport, self).__init__(template)

    def get_context(self, export):
        res = OverAllReportSerializer(export)
        context = res.data
        print("Getting contex...")
        print(context)
        return context

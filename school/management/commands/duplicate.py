from django.core.management.base import BaseCommand
import school.models as sh
import django.db.models as mds
import attendance.models as attmds


def iterate_in_batches(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i : i + batch_size]


class Command(BaseCommand):
    help = "Discover duplicate learners"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            type=str,
            default="true",
        )

        parser.add_argument(
            "--only",
            type=str,
            default="imports",
        )

        # parser.add_argument(
        #     "--start_date",
        #     type=str,
        #     default="imports",
        # )

        parser.add_argument(
            "--dry-run-count",
            type=int,
            default=102,
        )
        # parser.add_argument("modelName", type=str)

    def _printMessage(self, message, message_type="error"):
        if message_type == "error":
            self.stdout.write(
                self.style.ERROR(
                    "{}".format(message),
                ),
            )
        elif message_type == "info":
            self.stdout.write(
                self.style.WARNING(
                    "{}".format(message),
                ),
            )
        elif message_type == "success":
            self.stdout.write(
                self.style.SUCCESS(
                    "{}".format(message),
                ),
            )
        else:
            self.stdout.write(message)

    def printMessage(self, message):
        self._printMessage(message, "a")

    def printSuccess(self, message):
        self._printMessage(message, "success")

    def printWarning(self, message):
        self._printMessage(message, "info")

    def printError(self, message):
        self._printMessage(message, "error")

    def warning_message(self, options):
        if options["dry_run"] == "false":
            self.printError("**** STUDENTS WILL BE DELETED ******")

    def handle(self, *args, **options):
        # Your code here
        # self.printSuccess(str(options))
        dry_run_count = options["dry_run_count"]
        only = options["only"]
        self.printMessage("\n****** Welcome *******")
        if options["dry_run"] == "false":
            self.printError("\n**** STUDENTS WILL BE DELETED ******\n")
        queryset = sh.Student.objects.all()

        if only != "all":
            import_dates = list(sh.SchoolsStudentsImport.objects.all().values_list("created__date", flat=True))
            queryset = sh.Student.objects.filter(
                created__date__in=import_dates,
            )
            self.printSuccess(f"Found {len(import_dates)} Import Dates")
        else:
            self.printError("\n**** Working on all the learners ***** \n")

        ## Loop throug the students
        # sh.STUD_UNIQUE_NAME_CLASS
        pre_annotates = {
            "value": sh.STUD_UNIQUE_NAME_CLASS,
        }
        post_annotates = {
            "count": mds.Count("id"),
            "stream_sid": mds.F("stream_id"),
            "full_name": sh.STUD_FULL_NAMES,
        }
        fields = (key for key in {**pre_annotates, **post_annotates}.keys())

        self.printSuccess(f"Current learners count {sh.Student.objects.all().count()}")

        self.printMessage("Searching for duplicate learners...")

        queryset = (
            queryset.annotate(
                **pre_annotates,
            )
            .values("value")
            .annotate(**post_annotates)
            .filter(count__gt=1)
            .values(*fields)
            .order_by("-count")
        )
        # self.printSuccess(queryset.exists())
        # self.printSuccess(queryset.first())
        migrations = {}
        if not queryset.exists():
            self.printError("No Duplicates found.")
            return

        attendance_annotate = {
            "att_count": mds.Count("attendances"),
        }

        fields = (key for key in {**pre_annotates, **attendance_annotate}.keys())

        students_affected = 0
        attendances_affected = 0
        abasent_reasons_affected = 0
        total = queryset.count()
        completed = 0
        learners_to_delete = []
        for stud in list(queryset):
            completed += 1
            self.printWarning(f"\nWorking on {stud['full_name'].title()} ({stud['count']}) {completed}/{total}")
            stud_query = sh.Student.objects.all()
            stream_id = stud["stream_sid"]
            if stream_id != 0:
                stud_query = stud_query.filter(stream_id=stream_id)
            stud_query = (
                stud_query.annotate(
                    **pre_annotates,
                    **attendance_annotate,
                )
                .filter(value=stud["value"])
                .values("first_name", "att_count", "id")
                .order_by("-att_count")
            )
            # print(stud_query)

            main_id = stud_query.first()["id"]
            remain_ids = [std["id"] for std in list(stud_query.exclude(id=main_id))]

            # self.printWarning(f"\nWorking on {stud['full_name'].title()} ({stud['count']}) {completed}/{total}")
            # students_affected += len(remain_ids)
            learners_to_delete = [*learners_to_delete, *remain_ids]
            students_affected = len(learners_to_delete)
            ## Updare Attendande and Reason for absence
            # TODO: Ensure that both do not exists
            if "dry_run" in options and options["dry_run"] == "false":
                try:
                    attendances_affected += attmds.Attendance.objects.filter(student_id__in=remain_ids).update(student_id=main_id)
                    abasent_reasons_affected += sh.StudentAbsentReason.objects.filter(student_id__in=remain_ids).update(student_id=main_id)
                except Exception as e:
                    self.printError(str(e))
                    pass

                sh.Student.objects.filter(id__in=remain_ids).delete()
                # print(attendances_affected)
                self.warning_message(options=options)
                self.printSuccess(f"Deleted {students_affected} learners")
                self.printSuccess(f"Updated {attendances_affected} attendances")
                self.printSuccess(f"Updated {abasent_reasons_affected} reason for absence")
            else:
                # print(learners_to_delete)
                self.printWarning(f"Affected Learner {students_affected}")

            if options["dry_run"] != "false":
                if students_affected > dry_run_count:
                    break

            # self.printMessage(f"{main_id}")
            # self.printWarning(str(remain_ids))
        # for items in iterate_in_batches(learners_to_delete, 50000):
        #     # self.printWarning(str(items))
        #     sh.Student.objects.filter(id__in=items).delete()
        self.printSuccess(sh.Student.objects.all().count())
        self.printSuccess("*** DONE ***\n")

    # for learners_to_delete

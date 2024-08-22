from reports.utils import BaseCustomReport
from core.reports.overall import OverAllReport


class MonthlyReport(BaseCustomReport):
    def __init__(self, template) -> None:
        super(MonthlyReport, self).__init__(template)

    def get_context(self, export):
        return {
            "name": export.title,
            "old_password": export.description,
        }

CUSTOM_REPORTS = {
    "overall": OverAllReport("onekana_report.html"),
    "new_user": MonthlyReport("new_user.html"),
}

from model_report.report import reports, ReportAdmin
from appointment import models


class AnyModelReport(ReportAdmin):
    title = _('Appointments')
    model = Request_appointment
    fields = [
        'ailment',
    ]
    list_order_by = ('date_created',)
    type = 'report'

reports.register('Appointments-report', AnyModelReport)

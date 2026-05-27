
from odoo import fields, models


class HrAttendance(models.Model):
    _inherit='hr.attendance'
    
    late_minutes = fields.Float(string='Time Late')
    is_incomplete = fields.Boolean(string="Incomplete Attendance")
    attendance_status = fields.Selection([
        ('present', 'Present'),
        ('late', 'Late'),
        ('excused_late', 'Excused Late'),
        ('leave', 'Leave'),
        ('absent', 'Absent'),
    ], string="Attendance Status")

    
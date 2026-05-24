
from odoo import fields, models


class HrAttendance(models.Model):
    _inherit='hr.attendance'
    
    late_minutes = fields.Float(string='Time Late')

    
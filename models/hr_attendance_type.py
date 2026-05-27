
from odoo import models, fields


class HrAttendanceType(models.Model):
    _inherit = 'hr.leave.type'
    _description = 'HR Time off Type'
    
    is_late_permission = fields.Boolean(string='Is Late Permission')

from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    fingerprint_code = fields.Char(string="Fingerprint Code")
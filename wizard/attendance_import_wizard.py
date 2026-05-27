
import base64
from collections import defaultdict
from datetime import datetime, time
import tempfile
from datetime import timedelta

import xlrd
from odoo import fields, models


class AttendanceImportWizard(models.TransientModel):
    _name = 'attendance.import.wizard'
    _description = 'Attendance Import Files'
    
    
    import_file_att = fields.Binary(string="Excel File", required=True)
    filename_att = fields.Char()
    
    def action_import(self):
        self.ensure_one()
        
        if not self.import_file_att:
            return
        
        file_data = base64.b64decode(self.import_file_att)
        
        temp = tempfile.NamedTemporaryFile(suffix=".xls", delete=False)
        temp.write(file_data)
        temp.close()
         
        workbook = xlrd.open_workbook(temp.name)
        sheet = workbook.sheet_by_index(0)
        attendance_data = defaultdict(list)
        
        for row_idx in range(1, sheet.nrows):
            row = sheet.row_values(row_idx)
            employee_code = int(row[0])
            datetime_value = row[1]
            
            if not employee_code or not datetime_value:
                continue
            
            dt_tuple = xlrd.xldate_as_tuple(
                datetime_value, workbook.datemode
            )
            dt = datetime(*dt_tuple)
            date_key = dt.date()
            attendance_data[
                (employee_code, date_key)
            ].append(dt)
            
        for (employee_code, date_key), times in attendance_data.items():
            employee = self.env['hr.employee'].search([
                ('barcode', '=', str(employee_code))
            ], limit=1)
            
            if not employee:
                continue
            
            local_time_in = min(times)
            local_time_out = max(times)
            
            calendar = employee.resource_calendar_id
            weekday = str(local_time_in.weekday())

            attendance = calendar.attendance_ids.filtered(
                lambda a: a.dayofweek == weekday
            )[:1]
            if not attendance:
                continue
            
            hour = int(attendance.hour_from)
            minute = int((attendance.hour_from % 1) * 60)
            
            work_start = datetime.combine(
                local_time_in.date(),
                time(hour, minute)
            )
                
            if local_time_in > work_start:
                late_minutes = (
                    local_time_in - work_start   
                ).total_seconds()/60
            else:
                late_minutes=0
                
            is_incomplete = False
            
            check_in = local_time_in - timedelta(hours=7)
            check_out = local_time_out - timedelta(hours=7)
            
            if check_in == check_out:
                is_incomplete = True
                
            existing_attendance = self.env['hr.attendance'].search([
                ('employee_id', '=', employee.id),
                ('check_in', '>=', datetime.combine(date_key, time.min)),
            ], limit=1)
            
            if existing_attendance:
                continue
            
            attendance_status = 'present'
            if late_minutes > 0:
                leave = self.env['hr.leave'].search([
                    ('employee_id', '=', employee.id),
                    ('state', '=', 'validate'),
                    ('holiday_status_id.is_late_permission', '=', True),
                    ('request_date_from', '<=', date_key),
                    ('request_date_to', '>=', date_key),
                ], limit=1)
            
                if leave:
                    attendance_status = 'excused_late'
                else:
                    attendance_status = 'late'
                
            self.env['hr.attendance'].create({
                'employee_id': employee.id,
                'check_in': check_in,
                'check_out': check_out,
                'late_minutes': round(late_minutes, 2),
                'is_incomplete' : is_incomplete,
                'attendance_status': attendance_status,
            })
            
            
        
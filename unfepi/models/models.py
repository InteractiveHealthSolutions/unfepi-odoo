# -*- coding: utf-8 -*-

from odoo import models, fields, api

class unfepi(models.Model):
    _inherit = ['hr.attendance']

    # name_related = fields.Char(related='resource_id.name', string="Resource Name", readonly=True, store=True)
    # resource_id = fields.Many2one('resource.resource', string='Resource',
    #                               ondelete='cascade', required=True, auto_join=True)
    duty_type = fields.Selection([('0', 'Routine'),('1', 'Outreach')], 'Duty Type', required=True, index=True, default='0')
    assigned_location = fields.Char()
    assigned_latitude = fields.Char()
    assigned_longitude = fields.Char()
    calendar_id = fields.Many2one("resource.calendar", string='Assigned Working Time', help="The assigned working time")
    assigned_geopoint = fields.Char()
    assigned_checkin_time = fields.Float(string="Assigned Check In Time", required=True)
    assigned_checkout_time = fields.Float(string="Assigned Check Out Time", required=True)
    assigned_lax_period_minutes = fields.Char()

    checkin_latitude = fields.Char()
    checkin_longitude = fields.Char()
    checkin_geopoint = fields.Char()
    checkin_status = fields.Char()

    checkout_latitude = fields.Char()
    checkout_longitude = fields.Char()
    checkout_geopoint = fields.Char()
    checkout_status = fields.Char()

    # @api.depends('value')
    # def _value_pc(self):
    #     self.value2 = float(self.value) / 100

    @api.multi
    def name_get(self):
        result = []
        for attendance in self:
            if not attendance.check_out:
                result.append((attendance.id, ("%(empl_name)s from %(check_in)s") % {
                    'empl_name': attendance.employee_id.name_related,
                    'check_in': fields.Datetime.to_string(
                        fields.Datetime.context_timestamp(self, fields.Datetime.from_string(attendance.check_in))),
                }))
            else:
                result.append((attendance.id, ("%(empl_name)s from %(check_in)s to %(check_out)s") % {
                    'empl_name': attendance.employee_id.name_related,
                    'check_in': fields.Datetime.to_string(
                        fields.Datetime.context_timestamp(self, fields.Datetime.from_string(attendance.check_in))),
                    'check_out': fields.Datetime.to_string(
                        fields.Datetime.context_timestamp(self, fields.Datetime.from_string(attendance.check_out))),
                }))
        return result

    @api.model
    def search_custom(self, domain=None, fields=None, offset=0, limit=None, order=None):
        self.env['resource.calendar.attendance'].search_read([[]])

    @api.model
    def get_working_time(self):
        a = self.env['resource.calendar'].search([])
        records = []
        for t in a:
            records.append(t.read()[0])
        for temp in records:
            temp['working_time_records'] = []
            for a in temp['attendance_ids']:
                temp['working_time_records'].append(self.env['resource.calendar.attendance'].search_read([('id','=',a)])[0])
        print records
        # for rec in records:
        #     rec['parent_name'] = a.name
        return records

	    def get_emp_attendances(self, date_start, date_end):
        employees = self.env['hr.employee'].search([])
        empRecords = {}
        for emp in employees:
            emp_att_recs = self.search([('employee_id', '=', emp.id)])
            list = []
            for rec in emp_att_recs:
                if rec.check_in[0:10] >= date_start and rec.check_in[0:10] <= date_end:
                    record_read = rec.read()[0]
                    att_dict = {}
                    att_dict["employee"] = record_read["employee_id"]
                    att_dict["check_in"] = record_read["check_in"]
                    att_dict["check_out"] = record_read["check_out"]
                    # att_dict["calendar_id"] = record_read["calendar_id"]
                    att_dict["duty_type"] = record_read["duty_type"]
                    att_dict["checkin_status"] = record_read["checkin_status"]
                    att_dict["checkout_status"] = record_read["checkout_status"]
                    att_dict["employee_unique_id"] = rec.employee_id.identification_id
                    list.append(att_dict)
            if emp.identification_id is not False:
                empRecords[emp.identification_id] = list
        print empRecords
        return empRecords

    def get_attendances(self, date_start, date_end):
        attendances = []
        attendance_records = self.search([])
        for rec in attendance_records:
            if rec.check_in[0:10] >= date_start and rec.check_in[0:10] <= date_end:
                dict = rec.read()[0]
                att_dict = {}
                att_dict["employee"] = dict["employee_id"]
                att_dict["check_in"] = dict["check_in"]
                att_dict["check_out"] = dict["check_out"]
                att_dict["calendar_id"] = dict["calendar_id"]
                att_dict["duty_type"] = dict["duty_type"]
                att_dict["checkin_status"] = dict["checkin_status"]
                att_dict["checkout_status"] = dict["checkout_status"]
                att_dict["employee_unique_id"] = rec.employee_id.identification_id
                attendances.append(att_dict)
        return attendances
		
class holidays_custom(models.Model):
    _inherit = ['hr.holidays.public.line']

    def is_holiday(self, date, state):
        temp = self.env['hr.holidays.public.line'].search([('date', '=', '2017-02-05')])
        bool = False;
        for t in temp:
            for s in t.state_ids:
                print "*************************  "
                print s.name == 'Karachi'
                if (s.name.encode('utf8')).lower() == state.lower():
                    return True

        return False

    def create_state(self,country_name, name, code):
        country = self.env['res.country'].search([('name','=',country_name)])
        if country.id is False:
            country = self.env['res.country'].create({'name':country_name})
        record = self.env['res.country.state'].create({'name':name,'code':code,'country_id':country.id})
        return record.id
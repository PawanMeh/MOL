from __future__ import unicode_literals
import frappe
from frappe.utils import cint, flt, add_months, today, date_diff, getdate, add_days, cstr, time_diff_in_hours
from frappe import _

def auto_approve_leaves():
	leave_pending_approval = frappe.db.sql('''select name
												from `tabLeave Application`
												where DATE(modified) = (DATE(CURDATE()) - INTERVAL 7 DAY)
												and docstatus = 0
												and approval_status = 'Submitted'
												''', as_dict = 1)
	for leave in leave_pending_approval:
		leave_doc = frappe.get_doc("Leave Application", leave['name'])
		leave_doc.approval_status = "Approved"
		try:
			leave_doc.submit()
		except Exception as e:
			error_string = "Auto-approve leave: " + leave['name']
			frappe.log_error(message = e, title = error_string)

def auto_approve_timesheet():
	timesheet_pending_approval = frappe.db.sql('''select name
													from `tabTimesheet`
													where DATE(modified) = (DATE(CURDATE()) - INTERVAL 7 DAY)
													and docstatus = 0
													and mol_approval_status = 'Submitted'
												''', as_dict = 1)
	for timesheet in timesheet_pending_approval:
		timesheet_doc = frappe.get_doc("Timesheet", timesheet['name'])
		timesheet_doc.approval_status = "Approved"
		try:
			timesheet_doc.submit()
		except Exception as e:
			error_string = "Auto-approve timesheet: " + timesheet['name']
			frappe.log_error(message = e, title = error_string)

def validate_attendance(self, method):
	if self.in_time > self.out_time:
		frappe.throw(_("Out time should be greater than in time"))
	time_diff_hours = time_diff_in_hours(self.out_time, self.in_time)
	if self.status in ["Present", "Half Day"]:
		if time_diff_hours >= 8:
			self.status = "Present"
		elif (time_diff_hours >= 4 and time_diff_hours < 8):
			self.status = "Half Day"
		else:
			frappe.throw(_("To mark attendance as Present or Half Day, hours should be greater than or equal to 4"))
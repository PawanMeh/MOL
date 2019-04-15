# Copyright (c) 2013, hello@openetech.com and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _, utils
from erpnext.hr.doctype.leave_application.leave_application \
	import get_leave_allocation_records, get_leave_balance_on, get_approved_leaves_for_period, get_total_allocated_leaves


def execute(filters=None):
	leave_types = frappe.db.sql_list("select name from `tabLeave Type` order by name asc")

	columns = get_columns(leave_types)
	data = get_data(filters, leave_types)

	return columns, data

def get_columns(leave_types):
	columns = [
		_("Employee") + ":Link/Employee:150",
		_("Employee Name") + "::200",
		_("Department") +"::150"
	]

	for leave_type in leave_types:
		columns.append(_(leave_type) + " " + _("Opening") + ":Float:160")
		columns.append(_(leave_type) + " " + _("Added") + ":Float:160")
		columns.append(_(leave_type) + " " + _("Taken") + ":Float:160")
		columns.append(_(leave_type) + " " + _("Balance") + ":Float:160")

	return columns

def get_data(filters, leave_types):
	dates = frappe.db.sql('''select
									year_start_date, year_end_date
							from 
								`tabFiscal Year`
							where name = %s''', filters.fiscal_year)
	start_date = dates[0][0]
	end_date = dates[0][1]
	allocation_records_based_on_to_date_prev_year = get_leave_allocation_records(frappe.utils.add_days(start_date, -1))
	allocation_records_based_on_to_date = get_leave_allocation_records(end_date)
	allocation_records_based_on_from_date = get_leave_allocation_records(start_date)

	active_employees = frappe.get_all("Employee",
		filters = { "status": "Active", "company": filters.company},
		fields = ["name", "employee_name", "department", "user_id"])

	data = []
	for employee in active_employees:
		row = [employee.name, employee.employee_name, employee.department]
		for leave_type in leave_types:
			# leaves taken
			leaves_taken = get_approved_leaves_for_period(employee.name, leave_type,
				start_date, end_date)
			#prev_year_opening
			prev_year_end_date = frappe.utils.add_days(start_date, -1);
			prev_year_opening = get_leave_balance_on(employee.name, leave_type, prev_year_end_date,
				allocation_records_based_on_to_date_prev_year.get(employee.name, frappe._dict()))
			# opening balance
			opening = get_total_allocated_leaves(employee.name, leave_type, end_date)
			# closing balance
			closing = get_leave_balance_on(employee.name, leave_type, end_date,
				allocation_records_based_on_to_date.get(employee.name, frappe._dict()))

			row += [prev_year_opening, opening, leaves_taken, closing]

		data.append(row)

	return data
// Copyright (c) 2016, hello@openetech.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["MOL Yearly Leave Balance"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.defaults.get_default("year_start_date"),
			"read_only": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"default": frappe.defaults.get_default("year_end_date")
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("Company")
		}
	]
}
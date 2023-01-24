# Copyright (c) 2023, Wahni IT Solution and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate


def execute():
	skipped = frappe.db.get_all(
		"Employee Checkin",
		filters={"skip_auto_attendance": 1, "time": ["between", ["2023-01-01", "2023-01-23"]]},
		fields=["employee", "name", "time"]
	)

	for d in skipped:
		frappe.db.set_value("Employee Checkin", d.name, "skip_auto_attendance", 0)
		attendance = frappe.db.get_value(
			"Attendance", 
			{"docstatus": 1, "attendance_date": getdate(d.time), "employee": d.employee},
			"name"
		)
		if attendance:
			doc = frappe.get_doc("Attendance", attendance)
			doc.cancel()
			doc.delete()
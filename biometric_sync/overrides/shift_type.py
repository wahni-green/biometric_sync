# Copyright (c) 2023, Wahni IT Solution and contributors
# For license information, please see license.txt

import itertools

import frappe
from frappe.utils import add_days, cint, getdate, nowdate
from erpnext.hr.doctype.shift_type.shift_type import ShiftType
from erpnext.hr.doctype.employee_checkin.employee_checkin import (
	mark_attendance_and_link_log
)


class CustomShiftType(ShiftType):
	@frappe.whitelist()
	def process_auto_attendance(self):
		if (
			not cint(self.enable_auto_attendance)
		):
			return
		
		biometic_devices = frappe.db.get_all("Biometric Device", fields=[
			"machine_id", "process_attendance_after", "last_sync_of_checkin"
		])

		for device in biometic_devices:
			if not device.last_sync_of_checkin or not device.process_attendance_after:
				continue

			self.process_machine_attendance(
				device.machine_id,
				device.process_attendance_after,
				device.last_sync_of_checkin
			)
		
		for employee in self.get_assigned_employee(self.process_attendance_after, True):
			self.mark_absent_for_dates_with_no_attendance(employee)

	def process_machine_attendance(self, device, process_attendance_after, last_sync_of_checkin):
		filters = {
			"skip_auto_attendance": 0,
			"attendance": ("is", "not set"),
			"time": (">=", process_attendance_after),
			"shift_actual_end": ("<", last_sync_of_checkin),
			"shift": self.name,
			"device_id": device
		}
		logs = frappe.db.get_list(
			"Employee Checkin", fields="*", filters=filters, order_by="employee,time"
		)

		for key, group in itertools.groupby(
			logs, key=lambda x: (x["employee"], x["shift_actual_start"])
		):
			single_shift_logs = list(group)
			(
				attendance_status,
				working_hours,
				late_entry,
				early_exit,
				in_time,
				out_time,
			) = self.get_attendance(single_shift_logs)

			mark_attendance_and_link_log(
				single_shift_logs,
				attendance_status,
				key[1].date(),
				working_hours,
				late_entry,
				early_exit,
				in_time,
				out_time,
				self.name,
			)


def update_late_logs():
	logs = frappe.db.get_all(
		"Employee Checkin", fields=["employee", "time", "name", "device_id"],
		filters={"skip_auto_attendance": 1, "time": (">=", add_days(nowdate(), -3))}
	)
	for d in logs:
		try:
			device_id = d.device_id
			attendance = frappe.db.get_value(
				"Attendance",
				{
					"employee": d.employee,
					"attendance_date": getdate(d.time),
					"docstatus": 1,
					"status": ("!=", "Absent")
				},
				"name"
			)
			if attendance:
				device_id = frappe.db.get_value("Employee Checkin", {"attendance": attendance}, "device_id")
				frappe.get_doc("Attendance", attendance).cancel()
			device_id = device_id or d.device_id
			frappe.db.set_value("Employee Checkin", d.name, {
				"skip_auto_attendance": 0,
				"device_id": device_id
			})
			if device_id != d.device_id:
				frappe.get_doc(
					{
						"doctype": "Comment",
						"comment_type": "Comment",
						"reference_doctype": "Employee Checkin",
						"reference_name": d.name,
						"content": f"Device ID changed from {d.device_id} to {device_id} to process attendance.",
					}
				).insert(ignore_permissions=True)
		except Exception:
			continue

# Copyright (c) 2023, Wahni IT Solution and contributors
# For license information, please see license.txt

import itertools

import frappe
from frappe import _
from frappe.utils import cint
from erpnext.hr.doctype.shift_type.shift_type import ShiftType
from erpnext.hr.doctype.employee_checkin.employee_checkin import (
	add_comment_in_checkins,
	skip_attendance_in_checkins,
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


def mark_attendance_and_link_log(
	logs,
	attendance_status,
	attendance_date,
	working_hours=None,
	late_entry=False,
	early_exit=False,
	in_time=None,
	out_time=None,
	shift=None,
):
	"""Creates an attendance and links the attendance to the Employee Checkin.
	Note: If attendance is already present for the given date, the logs are marked as skipped and no exception is thrown.
	:param logs: The List of 'Employee Checkin'.
	:param attendance_status: Attendance status to be marked. One of: (Present, Absent, Half Day, Skip). Note: 'On Leave' is not supported by this function.
	:param attendance_date: Date of the attendance to be created.
	:param working_hours: (optional)Number of working hours for the given date.
	"""
	log_names = [x.name for x in logs]
	employee = logs[0].employee
	if attendance_status == "Skip":
		skip_attendance_in_checkins(log_names)
		return None

	elif attendance_status in ("Present", "Absent", "Half Day"):
		company = frappe.get_cached_value("Employee", employee, "company")
		duplicate = frappe.db.get_value(
			"Attendance",
			{"employee": employee, "attendance_date": attendance_date, "docstatus": ("!=", "2")},
			"name"
		)

		if duplicate:
			try:
				frappe.get_doc("Attendance", duplicate).cancel()
			except Exception:
				skip_attendance_in_checkins(log_names)
				add_comment_in_checkins(log_names, duplicate)
				return None

		doc_dict = {
			"doctype": "Attendance",
			"employee": employee,
			"attendance_date": attendance_date,
			"status": attendance_status,
			"working_hours": working_hours,
			"company": company,
			"shift": shift,
			"late_entry": late_entry,
			"early_exit": early_exit,
			"in_time": in_time,
			"out_time": out_time,
		}
		attendance = frappe.get_doc(doc_dict).insert()
		attendance.submit()

		if attendance_status == "Absent":
			attendance.add_comment(
				text=_("Employee was marked Absent for not meeting the working hours threshold.")
			)

		frappe.db.sql(
			"""update `tabEmployee Checkin`
			set attendance = %s
			where name in %s""",
			(attendance.name, log_names),
		)
		return attendance

	else:
		frappe.throw(_("{} is an invalid Attendance Status.").format(attendance_status))
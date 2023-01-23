# Copyright (c) 2023, Wahni IT Solution and contributors
# For license information, please see license.txt

import itertools

import frappe
from frappe.utils import cint
from erpnext.hr.doctype.shift_type.shift_type import ShiftType
from erpnext.hr.doctype.employee_checkin.employee_checkin import (
	mark_attendance_and_link_log,
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

		for employee in self.get_assigned_employee(process_attendance_after, True):
			self.mark_absent_for_dates_with_no_attendance(employee)
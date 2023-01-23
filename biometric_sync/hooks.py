from . import __version__ as app_version

app_name = "biometric_sync"
app_title = "Biometric Sync"
app_publisher = "Wahni IT Solution"
app_description = "Biometric machine wise attendance marking"
app_email = "danyrt@wahni.com"
app_license = "GNU GPL v3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/biometric_sync/css/biometric_sync.css"
# app_include_js = "/assets/biometric_sync/js/biometric_sync.js"

# include js, css files in header of web template
# web_include_css = "/assets/biometric_sync/css/biometric_sync.css"
# web_include_js = "/assets/biometric_sync/js/biometric_sync.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "biometric_sync/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "biometric_sync.utils.jinja_methods",
#	"filters": "biometric_sync.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "biometric_sync.install.before_install"
# after_install = "biometric_sync.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "biometric_sync.uninstall.before_uninstall"
# after_uninstall = "biometric_sync.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "biometric_sync.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Shift Type": "biometric_sync.overrides.shift_type.CustomShiftType"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"biometric_sync.tasks.all"
#	],
#	"daily": [
#		"biometric_sync.tasks.daily"
#	],
#	"hourly": [
#		"biometric_sync.tasks.hourly"
#	],
#	"weekly": [
#		"biometric_sync.tasks.weekly"
#	],
#	"monthly": [
#		"biometric_sync.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "biometric_sync.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "biometric_sync.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "biometric_sync.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"biometric_sync.auth.validate"
# ]

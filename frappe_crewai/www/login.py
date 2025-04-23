import frappe
from frappe import _
from frappe.auth import LoginManager
from frappe.utils.response import redirect

def get_context(context):
    context.message = ""

    if frappe.request.method == "POST":
        usr = frappe.form_dict.get("usr")
        pwd = frappe.form_dict.get("pwd")

        try:
            frappe.local.login_manager = LoginManager()
            frappe.local.login_manager.authenticate(usr, pwd)
            frappe.local.login_manager.post_login()

            redirect("/app")  # or any desired post-login route
        except frappe.AuthenticationError:
            context.message = _("Invalid login credentials")

    return context

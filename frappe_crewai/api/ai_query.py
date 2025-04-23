import frappe
from frappe_crewai.crew.frappe_ai_crew import FrappeAiCrew

@frappe.whitelist(allow_guest=True)
def ask_ai(query):
    try:
        ai_crew = FrappeAiCrew()
        result = ai_crew.crew().kickoff(inputs={'topic': query})
        return {'result': result}
    except Exception as e:
        error_msg = str(e)[:135]  # Truncate to 135 characters
        frappe.log_error(f"AI Error: {error_msg}")
        return {'error': error_msg}

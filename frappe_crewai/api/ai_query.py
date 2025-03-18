import frappe
from frappe_crewai.crew.frappe_ai_crew import FrappeAiCrew

@frappe.whitelist(allow_guest=True)
def ask_ai(query):
    try:
        ai_crew = FrappeAiCrew()
        ai_crew.crew().kickoff(inputs={'question': query})
        result = ai_crew.crew().output
        return {'result': result}
    except Exception as e:
        frappe.log_error(f"AI Query Error: {str(e)}")
        return {'error': str(e)}

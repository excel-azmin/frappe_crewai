import frappe
from crewai_tools import MySQLSearchTool

def get_all_mysql_tools():
    db_name = frappe.conf.db_name
    db_user = frappe.conf.db_username or 'frappe'
    db_password = frappe.conf.db_password
    db_host = frappe.conf.db_host or 'localhost'

    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"
    tables = frappe.db.get_tables()

    tools = []
    for table in tables:
        tool = MySQLSearchTool(
            db_uri=db_uri,
            table_name=table,
            config=dict(
                llm=dict(
                    provider="ollama",
                    config=dict(
                        model="deepseek-coder:6.7b",
                        temperature=0
                    )
                ),
                embedder=dict(
                    provider="ollama",
                    config=dict(
                        model="nomic-embed-text"
                    )
                )
            )
        )
        tools.append(tool)

    return tools

from crewai_tools import MySQLSearchTool

def get_all_mysql_tools():
    import frappe

    db_name = frappe.conf.db_name
    db_user = frappe.conf.db_username or 'frappe'
    db_password = frappe.conf.db_password
    db_host = frappe.conf.db_host or 'localhost'

    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"
    ollama_url = 'http://ollama:11434'

    tools = []
    tables = ['tabUser']  # You can fetch this dynamically if needed

    for table in tables:
        tool = MySQLSearchTool(
            table_name=table,
            host=db_host,
            port=3306,
            database=db_name,
            user=db_user,
            password=db_password,
            db_uri=db_uri,
            config=dict(
                llm=dict(
                    provider='ollama',
                    config=dict(
                        model='deepseek-r1:1.5b',
                        temperature=0.0,
                        base_url=ollama_url
                    )
                ),
                embedder=dict(
                    provider='ollama',
                    config=dict(
                        model='nomic-embed-text',
                        base_url=ollama_url
                    )
                )
            )
        )
        tools.append(tool)

    return tools

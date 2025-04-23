from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew
from frappe_crewai.tools.mysql_tool import get_all_mysql_tools  # Ensure this returns a List[BaseTool]

@CrewBase
class FrappeAiCrew:
    """AI Crew for ERPNext Semantic Search"""

    agents_config = 'frappe_crewai/config/agents.yaml'
    tasks_config = 'frappe_crewai/config/tasks.yaml'

    # LLM Setup
    ollama_llm = LLM(
        model='ollama/deepseek-r1:1.5b',
        api_base='http://ollama:11434',
        temperature=0.3
    )

    @agent
    def erpnext_agent(self) -> Agent:
        # Dynamically fetch tools at runtime
        mysql_tools = get_all_mysql_tools()

        return Agent(
            config=self.agents_config['erpnext_agent'],
            llm=self.ollama_llm,
            tools=mysql_tools,
            verbose=True,
            output_format='raw'
        )

    @task
    def erpnext_task(self) -> Task:
        return Task(
            config=self.tasks_config['erpnext_task']
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.erpnext_agent()],
            tasks=[self.erpnext_task()],
            process=Process.sequential,
            verbose=True
        )

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew
from frappe_crewai.tools.mysql_tool import get_all_mysql_tools

@CrewBase
class FrappeAiCrew():
    """AI Crew for ERPNext Semantic Search"""

    # YAML Config Paths
    agents_config_path = 'frappe_crewai/config/agents.yaml'
    tasks_config_path = 'frappe_crewai/config/tasks.yaml'

    print("\n\n Im from FranppeAiCrew \n\n")

    # LLM Setup: DeepSeek via Ollama
    # LLM Setup: DeepSeek via Ollama
    ollama_llm = LLM(
        model='ollama/deepseek-r1:8b',
        base_url='http://localhost:11434',
    )

    print("\n\n Im from FranppeAiCrew \n\n", str(ollama_llm),"\n\n Im from FranppeAiCrew \n\n")
    # Load MySQL Tools for all tables
    mysql_tools = get_all_mysql_tools()

    @agent
    def erpnext_agent(self) -> Agent:
        return Agent(
            config=self.agents_config_path + ':erpnext_data_expert',
            llm=self.ollama_llm,
            tools=self.mysql_tools,
            verbose=True,
            output_format='raw'
        )

    @task
    def erpnext_task(self) -> Task:
        return Task(
            config=self.tasks_config_path + ':answer_question',
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.erpnext_agent],
            tasks=[self.erpnext_task],
            process=Process.sequential,
            verbose=True
        )

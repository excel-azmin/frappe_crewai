from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew
from frappe_crewai.tools.mysql_tool import get_all_tools  # Ensure this returns a List[BaseTool]
# from langchain.prompts import PromptTemplate
# from langchain.chains.router import MultiPromptChain




# 1. Intent Router Setup
# sql_prompt = PromptTemplate.from_template("""SQL Question: {input}""")
# semantic_prompt = PromptTemplate.from_template("""Semantic Question: {input}""")

# intent_router = MultiPromptChain(
#     prompt_infos=[
#         {"name": "sql", "prompt_template": sql_prompt},
#         {"name": "semantic", "prompt_template": semantic_prompt},
#     ],
#     llm=LLM(model='llama3.2:1b', api_base='http://ollama:11434')
# )


@CrewBase
class FrappeAiCrew:
    """AI Crew for ERPNext Semantic Search"""
    def __init__(self):
        self.ollama_llm = LLM(
            model='ollama/llama3.2:1b',
            api_base='http://ollama:11434',
            temperature=0.3
        )

    agents_config = 'frappe_crewai/config/agents.yaml'
    tasks_config = 'frappe_crewai/config/tasks.yaml'

    # # LLM Setup
    # ollama_llm = LLM(
    #     model='ollama/llama3.2:1b',
    #     api_base='http://ollama:11434',
    #     temperature=0.3
    # )

    @agent
    def erpnext_agent(self) -> Agent:
        # Dynamically fetch tools at runtime
        tools = get_all_tools()

        return Agent(
            config=self.agents_config['erpnext_agent'],
            llm=self.ollama_llm,
            tools=tools,
            verbose=True,
            output_format='text',
            # decision_maker=intent_router 
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

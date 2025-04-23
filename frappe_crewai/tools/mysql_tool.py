from crewai_tools import MySQLSearchTool
from crewai_tools import QdrantVectorSearchTool
from transformers import AutoTokenizer, AutoModel
import torch





tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

def custom_embeddings(text: str) -> list[float]:
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings[0].tolist()


def get_all_tools():
    import frappe

    db_name = frappe.conf.db_name
    db_user = frappe.conf.db_username or 'frappe'
    db_password = frappe.conf.db_password
    db_host = frappe.conf.db_host or 'localhost'

    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"
    ollama_url = 'http://ollama:11434'

    tools = []
    tables = ['tabUser',] 
    
    for table in tables:
        tool = MySQLSearchTool(
            name="mysql_search",
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
                        model='llama3.2:1b',
                        temperature=0.2,
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
        tools.append(QdrantVectorSearchTool(
        name="qdrant_search",    
        collection_name='frappe',
        qdrant_url='http://192.168.110.216:6333',
        custom_embedding_fn=custom_embeddings,
        qdrant_api_key='',
        limit=5,
        score_threshold=0.3
        ))
        print("Appened data : \n\n\n",str(tool))

    return tools

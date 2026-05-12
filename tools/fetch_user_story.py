from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
load_dotenv()
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from pprint import pprint
from typing import List, Tuple
import os

def fetch_user_story() -> Tuple[List[str], List[int]]:
    organization_url = "https://dev.azure.com/creditsafe"
    project = "Testing"
    team = "Testing Team"
    iteration_path = "CTM 1"   # Example: ProjectName\Sprint 5
    pat = "os.getenv('ADO_PAT')"
    credentials = BasicAuthentication('', pat)

    connection = Connection(base_url=organization_url, creds=credentials)
    wit_client = connection.clients.get_work_item_tracking_client()
    core_client = connection.clients.get_core_client()

    wiql_query = f"""
    SELECT
        [System.Id],
        [System.Title],
        [System.State],
        [System.WorkItemType]
    FROM workitems
    WHERE
        [System.IterationPath] = '{iteration_path}'
    ORDER BY [System.Id]
    """

    wiql = {"query": wiql_query}
    wiql_results = wit_client.query_by_wiql(wiql, project=project)

    work_item_ids = [item.id for item in wiql_results.work_items]

    work_items = wit_client.get_work_items(ids=work_item_ids, expand="All")

    for item in work_items:
        fields = item.fields
        # print(f"ID: {item.id}")
        # print(f"Type: {fields.get('System.WorkItemType')}")
        # print(f"Title: {fields.get('System.Title')}")
        # print(f"State: {fields.get('System.State')}")
        # print(f"Assigned To: {fields.get('System.AssignedTo').display_name if fields.get('System.AssignedTo') else None}")
        # print(f"Iteration: {fields.get('System.IterationPath')}")
        # print(f"Tags: {fields.get('System.Tags')}")
        if item.id == "584035"
        description = fields.get("System.Description", "")
        print(f"description :{description}")
    return description

        
        

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()
llm = ChatOpenAI(model="qwen/qwen3.6-plus-preview:free",  temperature=0.2)
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from pprint import pprint

def fetch_user_story() -> str:
    organization_url = "https://dev.azure.com/YOUR_ORG"
    project = "YOUR_PROJECT_NAME"
    team = "YOUR_TEAM_NAME"
    iteration_path = "YOUR_PROJECT_NAME\\Sprint 5"   # Example: ProjectName\Sprint 5
    pat = "YOUR_PERSONAL_ACCESS_TOKEN"

    # ----------------------------------------------------
    # AUTHENTICATION
    # ----------------------------------------------------
    credentials = BasicAuthentication('', pat)
    connection = Connection(base_url=organization_url, creds=credentials)

    wit_client = connection.clients.get_work_item_tracking_client()
    core_client = connection.clients.get_core_client()

    # ----------------------------------------------------
    # STEP 1: Run WIQL through SDK to get work item IDs
    # ----------------------------------------------------
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

    print("🔍 Fetching work item IDs...")
    wiql_results = wit_client.query_by_wiql(wiql, project=project)

    if not wiql_results.work_items:
        print("⚠️ No work items found for sprint:", iteration_path)
        exit()

    work_item_ids = [item.id for item in wiql_results.work_items]
    print(f"✅ Found {len(work_item_ids)} work items")

    # ----------------------------------------------------
    # STEP 2: Get full details for each work item
    # ----------------------------------------------------
    print("\n📌 Fetching full work item details...\n")
    work_items = wit_client.get_work_items(ids=work_item_ids, expand="All")

    for item in work_items:
        fields = item.fields
        print("--------------------------------------")
        print(f"ID: {item.id}")
        print(f"Type: {fields.get('System.WorkItemType')}")
        print(f"Title: {fields.get('System.Title')}")
        print(f"State: {fields.get('System.State')}")
        print(f"Assigned To: {fields.get('System.AssignedTo').display_name if fields.get('System.AssignedTo') else None}")
        print(f"Iteration: {fields.get('System.IterationPath')}")
        print(f"Tags: {fields.get('System.Tags')}")

        
        

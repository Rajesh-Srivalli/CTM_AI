from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
load_dotenv()
#llm = ChatOpenAI(model="google/gemma-4-26b-a4b-it:free",  temperature=0.2)
#llm = ChatOllama(model="gemma3:270m", temperature=0.2)
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.work_item_tracking.models import JsonPatchOperation
from pprint import pprint
from typing import List, Tuple

def update_user_story(user_story_id: List[int], acceptance_criteria: List[str], test_cases: List[str] ) -> str:
    
    # organization_url = "https://dev.azure.com/YOUR_ORG"
    # project = "UPP"
    # pat = "YOUR_PAT"

    # credentials = BasicAuthentication('', pat)
    # connection = Connection(base_url=organization_url, creds=credentials)
    # wit_client = connection.clients.get_work_item_tracking_client()

    # def build_patch_document(acceptance_criteria: str, test_cases: str) -> List[JsonPatchOperation]:
    #     patch_document = [
    #     # Update Title
    #     JsonPatchOperation(
    #         op="add",
    #         path="/fields/System.Acceptance Criteria",
    #         value= acceptance_criteria
    #     ),

    #     # Update Description
    #     JsonPatchOperation(
    #         op="add",
    #         path="/fields/System.Test Cases",
    #         value=test_cases
    #     )

    #     ]
    #     return patch_document

    # len = len(user_story_id)
    # for i in range(len):
    #     patch_document = build_patch_document(acceptance_criteria[i], test_cases[i])
    #     work_item_id = user_story_id[i]
    #     updated_item = wit_client.update_work_item(
    #         document=patch_document,
    #         id=work_item_id,
    #         project=project
    #     )

    # print("✅ Work Item Updated Successfully!")
    # print("ID:", updated_item.id)
    # print("Title:", updated_item.fields.get("System.Title"))
    # print("State:", updated_item.fields.get("System.State"))

    return "update is successfull"



    
        
        

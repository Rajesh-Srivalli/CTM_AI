import sys
from pathlib import Path

from typing import List

# Add project root to Python path so we can import tools
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from tools.acceptance_criteria import create_acceptance_criteria as ac_func
from tools.test_cases import create_test_cases as tc_func
from tools.fetch_user_story import fetch_user_story as fu_func
from tools.update_user_story import update_user_story as uu_func
import os

load_dotenv()

messages = [
        SystemMessage(
            content=(
                "You are a QA assisting agent. "
                "You have access to a acceptance criteria tool for acceptance criteria creation and test cases creation tool for test case creation and fetch user story tool to fetch user stories  \n\n"

                "STRICT RULES — you must follow these exactly:\n"
                "1. NEVER guess or assume any outcome of the tool.\n"
                "2. ALWAYS use the specific tool when you need to create.\n"
            )
        ),
        HumanMessage(content="create acceptance criteria and test cases for the user stories. Fetch the user stories and their ids from azure devops sprint board. Update the user story with acceptance criteria and test cases."),

    ]

llm = ChatOllama(model=os.getenv("LLM_MODEL"), num_ctx=2048,temperature=0)

@tool
def create_acceptance_criteria(user_stories: List[str]) -> str:
    """
    Create acceptance criteria for a given user_story.
    only use this tool to create acceptance criteria, do not use this tool for any other purpose.
    """
    return ac_func(user_stories)

@tool
def create_test_cases(acceptance_criterias: List[str]) -> str:
    """
    Create test cases for a given acceptance criteria.
    only use this tool to create test cases, do not use this tool for any other purpose.
    """
    return tc_func(acceptance_criterias)

@tool
def fetch_user_story() -> List[str]:
    """
    Fetch user stories and their IDs from Azure DevOps.
    only use this tool to fetch user stories, do not use this tool for any other purpose.
    """
    return fu_func()

@tool
def update_user_story(user_story_id: List[int], acceptance_criteria: List[str], test_cases: List[str] ) -> None:
    """
    Update the user story with acceptance criteria and test cases in Azure DevOps.
    only use this tool to update user stories, do not use this tool for any other purpose
    """
    return uu_func(user_story_id, acceptance_criteria, test_cases)

tools=[create_acceptance_criteria, create_test_cases, fetch_user_story]

agent = create_agent(
    model=llm,
    tools=tools,
)

def main():
    result = agent.invoke({"messages": messages})

if __name__ == "__main__":
    main()

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
                
       "You are a QA Assisting Agent.\n\n"
        "You have access to the following tools:\n"
        "- fetch_user_story (to retrieve user stories)\n"
        "- create_acceptance_criteria (to create acceptance criteria)\n"
        "- update_user_story (to update user story with acceptance criteria and test cases)\n"
        "- create_test_cases (to create test cases)\n\n"
        "STRICT RULES — you must follow these exactly:\n"
        "1. NEVER guess, assume, or predict any output or result from a tool.\n"
        "2. ALWAYS use the appropriate tool when creating acceptance criteria or test cases.\n"
        "3. Do NOT manually create acceptance criteria or test cases without using the tools.\n"
        "4. Ensure all updates are applied directly to the corresponding Azure DevOps user story."

            )
        ),
        HumanMessage(content=(
"Fetch all user stories and their IDs from the Azure DevOps sprint board. "
        "For each user story:\n"
        "- Create acceptance criteria using the Acceptance Criteria Creation Tool.\n"
        "- Create test cases using the Test Case Creation Tool.\n"
        "- Update the respective user story with the generated acceptance criteria and test cases.\n\n"
        "Do not make any assumptions and rely only on tool-generated outputs."
        )
)

    ]

llm = ChatOpenAI(model=os.getenv("LLM_MODEL"), temperature=0)

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

tools=[create_acceptance_criteria, create_test_cases, fetch_user_story,update_user_story]

agent = create_agent(
    model=llm,
    tools=tools,
)

def main():
    result = agent.invoke({"messages": messages})

if __name__ == "__main__":
    main()

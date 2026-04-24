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
    {
        "role": "user",
        "content": (
            "Execute the task now.\n"
            "Step 1: Fetch user stories from Azure DevOps.\n"
            "Step 2: Create acceptance criteria for each story.\n"
            "Step 3: Create test cases for each acceptance criteria.\n"
            "Step 4: Update each user story with acceptance criteria and test cases.\n"
            "Do not explain steps. Perform them using tools."
        )
    }
]


llm = ChatOllama(model=os.getenv("LLM_MODEL"), num_ctx=2048,temperature=0)

@tool
def create_acceptance_criteria(user_stories: List[str]) -> str:
    """
    Create acceptance criteria for a given user_story.
    only use this tool to create acceptance criteria, do not use this tool for any other purpose.
    """
    print("creating acceptance criteria for user stories", user_stories[0])
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
    system_prompt=
"""

You are a QA assisting agent.

You must execute tasks ONLY by calling tools.

IMPORTANT DATA FLOW RULES:
1. When a tool returns data, you MUST store it mentally and reuse it.
2. The output of fetch_user_story MUST be passed as input to create_acceptance_criteria.
3. The output of create_acceptance_criteria MUST be passed to create_test_cases.
4. The outputs of fetch_user_story, create_acceptance_criteria, and create_test_cases MUST be passed to update_user_story.
5. NEVER call a tool with empty arguments unless the previous tool returned empty data.

Execution sequence:
- Call fetch_user_story
- Use its output as user_stories
- Call create_acceptance_criteria
- Use its output as acceptance_criterias
- Call create_test_cases
- Finally call update_user_story with all collected data

Do not explain.`
Do not summarize.
Do not skip steps.


"""
)
def main():
    result = agent.invoke({"messages": messages})

if __name__ == "__main__":
    main()

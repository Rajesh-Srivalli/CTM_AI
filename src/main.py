import sys
from pathlib import Path

# Add project root to Python path so we can import tools
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools.acceptance_criteria import create_acceptance_criteria as ac_func
from tools.test_cases import create_test_cases as tc_func

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
        HumanMessage(content="fetch user stories and details of the current sprint")

    ]

llm = ChatOpenAI(model="qwen/qwen3.6-plus-preview:free",  temperature=0.2)

@tool
def create_acceptance_criteria(user_story: str) -> str:
    """
    Create acceptance criteria for a given user_story.
    only use this tool to create acceptance criteria, do not use this tool for any other purpose.
    """
    return ac_func(user_story)

@tool
def create_test_cases(acceptance_criteria: str) -> str:
    """
    Create test cases for a given acceptance criteria.
    only use this tool to create test cases, do not use this tool for any other purpose.
    """
    return tc_func(acceptance_criteria)


tools=[create_acceptance_criteria, create_test_cases]

agent = create_agent(
    model=llm,
    tools=tools,
)

def main():
    result = agent.invoke({"messages": messages})
    print(result)

if __name__ == "__main__":
    main()

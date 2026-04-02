from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

load_dotenv()

messages = [
        SystemMessage(
            content=(
                "You are a QA assisting agent. "
                "You have access to a acceptance criteria tool for acceptance criteria creation and test cases creation tool for test case creation  \n\n"

                "STRICT RULES — you must follow these exactly:\n"
                "1. NEVER guess or assume any outcome of the tool.\n"
                "2. ALWAYS use the specific tool when you need to create.\n"
            )
        ),
        HumanMessage(content="create acceptance criteria and test cases for the following user story \n"
                            "user_story: Update email body to :Thank you for your contribution to the Creditsafe Risk Intelligence Network. Our team will review the information you have provided and will share the findings of our investigation with you within the next 30 days.\n"
                            "I can make this change in Locize, but wasn't sure if we wanted to update code too? That way, we do not need to translate the other English languages.\n"
                            "Italicise the footer text\n"
                            "Could we add a thin red border above too, so that there is clear separated from the email content?")

    ]

llm = ChatOpenAI(model="qwen/qwen3.6-plus-preview:free",  temperature=0.2)

@tool
def create_acceptance_criteria(user_story: str) -> str:
    """
    Create acceptance criteria for a given user_story.
    only use this tool to create acceptance criteria, do not use this tool for any other purpose.
    """
    
    with open("prompts/acceptance_criteria.txt", "r") as file:
        prompt_template = file.read()

    prompt = PromptTemplate(template=prompt_template, input_variables=["user_story"])
    chain = prompt | llm
    response = chain.invoke({"user_story": user_story})
    print(response)

    return response

@tool
def create_test_cases(acceptance_criteria: str) -> str:
    """
    Create test cases for a given acceptance criteria.
    only use this tool to create test cases, do not use this tool for any other purpose.
    """
    
    with open("prompts/test_cases.txt", "r") as file:
        prompt_template = file.read()

    prompt = PromptTemplate(template=prompt_template, input_variables=["acceptance_criteria"])
    chain = prompt | llm
    response = chain.invoke({"acceptance_criteria": acceptance_criteria})
    print(response)

    return response


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

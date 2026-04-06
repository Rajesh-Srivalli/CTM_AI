from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()
llm = ChatOpenAI(model="nvidia/nemotron-3-super-120b-a12b:free",  temperature=0.2)

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
    print("testcase",response)

    return response
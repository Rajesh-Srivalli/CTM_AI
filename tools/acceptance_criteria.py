from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
load_dotenv()
llm = ChatOpenAI(model="qwen/qwen3.6-plus-preview:free",  temperature=0.2)

def create_acceptance_criteria(user_story: str) -> str:
    
    with open("prompts/acceptance_criteria.txt", "r") as file:
        prompt_template = file.read()
    prompt = PromptTemplate(template=prompt_template, input_variables=["user_story"])
    chain = prompt | llm
    response = chain.invoke({"user_story": user_story})
    print("acceptance_criteria", response)

    return response
import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
load_dotenv()
llm = ChatOllama(model=os.getenv("LLM_MODEL"), num_ctx=2048,temperature=0)
from typing import List

def create_test_cases(acceptance_criterias: List[str]) -> List[str]:

    print("acceptance criterias", acceptance_criterias[0])
    with open("prompts/test_cases.txt", "r") as file:
        prompt_template = file.read()

    prompt = PromptTemplate(template=prompt_template, input_variables=["acceptance_criterias"])
    chain = prompt | llm
    response = chain.invoke({"acceptance_criterias": acceptance_criterias})

    return response
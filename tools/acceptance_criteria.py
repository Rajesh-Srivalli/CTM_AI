import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
load_dotenv()
llm = ChatOpenAI(model=os.getenv("LLM_MODEL"), temperature=0)
from typing import List

def create_acceptance_criteria(user_stories: List[str]) -> List[str]:
    
    with open("prompts/acceptance_criteria.txt", "r") as file:
        prompt_template = file.read()
    prompt = PromptTemplate(template=prompt_template, input_variables=["user_stories"])
    chain = prompt | llm
    response = chain.invoke({"user_stories": user_stories})

    return response
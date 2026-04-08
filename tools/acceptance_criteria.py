from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
load_dotenv()
#llm = ChatOpenAI(model="google/gemma-4-26b-a4b-it:free",  temperature=0.2)
llm = ChatOllama(model="qwen2.5:3b", temperature=0.1,num_predict=96,top_p=0.9)
from typing import List

def create_acceptance_criteria(user_stories: List[str]) -> List[str]:
    
    print("user stories", user_stories[0])
    with open("prompts/acceptance_criteria.txt", "r") as file:
        prompt_template = file.read()
    prompt = PromptTemplate(template=prompt_template, input_variables=["user_stories"])
    chain = prompt | llm
    response = chain.invoke({"user_stories": user_stories})

    return response
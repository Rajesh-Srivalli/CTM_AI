import os
from pathlib import Path
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

def create_acceptance_criteria(user_story: str) -> str:
    llm = ChatOpenAI(model="qwen/qwen3.6-plus-preview:free", temperature=0.2)

    # Get the directory of this file and construct the path to prompts
    current_dir = Path(__file__).parent.parent
    prompt_file = current_dir / "prompts" / "acceptance_criteria.txt"
    
    with open(prompt_file, "r") as file:
        prompt_template = file.read()

    prompt = PromptTemplate(template=prompt_template, input_variables=["user_story"])
    chain = prompt | llm
    response = chain.invoke({"user_story": user_story})

    return response.content

import os
from pathlib import Path
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

def create_test_cases(acceptance_criteria: str) -> str:
    llm = ChatOpenAI(model="qwen/qwen3.6-plus-preview:free", temperature=0.2)

    # Get the directory of this file and construct the path to prompts
    current_dir = Path(__file__).parent.parent
    prompt_file = current_dir / "prompts" / "test_cases.txt"
    
    with open(prompt_file, "r") as file:
        prompt_template = file.read()

    prompt = PromptTemplate(template=prompt_template, input_variables=["acceptance_criteria"])
    chain = prompt | llm
    response = chain.invoke({"acceptance_criteria": acceptance_criteria})

    return response.content

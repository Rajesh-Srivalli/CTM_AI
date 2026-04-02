from dotenv import load_dotenv
import asyncio
import sys
import os
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage


async def main():

    load_dotenv()
    llm = ChatOpenAI(model="qwen/qwen3.6-plus-preview:free", temperature=0.2)

    # Get the path to the current Python executable (venv)
    python_executable = sys.executable
    mcp_server_path = str(Path(__file__).parent.parent / "mcp_server" / "server.py")

    # connect to your MCP server using stdio transport
    client = MultiServerMCPClient(
        {
            "qa_tools": {
                "transport": "stdio",
                "command": python_executable,
                "args": [mcp_server_path],
            }
        }
    )

    # load MCP tools into LangChain
    tools = await client.get_tools()
    
    agent = create_agent(
        model=llm,
        tools=tools
    )

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

    response = await agent.ainvoke({"messages": messages})
    print(response)

if __name__ == "__main__":
    asyncio.run(main())


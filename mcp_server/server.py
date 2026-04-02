
from dotenv import load_dotenv
from fastmcp import FastMCP
from tools.acceptance_criteria import create_acceptance_criteria
from tools.test_cases import create_test_cases

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP("QA-Tools-MCP")

@mcp.tool()
def create_acceptance_criteria_tool(user_story: str) -> str:
    """
    Create acceptance criteria for a given user_story.
    only use this tool to create acceptance criteria, do not use this tool for any other purpose.
    """
    return create_acceptance_criteria(user_story)

@mcp.tool()
def create_test_cases_tool(acceptance_criteria: str) -> str:
    """
    Create test cases for a given acceptance criteria.
    only use this tool to create test cases, do not use this tool for any other purpose.
    """
    return create_test_cases(acceptance_criteria)

if __name__ == "__main__":
    # stdio transport for local agent communication
    mcp.run(transport="stdio")

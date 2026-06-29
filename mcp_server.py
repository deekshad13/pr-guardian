import os
import json
from github import Github, Auth

# MCP Server for PR Guardian
# Exposes GitHub PR fetching as an MCP tool for agent consumption

github_client = Github(auth=Auth.Token(os.environ.get("GITHUB_TOKEN")))

# MCP Tool Definition
TOOLS = [
    {
        "name": "fetch_pr_code",
        "description": "Fetch the code diff and metadata from a GitHub Pull Request",
        "input_schema": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "GitHub repo in format owner/repo e.g. pallets/flask"
                },
                "pr_number": {
                    "type": "integer",
                    "description": "The pull request number to fetch"
                }
            },
            "required": ["repo_name", "pr_number"]
        }
    }
]

def fetch_pr_code(repo_name: str, pr_number: int) -> str:
    """MCP Tool: Fetch actual code diff from a GitHub PR."""
    repo = github_client.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    code_content = f"PR Title: {pr.title}\n"
    code_content += f"PR Description: {pr.body}\n\n"
    code_content += "=== FILES CHANGED ===\n"

    for file in pr.get_files():
        code_content += f"\nFile: {file.filename}\n"
        code_content += f"Changes: +{file.additions} additions, -{file.deletions} deletions\n"
        if file.patch:
            code_content += f"Diff:\n{file.patch[:2000]}\n"

    return code_content

def handle_tool_call(tool_name: str, tool_input: dict) -> dict:
    """Route incoming MCP tool calls to the correct function."""
    if tool_name == "fetch_pr_code":
        result = fetch_pr_code(
            repo_name=tool_input["repo_name"],
            pr_number=tool_input["pr_number"]
        )
        return {"success": True, "result": result}
    else:
        return {"success": False, "error": f"Unknown tool: {tool_name}"}

def run_mcp_server():
    """
    MCP Server main loop.
    Reads JSON tool calls from stdin, returns JSON results to stdout.
    This is the standard MCP stdio transport protocol.
    """
    print(json.dumps({"status": "ready", "tools": TOOLS}))

    for line in os.sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            tool_name = request.get("tool")
            tool_input = request.get("input", {})
            response = handle_tool_call(tool_name, tool_input)
            print(json.dumps(response))
        except json.JSONDecodeError as e:
            print(json.dumps({"success": False, "error": f"Invalid JSON: {e}"}))

if __name__ == "__main__":
    run_mcp_server()
# PR Guardian
### Multi-Agent Code Review System with Adversarial Red-Teaming

PR Guardian deploys four specialized AI agents to review GitHub Pull Requests — catching security vulnerabilities and adversarial code before it reaches production.

Built for the Kaggle AI Agents: Intensive Vibe Coding Capstone 2026 — Agents for Business track.

---

## The Problem

Open source maintainers are drowning in pull requests. Popular repositories receive hundreds of PRs monthly but maintainer bandwidth has not scaled. Security vulnerabilities slip through, good PRs wait weeks, and maintainers burn out.

PR Guardian acts as an always-on senior engineering team, reviewing every PR before a human touches it.

---

## How It Works

The pipeline runs in this order:

1. GitHub PR is fetched via the MCP Server
2. Orchestrator passes the code to all three agents
3. Writer Agent reviews quality and rewrites the code
4. Reviewer Agent challenges the Writer's findings
5. Red Team Agent probes for security vulnerabilities
6. Orchestrator detects disagreement between agents
7. Either auto-approves the PR or escalates to a human

---

## The Four Agents

**Writer Agent** reviews code quality, scores it 0-10, identifies issues, and rewrites with fixes applied.

**Reviewer Agent** challenges the Writer's review, finds blind spots and missed vulnerabilities, and gives an AGREE or DISAGREE verdict.

**Red Team Agent** probes for prompt injection hidden in comments, malicious logic disguised as utility functions, and adversarial manipulation of the review pipeline.

**Orchestrator** runs the full pipeline, detects disagreement, and triggers human-in-the-loop escalation when agents cannot reach consensus.

---

## Course Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| Multi-agent system | 4 agents with A2A communication |
| MCP Server | GitHub PR fetcher as MCP tool via stdio |
| Security features | Red Team agent and prompt injection detection |
| Human-in-the-loop | Terminal escalation on agent disagreement |
| Agent Skills | Packaged reusable behaviors per agent role |

---

## Tech Stack

- Language: Python 3.11
- LLM: Groq API with llama-3.3-70b-versatile
- GitHub Integration: PyGithub
- IDE: Firebase Studio
- Protocol: MCP stdio transport

---

## Setup Instructions

Clone the repo:

    git clone https://github.com/deekshad13/pr-guardian.git
    cd pr-guardian

Install dependencies:

    pip install groq PyGithub

Set environment variables:

    export GROQ_API_KEY="your-groq-api-key"
    export GITHUB_TOKEN="your-github-token"

Test the MCP server:

    echo '{"tool": "fetch_pr_code", "input": {"repo_name": "pallets/flask", "pr_number": 6066}}' | python3 mcp_server.py

Run the full pipeline:

    python3 agents.py

---

## File Structure

- agents.py — Main multi-agent pipeline
- mcp_server.py — MCP server wrapping GitHub PR fetcher
- README.md — Project documentation

---

## Author

Deeksha D — Kaggle AI Agents Intensive Vibe Coding Capstone 2026

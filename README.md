# Aura: Autonomous Unified Risk & Audit System 🛡️

Aura is an event-driven, multi-agent AI system designed for enterprise cloud governance. It autonomously audits cloud infrastructure deployments against complex compliance frameworks (SOC2, GDPR) using a **hybrid GraphRAG** pipeline, and safely generates remediation code via a **Model Context Protocol (MCP)** gateway.

![Aura Architecture](https://img.shields.io/badge/Architecture-Event--Driven_Swarm-indigo)
![Tech Stack](https://img.shields.io/badge/Stack-FastAPI_%7C_Next.js_%7C_Neo4j_%7C_pgvector-blue)
![AI Orchestration](https://img.shields.io/badge/AI-LangGraph_%7C_MCP-emerald)

## 🌟 The Problem it Solves
In large enterprises, AI agents are often given too much direct access or lack deterministic knowledge of corporate policies. Aura solves this by introducing:
1. **GraphRAG (Neo4j + pgvector):** Eliminates AI hallucinations by mapping cloud resources to exact regulatory policies using deterministic graph relationships combined with semantic vector search.
2. **Secure MCP Gateway:** AI agents do not have direct access to AWS or Jira. They must request actions through a heavily restricted, auditable Model Context Protocol (MCP) server.
3. **LangGraph Swarms:** Moves beyond "chat" interfaces. Aura is an autonomous background swarm that wakes up via webhooks, investigates, audits, and writes Infrastructure-as-Code (IaC) fixes without human intervention.

## 🏗️ Architecture

```text
[Cloud Event Webhook] ➔ [FastAPI Backend] ➔ [LangGraph Agent Swarm]
                                                     ⬍
                                              [MCP Gateway]
                                              ⬢           ⬢
                                     [GraphRAG DB]     [AWS / Jira]
                                   (Neo4j + pgvector)
```

### The AI Swarm (LangGraph Nodes)
*   🕵️ **Investigator Agent:** Uses MCP tools to securely fetch the current state of newly deployed cloud infrastructure (e.g., an S3 bucket).
*   📋 **Compliance Agent:** Queries the GraphRAG pipeline to find which laws govern the resource and determines if the current state violates policy.
*   🛠️ **Remediation Agent:** Automatically drafts the exact Terraform/IaC script required to fix the compliance violation.
*   📝 **Reporter Agent:** Uses MCP tools to securely open a Jira ticket containing the audit trail and the generated code fix.

## 🚀 Tech Stack

*   **Frontend:** Next.js, React, Tailwind CSS
*   **Backend:** Python, FastAPI, LangGraph, LangChain
*   **Database (GraphRAG):** Neo4j (Knowledge Graph), PostgreSQL + pgvector (Semantic Search)
*   **Integration:** Model Context Protocol (MCP)
*   **Infrastructure:** Docker Compose

## 💻 Local Setup & Installation

### Prerequisites
*   Docker & Docker Compose
*   Python 3.11+
*   Node.js 18+

### 1. Boot up the Databases (GraphRAG)
```bash
docker-compose up -d
```
*This starts Neo4j, PostgreSQL (with pgvector), and Redis.*

### 2. Start the FastAPI AI Backend
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # On Windows
pip install -r requirements.txt
python seed_data.py           # Injects mock SOC2/GDPR policies into the GraphRAG
uvicorn main:app --reload     # Starts API on http://localhost:8000
```

### 3. Start the Next.js Dashboard
```bash
cd frontend
npm install
npm run dev                   # Starts UI on http://localhost:3000
```

## 🎯 Usage
1. Navigate to `http://localhost:3000`.
2. Click **"Simulate AWS Deployment"** to send a mock `s3:CreateBucket` webhook to the backend.
3. Watch the UI populate with the live LangGraph swarm's thought process, the compliance audit results, and the generated Terraform remediation code.

## 💼 Built for Enterprise
This project was architected specifically to demonstrate enterprise-grade AI integration, focusing on **Trust, Security, and Explainability**, making it highly relevant for Cloud Security and Risk Consulting architectures.

# Product Requirements Document (PRD)
**Project Name:** Aura (Autonomous Unified Risk & Audit System)
**Target Audience:** PwC / Big 4 Technical Interviews (Cloud, AI, Enterprise Risk)

---

## 1. Executive Summary
**Aura** is an event-driven, multi-agent Cloud Governance and Audit system. It leverages a hybrid GraphRAG (Neo4j + pgvector) database to understand complex enterprise compliance policies (like SOC2, GDPR). Using a Model Context Protocol (MCP) gateway for secure, permissioned data access, a LangGraph agent swarm autonomously investigates cloud infrastructure deployments, identifies compliance violations, and generates remediation code.

**The "PwC" Value Proposition:** Moving AI from a "chat" interface to a secure, autonomous auditor that respects enterprise data boundaries and provides transparent, actionable risk mitigation.

---

## 2. System Architecture

### 2.1 Tech Stack
*   **Frontend:** Next.js (React), Tailwind CSS, Zustand (State Management).
*   **API Gateway & Swarm:** Python (FastAPI), LangGraph, LangChain.
*   **Message Broker / Queues:** Redis (via Celery or BullMQ) for asynchronous agent event handling.
*   **Database (GraphRAG):** 
    *   **Neo4j:** Stores the Knowledge Graph (Entities: Servers, Databases, Policies, PII).
    *   **PostgreSQL (pgvector):** Stores semantic embeddings of the actual compliance text.
*   **Integration Layer:** MCP (Model Context Protocol) Server for secure agent tool execution.
*   **Infrastructure/Cloud:** Docker, LocalStack (to simulate AWS environments safely/free).

### 2.2 High-Level Diagram
`Cloud Event (Webhook)` ➔ `Redis Queue` ➔ `LangGraph Swarm`
                                                 ⬍
                                            `MCP Gateway`
                                            ⬢       ⬢
                                     `GraphRAG`   `Mock AWS/Jira`

---

## 3. Core Workflows

### Workflow 1: Compliance Ingestion (GraphRAG)
1. System ingests PDF/Markdown documents of mock compliance policies (e.g., "All S3 buckets containing PII must be encrypted").
2. LLM extracts entities (Data Types, Infrastructure components) and relationships (`GOVERNS`, `CONTAINS`, `REQUIRES`).
3. Graph relationships are stored in Neo4j; semantic text is embedded into pgvector.

### Workflow 2: Event-Driven Audit
1. A mock webhook fires simulating a cloud deployment (e.g., "Terraform script deployed new S3 bucket: `user-data-bucket` with encryption=false").
2. The LangGraph swarm wakes up.
    *   **Investigator Agent:** Uses the MCP Gateway to "query" the mock AWS environment and gather bucket metadata.
    *   **Compliance Agent:** Queries the GraphRAG pipeline: *"What policies apply to `user-data-bucket`?"* The Graph returns the exact rule that PII buckets must be encrypted.
    *   **Remediation Agent:** Generates the Terraform/Python script to fix the encryption flag.
    *   **Reporter Agent:** Uses MCP to create a mock Jira ticket and logs the entire thought process for the audit trail.

### Workflow 3: Enterprise Dashboard
1. A Next.js frontend visualizes the live LangGraph swarm state (showing which agent is currently "thinking").
2. Displays the Neo4j Graph visualization of the infrastructure vs. compliance policies.
3. Shows an "Audit Log" of all actions taken by the agents through the MCP Gateway.

---

## 4. Implementation Plan (Execution Phases)

### Phase 1: Infrastructure & Scaffolding
*   [ ] Set up Docker Compose (`postgres` with `pgvector`, `neo4j`, `redis`).
*   [ ] Initialize Next.js frontend application.
*   [ ] Initialize Python FastAPI backend application.

### Phase 2: GraphRAG Data Pipeline
*   [ ] Write scripts to parse sample Markdown compliance policies.
*   [ ] Set up LLM extraction to generate Neo4j Cypher queries.
*   [ ] Set up vector embeddings insertion into pgvector.
*   [ ] Create API endpoint to test hybrid querying (Vector search + Graph traversal).

### Phase 3: The Secure MCP Gateway
*   [ ] Implement a lightweight MCP Server (Python or Node.js).
*   [ ] Create mocked tools exposed via MCP:
    *   `get_aws_resource_status(resource_id)`
    *   `create_jira_ticket(title, description)`
*   [ ] Connect FastAPI backend to communicate with the MCP Server.

### Phase 4: LangGraph Swarm Orchestration
*   [ ] Define LangGraph nodes (Investigator, Compliance, Remediation, Reporter).
*   [ ] Define edges and conditional routing (e.g., if Compliance says "Pass", skip Remediation).
*   [ ] Connect the Swarm to the MCP tools and the GraphRAG query endpoint.
*   [ ] Wrap the Swarm trigger in a FastAPI endpoint / Redis worker.

### Phase 5: Dashboard & Polish
*   [ ] Build the Next.js UI to trigger the mock webhook.
*   [ ] Poll or WebSocket stream the LangGraph state to the UI.
*   [ ] Render the Audit Trail and Remediation Code blocks in the browser.

---

## 5. PwC Interview Talking Points
*   **"Trust by Design":** Emphasize the MCP gateway. "Agents shouldn't have raw DB credentials. MCP creates an auditable, rate-limited choke point."
*   **"Explainable AI":** Emphasize GraphRAG. "Standard RAG hallucinates. GraphRAG provides deterministic, traceable links between an infrastructure component and the exact regulatory paragraph that governs it."
*   **"Actionable AI":** Emphasize the Swarm. "Dashboards that show red alerts cause alert fatigue. Aura doesn't just flag the issue; it drafts the exact infrastructure-as-code fix and opens the ticket."
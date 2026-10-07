# 🛡️ GraphQL Sentinel

### AI-Powered Runtime Security Gateway for GraphQL APIs

[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-Dashboard-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![GraphQL](https://img.shields.io/badge/GraphQL-Security-E10098?logo=graphql&logoColor=white)](https://graphql.org/)
[![Security](https://img.shields.io/badge/Focus-API%20Security-critical?logo=shield&logoColor=white)](#security-model)

> **Detect. Explain. Score. Protect.**
>
> GraphQL Sentinel is an intelligent security gateway designed to detect, analyze, explain, and mitigate malicious or abnormal GraphQL operations in real time.

---

## ✨ Why GraphQL Sentinel?

GraphQL gives clients enormous flexibility, but that flexibility creates a unique security surface.

A single GraphQL request can:

- Traverse deeply nested relationships
- Request hundreds of fields
- Abuse aliases and fragments
- Enumerate an entire schema
- Trigger expensive resolver chains
- Consume excessive server resources
- Exploit weak authorization boundaries
- Generate abnormal traffic patterns
- Bypass traditional endpoint-based security assumptions

Traditional API security tools often treat:

```text
POST /graphql
```

as a single endpoint.

GraphQL Sentinel treats the **operation itself as the security boundary**.

Instead of asking only:

> "Is this request going to `/graphql`?"

Sentinel asks:

> **"What is this GraphQL operation trying to do, how expensive is it, how does it compare with normal behavior, and should it be allowed to execute?"**

---

# 🎯 Core Concept

GraphQL Sentinel combines **deterministic security rules**, **GraphQL AST analysis**, **behavioral anomaly detection**, and **risk-based decision making**.

```text
                       ┌─────────────────┐
                       │ GraphQL Client  │
                       └────────┬────────┘
                                │
                                ▼
                    ┌──────────────────────┐
                    │  GraphQL Sentinel    │
                    │   Security Gateway   │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       AST Analyzer      Threat Engine     Identity Engine
             │                 │                 │
       Depth Analysis     Rule Detection     API Identity
       Complexity          ML Detection       Reputation
       Alias Abuse         Behavioral         Rate Limits
       Fragments           Analysis
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                     ┌────────────────────┐
                     │   Risk Aggregator  │
                     │      0 - 100       │
                     └─────────┬──────────┘
                               │
                  ┌────────────┼────────────┐
                  ▼            ▼            ▼
                ALLOW        THROTTLE      BLOCK
                  │            │            │
                  └────────────┼────────────┘
                               ▼
                     ┌─────────────────┐
                     │ GraphQL Server  │
                     └─────────────────┘
```

---

# 🚀 Features

## 🔍 GraphQL AST Security Analysis

Every GraphQL operation can be analyzed before execution.

Sentinel extracts security-relevant features such as:

- Query depth
- Query complexity
- Field count
- Unique field count
- Alias count
- Fragment count
- Fragment depth
- Argument count
- Mutation ratio
- Introspection usage
- Nested relationship depth
- Potentially expensive operations
- Suspicious query structures

Example:

```graphql
query {
  users {
    posts {
      comments {
        author {
          posts {
            comments {
              author {
                posts {
                  id
                }
              }
            }
          }
        }
      }
    }
  }
}
```

Sentinel can transform this into a security profile:

```text
Query Analysis
────────────────────────────
Depth:              9
Fields:             14
Complexity:         847
Nested Relations:   8
Fragments:          0
Aliases:            0
Introspection:      false

Risk: HIGH
```

---

# 🧠 Hybrid Threat Detection

GraphQL Sentinel is designed around a hybrid detection model.

Instead of relying entirely on machine learning:

```text
                 Incoming Operation
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
       Rule-Based Engine       ML Detection
             │                       │
       Deterministic             Behavioral
       Detection                 Detection
             │                       │
             └───────────┬───────────┘
                         ▼
                  Risk Aggregator
                         │
                         ▼
                  Security Decision
```

### Deterministic detection

Useful for known security conditions:

- Excessive query depth
- Excessive complexity
- Introspection restrictions
- Rate-limit violations
- Alias abuse
- Batch abuse
- Suspicious mutations
- Policy violations

### Behavioral detection

Useful for previously unknown or evolving behavior:

- Unusual query patterns
- Abnormal request frequency
- Sudden complexity changes
- User-specific behavioral deviations
- API-key behavioral anomalies
- Traffic spikes
- Previously unseen operation structures

---

# 📊 Risk Scoring

Every request can receive a normalized risk score:

```text
0 ───────────────────────────────────── 100
│                    │                  │
SAFE               SUSPICIOUS          CRITICAL
```

Example:

```text
┌─────────────────────────────────────────┐
│             SECURITY DECISION           │
├─────────────────────────────────────────┤
│                                         │
│ Risk Score                 94 / 100     │
│ Confidence                  97%          │
│                                         │
│ Query Depth                 +31          │
│ Complexity                  +28          │
│ Behavioral Anomaly          +19          │
│ Rate Anomaly                +16          │
│                                         │
│ Decision                    BLOCK        │
│ Policy                      HIGH_RISK    │
│                                         │
└─────────────────────────────────────────┘
```

The scoring system is designed to make security decisions **explainable rather than opaque**.

---

# 🔬 Behavioral Baselines

One of the key ideas behind Sentinel is that malicious behavior isn't always defined by a static rule.

A query can be technically valid while still being suspicious.

For example, an application normally produces:

```text
Query depth:        2–4
Complexity:         20–120
Requests/minute:    5–20
Mutations:          <5%
Introspection:      0%
```

A sudden pattern like:

```text
Query depth:        11
Complexity:         1,900
Requests/minute:    420
Mutations:          41%
Introspection:      27%
```

can trigger a behavioral anomaly even when no single rule is violated.

This enables Sentinel to detect:

> **"This operation is abnormal for this actor."**

rather than only:

> **"This operation matches a known attack."**

---

# 🛡️ Threat Classes

GraphQL Sentinel is designed to detect and mitigate multiple classes of GraphQL abuse.

### Query Abuse

- Excessive query depth
- Excessive query complexity
- Nested relationship abuse
- Large field selections
- Fragment explosion
- Alias abuse

### Schema Abuse

- Introspection abuse
- Schema enumeration
- Sensitive field discovery
- Deprecated field probing
- Unauthorized operation discovery

### Resource Exhaustion

- Query-based DoS
- Expensive resolver traversal
- Excessive pagination
- Large list arguments
- Batch query abuse
- High-frequency requests

### Behavioral Threats

- Abnormal user behavior
- Abnormal API-key behavior
- Sudden traffic changes
- Query pattern anomalies
- Repeated suspicious operations

### Authorization Signals

Sentinel can surface suspicious authorization-related behavior for further investigation, while authorization itself should remain enforced by the underlying application.

---

# ⚙️ Policy Engine

Security policies should be configurable rather than hard-coded.

Example:

```yaml
policies:

  max_query_depth:
    value: 7
    action: block

  max_complexity:
    value: 500
    action: block

  introspection:
    production: false
    action: block

  max_requests_per_minute:
    value: 120
    action: throttle

  suspicious_score:
    threshold: 80
    action: block
```

This allows teams to adapt Sentinel to their own API architecture.

---

# 🚦 Adaptive Decisions

Sentinel can classify requests into three primary actions:

### 🟢 ALLOW

The request is considered safe.

```text
Risk: 12
Action: ALLOW
```

### 🟡 THROTTLE

The request is suspicious but does not necessarily justify an immediate block.

```text
Risk: 67
Action: THROTTLE
```

### 🔴 BLOCK

The request crosses a configured security threshold.

```text
Risk: 94
Action: BLOCK
```

This makes Sentinel suitable for both:

- Monitoring mode
- Enforcement mode

---

# 🔌 GraphQL Security Gateway

The long-term goal of Sentinel is to operate as a drop-in security layer:

```text
                Client
                  │
                  ▼
        ┌─────────────────────┐
        │  GraphQL Sentinel   │
        │     Gateway         │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Existing GraphQL    │
        │       API           │
        └─────────────────────┘
```

Example:

```text
Client
  ↓
http://localhost:8080/graphql
  ↓
GraphQL Sentinel
  ↓
http://graphql-api:4000/graphql
```

This allows security controls to be introduced without rewriting the application itself.

---

# 🧪 Attack Simulation Lab

Sentinel can include a controlled security testing environment for development and demonstrations.

Example attack scenarios:

```text
┌─────────────────────────────────────┐
│          GRAPHQL ATTACK LAB         │
├─────────────────────────────────────┤
│                                     │
│  [ Query Depth Attack ]             │
│  [ Complexity Attack ]              │
│  [ Introspection Abuse ]            │
│  [ Alias Abuse ]                    │
│  [ Batch Abuse ]                    │
│  [ Rate Limit Attack ]              │
│                                     │
└─────────────────────────────────────┘
```

A simulated attack should produce an end-to-end result:

```text
Attack
  ↓
GraphQL Request
  ↓
AST Analysis
  ↓
Threat Detection
  ↓
Risk Score
  ↓
Security Policy
  ↓
BLOCK
  ↓
Evidence + Explanation
```

> ⚠️ Attack simulations should only be performed against systems you own or are explicitly authorized to test.

---

# 🧾 Explainable Security Decisions

A security system should not simply say:

```text
BLOCKED
```

It should explain **why**.

Example:

```text
Request #8F12A

Decision: BLOCK
Risk: 94/100
Confidence: 97%

Triggered signals:

🔴 Excessive query depth
   Depth = 11
   Threshold = 7

🔴 Excessive complexity
   Complexity = 924
   Threshold = 500

🟠 Behavioral anomaly
   8.7x above normal complexity

🟠 Rate anomaly
   4.2x above baseline

Policy:
HIGH_RISK_QUERY

Action:
BLOCK
```

This is particularly useful for:

- Security analysts
- Developers
- Incident response
- Debugging
- Compliance
- Security demonstrations

---

# 🖥️ Security Dashboard

The web dashboard is designed to provide real-time visibility into GraphQL security.

### Overview

```text
┌────────────────┬────────────────┬────────────────┐
│ Requests       │ Threats        │ Blocked        │
│ 1.24M          │ 3,842          │ 1,291          │
└────────────────┴────────────────┴────────────────┘
```

### Security Timeline

```text
Requests
  │
  │          ╭──────╮
  │     ╭────╯      ╰──────╮
  │─────╯                   ╰────
  └────────────────────────────────
              Time
```

### Threat Distribution

```text
Query DoS             ██████████████ 42%
Introspection         ███████        21%
Behavioral Anomaly    █████          17%
Alias Abuse           ███             9%
Other                 ███            11%
```

### Useful dashboard views

- Real-time request stream
- Threat timeline
- Risk distribution
- Blocked operations
- Top suspicious actors
- API-key activity
- Query complexity trends
- Query-depth trends
- Security events
- Model predictions
- Detection explanations
- System health

---

# 🔍 Schema Security Scanner

A future Sentinel scanner can analyze a GraphQL schema before deployment.

Example:

```bash
sentinel scan schema.graphql
```

Example output:

```text
GraphQL Sentinel Schema Scanner
────────────────────────────────────

Schema: api.graphql

✓ Authentication analysis
✓ Query complexity analysis
✓ Mutation analysis
✓ Introspection analysis
✓ Recursive relationship analysis

Security Score: 82 / 100

CRITICAL   2
HIGH       5
MEDIUM     8
LOW        3
```

Example findings:

```text
HIGH
Mutation has no visible authorization policy

HIGH
Recursive relationship may permit expensive traversal

MEDIUM
Introspection enabled in production configuration

MEDIUM
Unrestricted pagination argument detected
```

---

# 🧰 CLI

A dedicated CLI makes Sentinel useful outside the dashboard.

Potential commands:

```bash
sentinel scan schema.graphql
```

```bash
sentinel proxy \
  --target http://localhost:4000/graphql \
  --port 8080
```

```bash
sentinel analyze request.json
```

```bash
sentinel replay attack.json
```

```bash
sentinel report --format json
```

---

# 📈 Security Metrics

Sentinel should measure more than "number of attacks."

Recommended metrics include:

| Metric | Description |
|---|---|
| Detection Rate | Percentage of malicious operations detected |
| Precision | Percentage of alerts that are actually malicious |
| Recall | Percentage of malicious operations detected |
| F1 Score | Combined precision/recall measure |
| False Positive Rate | Safe requests incorrectly flagged |
| P50 Latency | Median analysis latency |
| P95 Latency | 95th percentile analysis latency |
| P99 Latency | 99th percentile analysis latency |
| Requests/sec | Gateway throughput |
| Block Rate | Percentage of requests blocked |
| Risk Accuracy | Quality of risk classification |

> Do not publish benchmark numbers until they have been measured against a reproducible test dataset.

---

# 🧪 Benchmarking

A reproducible benchmark dataset can contain:

```text
Normal Queries             100,000
Depth Attacks               10,000
Complexity Attacks          10,000
Introspection Attacks       10,000
Alias Abuse                 10,000
Batch Abuse                 10,000
Behavioral Anomalies        10,000
```

The benchmark pipeline:

```text
Dataset
   ↓
Feature Extraction
   ↓
Rule Engine
   ↓
ML Engine
   ↓
Risk Aggregator
   ↓
Predictions
   ↓
Precision / Recall / F1
   ↓
Latency Benchmark
```

The goal is to make performance and detection claims **measurable and reproducible**.

---

# 🔭 Observability

For production environments, Sentinel should expose observability signals through standard tooling.

```text
                GraphQL Sentinel
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
        Logs        Metrics       Traces
          │            │            │
          └────────────┼────────────┘
                       ▼
                OpenTelemetry
                       │
              ┌────────┴────────┐
              ▼                 ▼
          Prometheus          Grafana
```

Useful operational metrics:

```text
sentinel_requests_total
sentinel_blocked_requests_total
sentinel_detection_latency_seconds
sentinel_risk_score
sentinel_query_complexity
sentinel_query_depth
sentinel_anomaly_score
sentinel_gateway_errors_total
```

---

# 🏗️ Architecture

A production-oriented architecture can be organized as:

```text
graphQL-sentinel/
│
├── backend/
│   ├── api/
│   ├── gateway/
│   ├── analyzer/
│   ├── detection/
│   ├── policies/
│   ├── scoring/
│   ├── models/
│   ├── storage/
│   └── services/
│
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── charts/
│   ├── security/
│   └── dashboard/
│
├── ml/
│   ├── datasets/
│   ├── training/
│   ├── evaluation/
│   ├── models/
│   └── notebooks/
│
├── attacks/
│   ├── depth/
│   ├── complexity/
│   ├── introspection/
│   ├── aliases/
│   └── batch/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── security/
│   └── benchmark/
│
├── docker/
│
├── docs/
│
├── scripts/
│
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── README.md
```

---

# 🧩 Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- GraphQL parsing / AST tooling
- Async HTTP stack
- Machine-learning inference

## Frontend

- React
- TypeScript
- Modern dashboard components
- Interactive charts
- Real-time security events

## Machine Learning

Potential components include:

- Autoencoder-based anomaly detection
- Random Forest / tree-based classification
- Ensemble scoring
- Behavioral baselines
- Feature normalization
- Model evaluation

## Infrastructure

- Docker
- Docker Compose
- CI/CD
- REST APIs
- GraphQL
- OpenTelemetry
- Prometheus
- Grafana

---

# 🔐 Security Model

GraphQL Sentinel follows a defense-in-depth model:

```text
                    Security
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
      Rules            ML         Behavioral
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                 Risk Scoring
                       │
                       ▼
              Policy Enforcement
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
            Allow    Throttle   Block
```

Sentinel should complement—not replace:

- Authentication
- Authorization
- Secure resolver implementation
- Input validation
- Database security
- Secrets management
- TLS
- Network controls
- Application-level security

---

# 🚀 Quick Start

## Prerequisites

Make sure you have:

- Python 3.11+
- Node.js 18+
- npm
- Docker
- Docker Compose
- Git

---

## Clone the repository

```bash
git clone https://github.com/satyamshrivastav955-dotcom/GraphQL-Sentinel.git

cd GraphQL-Sentinel
```

---

## Backend

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

The development dashboard should then be available at:

```text
http://localhost:3000
```

> Adjust the commands above to match the actual project entry points if the repository uses different paths/scripts.

---

# 🐳 Docker

Build the project:

```bash
docker compose build
```

Start the stack:

```bash
docker compose up
```

Run in detached mode:

```bash
docker compose up -d
```

Stop:

```bash
docker compose down
```

---

# ⚡ Example Request

A normal GraphQL request:

```graphql
query GetUser {
  user(id: "123") {
    id
    name
    email
  }
}
```

might produce:

```json
{
  "decision": "allow",
  "risk_score": 8,
  "confidence": 0.98,
  "query_depth": 2,
  "complexity": 24
}
```

A suspicious operation:

```graphql
query {
  users {
    posts {
      comments {
        author {
          posts {
            comments {
              author {
                posts {
                  comments {
                    id
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

could produce:

```json
{
  "decision": "block",
  "risk_score": 94,
  "confidence": 0.97,
  "query_depth": 11,
  "complexity": 924,
  "reasons": [
    "excessive_query_depth",
    "high_query_complexity",
    "behavioral_anomaly"
  ]
}
```

---

# 📚 API

Example endpoints:

```text
GET    /health
GET    /metrics

POST   /analyze
POST   /graphql

GET    /security/events
GET    /security/events/{id}

GET    /security/stats
GET    /security/threats

POST   /policies/validate
GET    /policies

POST   /schema/scan
POST   /replay
```

> Keep this section synchronized with the actual routes implemented in the project.

---

# 🧪 Testing

Run unit tests:

```bash
pytest
```

Run security tests:

```bash
pytest tests/security
```

Run integration tests:

```bash
pytest tests/integration
```

Run with coverage:

```bash
pytest --cov
```

---

# 🧠 ML Pipeline

The ML pipeline follows:

```text
GraphQL Request
      │
      ▼
AST Parsing
      │
      ▼
Feature Extraction
      │
      ├── Depth
      ├── Complexity
      ├── Field Count
      ├── Alias Count
      ├── Fragment Count
      ├── Mutation Ratio
      └── Behavioral Features
      │
      ▼
Feature Normalization
      │
      ▼
ML Models
      │
      ├── Anomaly Detection
      └── Classification
      │
      ▼
Model Scores
      │
      ▼
Risk Aggregator
      │
      ▼
Security Decision
```

---

# 🔬 Explainability

Machine-learning predictions should be accompanied by interpretable signals.

Instead of:

```text
Prediction = malicious
```

Sentinel should expose:

```text
Prediction: MALICIOUS

Top contributing signals:

1. Query complexity
2. Query depth
3. Request frequency
4. Behavioral deviation
5. Operation structure
```

This improves trust and makes the system easier to debug.

---

# 📦 Deployment

A production deployment can look like:

```text
                       Internet
                           │
                           ▼
                     Load Balancer
                           │
                           ▼
                ┌────────────────────┐
                │ GraphQL Sentinel   │
                │     Gateway        │
                └─────────┬──────────┘
                          │
                 ┌────────┴────────┐
                 ▼                 ▼
          GraphQL API         Observability
                 │                 │
                 ▼          ┌──────┴──────┐
             Database       ▼             ▼
                         Metrics        Logs
```

For horizontal scaling:

```text
                 Load Balancer
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
    Sentinel-1    Sentinel-2    Sentinel-3
        │             │             │
        └─────────────┼─────────────┘
                      ▼
              Shared State Store
```

---

# 📋 Roadmap

## Phase 1 — GraphQL Security Core

- [x] GraphQL request analysis
- [x] Security API
- [x] Dashboard foundation
- [ ] AST security analyzer
- [ ] Query complexity engine
- [ ] Query depth enforcement
- [ ] Introspection controls
- [ ] Alias detection
- [ ] Fragment analysis

## Phase 2 — Detection Engine

- [ ] Hybrid rule + ML engine
- [ ] Behavioral baselines
- [ ] Risk scoring
- [ ] Explainable predictions
- [ ] Threat classification
- [ ] False-positive tracking

## Phase 3 — Gateway

- [ ] Reverse proxy
- [ ] Allow / throttle / block
- [ ] Policy-as-code
- [ ] API-key identity
- [ ] Rate limiting
- [ ] Persistent security events

## Phase 4 — Developer Tooling

- [ ] CLI
- [ ] Schema scanner
- [ ] Attack replay
- [ ] Security reports
- [ ] Python SDK
- [ ] TypeScript SDK

## Phase 5 — Production

- [ ] OpenTelemetry
- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] Distributed deployment
- [ ] Performance benchmarks
- [ ] Security regression suite
- [ ] Container hardening
- [ ] SBOM generation

---

# 🏆 Project Goals

GraphQL Sentinel aims to become:

### For developers

A simple way to add GraphQL security controls without rewriting their API.

### For security teams

A source of actionable GraphQL security events and behavioral intelligence.

### For researchers

A platform for experimenting with GraphQL anomaly detection and security models.

### For DevOps teams

A deployable gateway with metrics, logging, policy enforcement, and observability.

---

# 📊 What Makes Sentinel Different?

Traditional API security often focuses on:

```text
IP
│
├── Request
├── Endpoint
└── HTTP metadata
```

GraphQL Sentinel focuses on:

```text
Request
   │
   ▼
GraphQL Operation
   │
   ├── AST Structure
   ├── Query Depth
   ├── Complexity
   ├── Fields
   ├── Aliases
   ├── Fragments
   ├── Identity
   ├── Frequency
   └── Behavioral History
          │
          ▼
      Risk Score
          │
          ▼
       Decision
```

The objective is to understand **what the API request is actually doing**, not merely where it was sent.

---

# 🔒 Responsible Security

GraphQL Sentinel is intended for:

- Defensive security
- Authorized penetration testing
- Security research
- API hardening
- Development environments
- Security education

Never use the project against systems you do not own or have explicit authorization to test.

The attack simulation and replay features should only target controlled environments.

---

# 🤝 Contributing

Contributions are welcome.

A typical workflow:

```bash
git checkout -b feature/my-feature
```

Make your changes, then run:

```bash
pytest
```

and:

```bash
npm test
```

where applicable.

Commit:

```bash
git commit -m "feat: add query complexity detection"
```

Push:

```bash
git push origin feature/my-feature
```

Then open a pull request.

### Good first contributions

- Add GraphQL security rules
- Improve AST feature extraction
- Add test cases
- Improve dashboard visualizations
- Add benchmark datasets
- Improve documentation
- Add integrations
- Improve model explainability

---

# 🐛 Reporting Security Issues

Please do not publicly disclose sensitive vulnerabilities before they have been responsibly reported and assessed.

For security-sensitive issues, use the project's private security reporting mechanism where available.

---

# 📄 License

This project is distributed under the license specified in the repository's `LICENSE` file.

---

# 👨‍💻 Author

### Satyam Shrivastav

Engineering Student & Developer

Building:

> **GraphQL Sentinel — intelligent runtime security for GraphQL APIs.**

GitHub:

**[satyamshrivastav955-dotcom](https://github.com/satyamshrivastav955-dotcom)**

Project:

**[GraphQL-Sentinel](https://github.com/satyamshrivastav955-dotcom/GraphQL-Sentinel)**

---

# ⭐ Support the Project

If GraphQL Sentinel is useful to you:

- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 🔐 Contribute security rules
- 🧪 Contribute test cases
- 📚 Improve documentation
- 🚀 Submit pull requests

---

# 🛡️ GraphQL Sentinel

### Detect. Explain. Score. Protect.

```text
                 ┌─────────────────────┐
                 │    GRAPHQL QUERY    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    AST ANALYSIS     │
                 └──────────┬──────────┘
                            │
                  ┌─────────┴─────────┐
                  ▼                   ▼
             RULE ENGINE          ML ENGINE
                  │                   │
                  └─────────┬─────────┘
                            ▼
                     RISK SCORING
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
           ALLOW         THROTTLE        BLOCK
                            │
                            ▼
                     SECURITY EVENT
                            │
                            ▼
                       DASHBOARD
```

> **GraphQL Sentinel turns GraphQL security from endpoint protection into operation-level intelligence.**

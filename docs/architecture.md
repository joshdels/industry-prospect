# Architecture

Industry Prospect is designed as a **Django-centered application** with a small number of focused components.

The architecture prioritizes simplicity: the application should make it easy to capture prospect information, enrich it with AI, generate discovery-oriented outreach, and learn from conversations without becoming a full CRM.

---

## Architecture Overview

```text
                         ┌─────────────────────┐
                         │       User          │
                         │                     │
                         │ Prospect information│
                         │ Conversation results│
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Django Web App    │
                         │                     │
                         │ Insert              │
                         │ Prospect Bank       │
                         │ Dashboard           │
                         │ Outreach            │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
             ┌────────────┐  ┌─────────────┐  ┌─────────────┐
             │   Models   │  │  Services   │  │    Tasks    │
             │            │  │             │  │             │
             │ Prospects  │  │ AI Analysis │  │   Celery    │
             │ Industries │  │ Outreach    │  │ Background  │
             │ Tags       │  │ Learning    │  │ Processing  │
             └─────┬──────┘  └──────┬──────┘  └──────┬──────┘
                   │                │                │
                   └────────────────┼────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    PostgreSQL       │
                         │                     │
                         │ Prospect data       │
                         │ Industry / Tags     │
                         │ Outcomes / Lessons  │
                         └─────────────────────┘


                         ┌─────────────────────┐
                         │     MCP Server      │
                         │                     │
                         │ AI-facing tools     │
                         │ Prospect tools      │
                         │ Analysis tools      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      AI Client      │
                         │                     │
                         │ Claude / MCP client │
                         └─────────────────────┘
```

---

# Architectural Principles

## 1. Django Is the Core

Django is the center of the application.

The database models, business logic, authentication, admin interface, web views, and application workflows remain inside the Django project.

The goal is to avoid splitting the application into unnecessary microservices.

```text
Django
├── Models
├── Views
├── Services
├── Tasks
├── Admin
└── MCP integration
```

This keeps development and deployment relatively simple.

---

## 2. Services Contain Business Logic

Business logic should not be scattered throughout views, MCP tools, or model methods.

Instead, reusable operations belong in service modules.

For example:

```text
apps/
└── inspector/
    ├── models/
    ├── services/
    │   ├── prospect.py
    │   ├── analysis.py
    │   ├── outreach.py
    │   └── learning.py
    └── ...
```

A service should represent an application operation.

For example:

```python
create_prospect_from_analysis(...)
```

The same service can then be called from:

* Django views
* Celery tasks
* MCP tools
* Management commands
* Tests

This prevents duplicated business logic.

---

# Application Layers

The application can be thought of as four primary layers.

```text
┌──────────────────────────────────────┐
│             Interfaces               │
│                                      │
│ Django UI / Admin / MCP              │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│             Services                 │
│                                      │
│ Analysis / Outreach / Learning       │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│               Models                 │
│                                      │
│ Prospect / Industry / Tag / Outcome  │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│             PostgreSQL               │
└──────────────────────────────────────┘
```

---

# 1. Interface Layer

The interface layer is how users and AI clients interact with the system.

### Django UI

The web application provides the primary human interface.

Current areas include:

```text
Insert
Prospect Bank
Dashboard
Outreach
```

The UI should remain relatively thin.

It collects input, displays information, and calls application services.

---

### MCP

The MCP server provides an AI-facing interface to the application.

```text
Claude
   │
   │ MCP
   ▼
MCP Server
   │
   ▼
Django Services
   │
   ▼
Database
```

MCP tools should not contain the application's core business logic.

Instead, they should translate an AI request into a call to an existing service.

For example:

```python
@mcp.tool()
def analyze_prospect(prospect_id):
    return analyze_prospect_service(prospect_id)
```

This keeps the MCP layer thin and makes the same functionality usable from the Django application.

---

# 2. Service Layer

The service layer contains the application's business operations.

Potential responsibilities include:

### Prospect Services

```text
Create prospect
Update prospect
Change prospect status
Retrieve pending prospects
```

### Analysis Services

```text
Analyze raw prospect information
Extract company
Identify industry
Extract useful context
Generate structured notes
```

### Outreach Services

```text
Generate discovery questions
Generate outreach message
Use prospect context
Apply the three core questions
```

### Learning Services

```text
Record conversation outcome
Record lessons learned
Identify successful patterns
Identify unsuccessful approaches
```

The service layer is where the application's actual workflow should live.

---

# 3. Data Layer

PostgreSQL stores the persistent application data.

The database represents the prospect intelligence accumulated by the system.

A simplified relationship looks like:

```text
                    ┌──────────────┐
                    │   Prospect   │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────────┐
        │ Industry │ │   Tags   │ │ Conversations│
        └──────────┘ └──────────┘ └──────┬───────┘
                                         │
                                         ▼
                                  ┌──────────────┐
                                  │   Lessons    │
                                  └──────────────┘
```

The exact models can evolve as the product develops.

The important principle is that the database should capture **knowledge about the prospect and what was learned**, not just contact information.

---

# Prospect Lifecycle

A prospect moves through a simple lifecycle.

```text
              ┌─────────┐
              │   NEW   │
              └────┬────┘
                   │
                   ▼
             ┌───────────┐
             │ ANALYZED  │
             └─────┬─────┘
                   │
                   ▼
             ┌───────────┐
             │ OUTREACH  │
             └─────┬─────┘
                   │
                   ▼
             ┌──────────────┐
             │ CONVERSATION │
             └──────┬───────┘
                    │
                    ▼
             ┌─────────────┐
             │   LEARNED   │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │   OUTCOME   │
             └─────────────┘
```

The actual Django status choices may be simpler than this diagram.

The diagram represents the **business workflow**, not necessarily every database status.

---

# AI Enrichment Flow

When a user inserts raw prospect information:

```text
User Input
    │
    ▼
ProspectInput
    │
    ▼
AI Analysis
    │
    ├── Company
    ├── Industry
    ├── Notes
    ├── Context
    └── Other structured information
    │
    ▼
Create / Update Prospect
    │
    ▼
Prospect Bank
```

The raw input and structured prospect should be treated as separate concepts when useful.

This allows the original information to remain available while the AI-generated structure can evolve.

---

# Outreach Flow

Outreach is generated from the structured prospect information.

```text
Prospect
    │
    ▼
Context
    │
    ▼
Current workflow
    │
    ▼
Potential problem
    │
    ▼
Discovery questions
    │
    ▼
Outreach message
```

The core discovery framework is:

```text
1. How are you doing this today?

2. What is difficult about the current process?

3. What happens if the problem is not solved?
```

The system should use these questions as a **discovery framework**, not blindly insert them into every message.

The goal is to generate a natural question based on the prospect's actual context.

---

# MCP Architecture

MCP acts as an interface between AI clients and the Industry Prospect application.

```text
┌───────────────┐
│ Claude / AI   │
└───────┬───────┘
        │
        │ MCP
        ▼
┌────────────────────┐
│ apps/mcp/server.py │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Django Services    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Django Models      │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ PostgreSQL         │
└────────────────────┘
```

### Important Rule

**MCP tools should be thin.**

Avoid putting substantial business logic directly inside:

```text
apps/mcp/server.py
```

Instead:

```text
MCP Tool
   ↓
Service
   ↓
Model
   ↓
Database
```

This makes the system easier to test and maintain.

---

# Celery Architecture

Celery is used for work that does not need to block the user's request.

For example:

```text
User
 │
 ▼
Django
 │
 ▼
Queue Task
 │
 ▼
Redis / Broker
 │
 ▼
Celery Worker
 │
 ▼
Analysis / Processing
 │
 ▼
PostgreSQL
```

Potential background operations include:

* AI prospect analysis
* Large prospect enrichment jobs
* Batch processing
* Future external data enrichment
* Other long-running operations

Not every operation needs Celery.

Simple database operations should remain synchronous.

---

# Why a Monolith?

Industry Prospect intentionally starts as a **Django monolith**.

A monolithic architecture provides:

* Faster development
* Easier debugging
* Simpler deployment
* Shared database access
* Straightforward testing
* Less infrastructure
* Easier iteration during product discovery

The application is still modular internally.

```text
Django Monolith
│
├── Inspector
│   ├── Models
│   ├── Services
│   ├── Views
│   └── Tasks
│
├── MCP
│   └── Tools
│
└── Config
```

A monolith does not mean everything should be placed in one file.

The goal is:

> **Simple deployment, modular code.**

---

# Dependency Direction

The preferred dependency direction is:

```text
Interfaces
    ↓
Services
    ↓
Models
    ↓
Database
```

For example:

```text
MCP Tool
    ↓
Prospect Service
    ↓
Prospect Model
    ↓
PostgreSQL
```

Avoid creating dependencies in the opposite direction.

For example, a model should not need to know about:

* MCP
* Claude
* HTTP requests
* UI templates

This keeps the domain logic independent from external interfaces.

---

# External AI

AI should be treated as an external capability rather than the application's source of truth.

```text
Django
   │
   ├── Prospect context
   │
   ▼
AI
   │
   ├── Analysis
   ├── Extraction
   └── Generation
   │
   ▼
Django
   │
   ▼
Validated / structured data
   │
   ▼
PostgreSQL
```

The database remains the application's source of truth.

AI-generated information can be reviewed, updated, or replaced.

---

# Future Architecture

The current architecture should remain intentionally small.

As the product grows, additional components can be introduced only when there is a clear need.

Potential future additions include:

```text
External enrichment APIs
        │
        ▼
Enrichment Service
        │
        ▼
Prospect
```

or:

```text
Django
  │
  ├── Web Application
  ├── API
  ├── MCP
  ├── Celery
  └── Services
```

A separate frontend, API service, or microservice architecture should only be introduced when the existing Django architecture becomes an actual constraint.

---

# Architecture Goals

The architecture should optimize for:

1. **Simplicity** — minimize unnecessary infrastructure.
2. **Modularity** — keep business logic separated into services.
3. **Reusability** — allow Django, MCP, Celery, and future interfaces to reuse the same services.
4. **Testability** — keep business operations independent from UI and MCP.
5. **AI flexibility** — AI should enrich the system without becoming tightly coupled to the database.
6. **Fast iteration** — the architecture should support rapid changes while the product is still being validated.

The guiding principle is:

> **Build the smallest architecture that supports the feedback loop.**

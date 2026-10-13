# Miguel Moreno · Engineering in practice

I build full-stack applications, cloud automations, and AI-assisted workflows that make everyday operations more reliable.

This is my public engineering portfolio: **three original, runnable demonstrations built with fictional data**. The code, interfaces, and screenshots were created specifically for this repository. They are not extracts, replicas, or anonymized exports of client systems.

[Professional profile](https://www.linkedin.com/in/miguelven/) · [Architecture & tradeoffs](docs/ARCHITECTURE.md) · [Use in applications](docs/APPLICATIONS.md)

## About me

I'm Miguel Moreno, a software engineer with a mechanical-engineering background. I build across the interface, API, database, and operational workflow: React and Next.js products, Python and Node.js services, cloud integrations, and practical AI tools. My experience includes startup full-stack development, Python services for AI workflows, and internal applications connecting scheduling, reporting, payments, and legacy systems.

I like work where understanding the business process matters as much as choosing the framework. I can discuss a problem with the person doing the work, turn it into a usable application, and investigate what happens when the inputs or network stop behaving ideally. I work in English and Spanish and use AI development tools with tests, review, and explicit verification boundaries.

**Available for remote full-time or contractor engineering roles.** My strongest fit is full-stack product engineering, applied AI integrations, and cloud/business automation.

## Selected experience

These are high-level summaries of my broader work. The source code and screenshots in this repository belong only to the new synthetic demonstrations below.

| Area | Work I've done | Relevant capabilities |
| --- | --- | --- |
| Scheduling and cloud integrations | Connected calendars, scheduling APIs, operational records, and notifications; handled renewal, retries, duplicates, and state reconciliation | Python, Azure Functions, Microsoft Graph, webhooks |
| Field operations | Built inspection, work-order, scheduling, and reporting workflows with offline storage, draft recovery, and synchronization | React, IndexedDB, Node.js, SQL, PDF reports |
| Business intake and dashboards | Connected forms, documents, email, chat, and operational data so users can work from a structured record | FastAPI, TypeScript, Airtable, Teams |
| Payments and invoicing | Integrated payment services and chat-based invoice workflows with structured inputs and operator feedback | Stripe, REST APIs, adaptive cards |
| Manufacturing systems | Extended a legacy ERP through macros, SQL queries, and reporting for quotes, materials, procurement, and production | ERP integration, SQL, engineering workflows |
| Document processing | Extracted PDF annotations with page/section context and generated structured reports and addendums | Python, PyMuPDF, Streamlit, DOCX/PDF |
| AI and data tooling | Built model-backed workflows and contact-enrichment tools with source provenance, confidence signals, and human review; explored local inference separately | Model integration, tool interfaces, data validation; MLX experiments |
| Product applications | Built live league standings with explicit tie-breaking rules and administrative controls; worked on interview workflows with recovery and reporting | Next.js, Supabase, realtime, browser media, tests |

I studied Mechanical Engineering at Metropolitan University of Caracas (2020–2025) and software development through freeCodeCamp (2019–2023). My mechanical background is particularly useful when software needs to represent physical processes and operational constraints.

## How I work

- **Understand the workflow:** clarify who uses the result, what must remain correct, and which failure cases matter.
- **Own the complete path:** interface, API, data model, cloud configuration, and debugging evidence.
- **Make results reviewable:** focused tests, understandable traces, source-backed answers, and clear limitations.
- **Protect the underlying work:** discuss architecture and decisions without sharing client implementations or private records.

## Start with the work

| Demonstration | What to try | What it shows |
| --- | --- | --- |
| **01 · Reliable integrations** | Run seven deliveries, including failure, retry, replay, stale data, and a conflicting writer | Transaction boundaries, idempotency, revision checks, and visible outcomes |
| **02 · Data to decisions** | Validate a deliberately flawed CSV, load the clean sample, then export | Row-level feedback, decimal arithmetic, and safe export gating |
| **03 · Transparent assistant** | Ask about blocked orders, inspect a specific order, or request a prohibited action | Read-only tools, evidence-backed answers, explicit unsupported intents |

### 01 · Reliable integrations

![Event delivery trace with seven attempts, three writes, and final revision four](docs/01-reliable-integrations.jpg)

The temporary failure leaves no acknowledgement. A retry succeeds, its replay is ignored, an old revision cannot reverse the result, and a conflicting writer cannot overwrite newer state. Each run starts with a fresh SQLite database in memory.

### 02 · Data to decisions

![CSV validation with individual row errors and export disabled](docs/02-data-validation.jpg)

Invalid quantities and unknown items are explained in place. A clean input enables a JSON download. Totals use Python's `Decimal`; invalid rows never silently contribute to the subtotal, and a changed input invalidates its previous preview.

### 03 · Transparent assistant

![Fictional blocked orders alongside the tool execution trace](docs/03-assistant-workflow.jpg)

The answer includes the records that support it. This intentionally uses **deterministic routing, not a live LLM**. It demonstrates the tool and evidence layer without sending any data to a model provider. All implemented tools are read-only; the phrase filter is a demonstration, not a production authorization system.

## Run locally

Requires **Python 3.10+**. There are no packages to install, accounts to create, API keys, or external services.

```sh
git clone https://github.com/Migue19ve/engineering-portfolio.git
cd engineering-portfolio
python3 server.py
```

Open **http://127.0.0.1:8765**. Stop the server with Ctrl+C. To use another port: `python3 server.py --port 8766`.

The Python backend is required; opening the HTML file directly will not run the demos. This repository is not a hosted live service.

## Verify

```sh
python3 -m unittest discover -s tests -v
node --check static/app.js
node --test tests/frontend.test.cjs
python3 scripts/check_public_content.py
```

Node is only needed for the JavaScript checks and regression tests. Git is needed for the tracked-file publication check. GitHub Actions runs these checks on pushes and pull requests.

## Scope and provenance

- All company names, orders, products, amounts, identifiers, and failure scenarios are invented fixtures. No client code or data was consulted to implement these demos.
- Screenshots show this application using those fixtures. They are not production screenshots or mock images of claimed customer results.
- Requests stay on the local server. There are no runtime API integrations, analytics, external fonts, or automatic network calls beyond the local app. The LinkedIn link opens a professional profile only when clicked.
- No personal email, phone number, résumé, client names, credentials, private links, infrastructure identifiers, or internal documents are included.
- The demos illustrate engineering choices; they do not establish production scalability, distributed correctness, enterprise security, deployed AI, or measured business results.
- Development was AI-assisted, including implementation and tests. The repository is a demonstration artifact, not a claim that every line was written without assistance.

## Technical walkthrough

The backend uses Python's standard library, SQLite transactions, CSV parsing, and decimal arithmetic. The frontend is accessible HTML, responsive CSS, and browser JavaScript. See [the architecture notes](docs/ARCHITECTURE.md) for decisions, limitations, and next steps for a real deployment.

**Copyright © 2026 Miguel Moreno. All rights reserved.** Shared for portfolio evaluation; no open-source reuse license is granted. See [LICENSE](LICENSE).

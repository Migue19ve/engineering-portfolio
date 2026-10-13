# Implementation notes

## A deliberately small system

```text
Browser interface (HTML / CSS / JavaScript)
                 |
          same-origin JSON
                 |
        Python localhost server
          /       |       \
    event replay  CSV      read-only tool router
    SQLite        Decimal fictional order fixtures
```

The app has no package dependencies, build step, account, or remote backend. One command starts it. This lowers the friction for a reviewer and keeps synthetic data inside the demonstration.

## Event processing

`EventStore.apply` opens a transaction, checks for an existing delivery ID, compares revisions, applies a conditional update, and records the delivery before committing. A simulated transient failure rolls back. A conflicting expected revision also rolls back without acknowledging the event. A repeated ID with different revision/value is rejected.

The server constructs the scenario; clients cannot send arbitrary events. Every run owns a fresh, independent SQLite connection. Parallel test runs establish isolation between scenarios; they do **not** test multiple workers contending on a shared database. This is a sequential illustration of the state machine.

For a real integration, requirements would include persistent storage and retention, external authentication and signature validation, a defined retry/dead-letter policy, operational metrics, real concurrent-writer testing, schema evolution, and recovery after a crash. The event ID is assumed to identify the immutable revision/value. A production schema would need an explicit canonical payload contract and collision policy.

## CSV to validated output

The schema requires exactly `sku,quantity,unit_price`. Limits bound request size, row count, quantities, and monetary values. Each row is checked for known products, unique SKU, complete columns, integer quantity, and finite decimal money with no more than two decimal places. Scientific notation, non-finite values, negative prices, and fractional quantities are rejected.

The preview reports a subtotal for valid rows, clearly distinct from a fully valid quote. JSON export requires zero invalid rows. Editing input clears the previous export state. An in-flight response is discarded if it no longer matches the current input. The sample clean subtotal is **USD 266.20**.

JSON is used instead of spreadsheet output, avoiding a spreadsheet-formula execution surface. The narrow SKU allowlist also rejects formula-like values. This is a fictional estimate; it does not calculate tax, take payment, or place orders.

## Assistant tools and evidence

Three supported intents map to a read-only dataset: blocked orders, specific demo order IDs, and an order summary. A small policy check makes prohibited actions visible. There is no dynamic code execution, SQL generation, remote tool invocation, or model call. An unsupported question returns a scoped response rather than invented facts.

The important boundary is architectural: no mutating tool exists. Keyword filtering alone is not a security boundary. A real assistant would need authenticated identities, authorization inside each tool, explicit approval for consequential actions, model/provider configuration, evaluation datasets, and logging/redaction policy.

## UI and server boundaries

- User-derived values are inserted using `textContent`, not interpreted as HTML.
- Request size and input length are bounded. Only explicitly listed static files are served.
- The server binds to `127.0.0.1`; Host and Origin checks limit cross-site requests and host confusion.
- Content Security Policy restricts scripts and connections to this app. No third-party assets load.
- Request logging is disabled. No input is written to disk. A user-initiated JSON download is the only persisted demo output.
- The Python standard-library server is for local review, not public hosting. Do not expose it with a tunnel or bind it publicly.

## What is and is not verified

The automated suite checks state transitions, retry behavior, ID collision, conflict preservation, independent scenario runs, money precision, invalid CSV, assistant boundaries, returned-record isolation, and HTTP access limits. The frontend gets a syntax check, asynchronous stale-response regression tests, and manual browser verification of interactions and responsive layouts. Screenshots are direct browser captures.

No real customer system, cloud account, live model, load benchmark, shared-database concurrency guarantee, or production deployment is part of this repository.

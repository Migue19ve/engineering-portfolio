"""Original portfolio exercises. All records and scenarios are fictional."""
import csv
import io
import re
import sqlite3
from decimal import Decimal

CATALOG = {"KITE-01": "Desktop stand", "MOSS-02": "Cable organizer", "LUMA-03": "Task light"}
ORDERS = [
    {"id": "DEMO-1001", "customer": "Juniper Studio", "status": "ready", "items": 4},
    {"id": "DEMO-1002", "customer": "Orbit Workshop", "status": "blocked", "items": 7, "reason": "Missing delivery window"},
    {"id": "DEMO-1003", "customer": "Pebble Lab", "status": "pending", "items": 2},
    {"id": "DEMO-1004", "customer": "Cedar Works", "status": "blocked", "items": 3, "reason": "Item substitution needs review"},
]


class EventStore:
    """Transactional local illustration of replay and revision protection."""
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.db.executescript("""
            CREATE TABLE delivery(id TEXT PRIMARY KEY, revision INTEGER, value TEXT);
            CREATE TABLE record(id INTEGER PRIMARY KEY, revision INTEGER, value TEXT);
            INSERT INTO record VALUES(1, 0, 'Not created');
        """)

    def close(self):
        self.db.close()

    def state(self):
        revision, value = self.db.execute("SELECT revision,value FROM record WHERE id=1").fetchone()
        return {"revision": revision, "value": value}

    def apply(self, event, transient=False):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            old = self.db.execute("SELECT revision,value FROM delivery WHERE id=?", (event["id"],)).fetchone()
            if old:
                status = "duplicate" if old == (event["revision"], event["value"]) else "conflict"
            elif transient:
                # Failure occurs before acknowledgement. The same event may retry.
                self.db.rollback()
                return "retry"
            else:
                current = self.state()["revision"]
                if event["revision"] <= current:
                    status = "stale"
                elif event["expected"] != current:
                    self.db.rollback()
                    return "conflict"
                else:
                    self.db.execute("UPDATE record SET revision=?,value=? WHERE id=1 AND revision=?",
                                    (event["revision"], event["value"], current))
                    status = "applied"
                self.db.execute("INSERT INTO delivery VALUES(?,?,?)", (event["id"], event["revision"], event["value"]))
            self.db.commit()
            return status
        except Exception:
            self.db.rollback()
            raise


def event_scenario():
    schedule = [
        ("evt-01", 1, 0, "Draft", False, "Create the initial record"),
        ("evt-02", 2, 1, "Scheduled", True, "Inject a temporary failure before writing"),
        ("evt-02", 2, 1, "Scheduled", False, "Retry the unacknowledged delivery"),
        ("evt-02", 2, 1, "Scheduled", False, "Replay the successful delivery"),
        ("evt-03", 1, 0, "Draft", False, "Deliver an older revision late"),
        ("evt-04", 4, 2, "Confirmed", False, "Apply a newer valid revision"),
        ("evt-05", 5, 2, "Rescheduled", False, "Reject a writer with outdated state"),
    ]
    store = EventStore()
    try:
        log = []
        for event_id, revision, expected, value, transient, detail in schedule:
            event = {"id": event_id, "revision": revision, "expected": expected, "value": value}
            status = store.apply(event, transient)
            log.append({"event": event_id, "status": status, "detail": detail, "revision": store.state()["revision"]})
        return {"log": log, "state": store.state(), "writes": sum(x["status"] == "applied" for x in log),
                "deliveries": len(log), "mode": "Synthetic, sequential fault simulation; fresh in-memory SQLite database per run"}
    finally:
        store.close()


def validate_quote(text):
    """Validate every row before allowing export. Money never uses floats."""
    if not isinstance(text, str) or len(text) > 20000:
        raise ValueError("Provide CSV text under 20,000 characters.")
    reader = csv.reader(io.StringIO(text), strict=True)
    rows, seen, total = [], set(), Decimal("0.00")
    try:
        if next(reader, []) != ["sku", "quantity", "unit_price"]:
            raise ValueError("Expected exactly: sku,quantity,unit_price")
        while True:
            line = reader.line_num + 1
            values = next(reader, None)
            if values is None:
                break
            if not values:
                continue
            if len(rows) >= 100:
                raise ValueError("Use at most 100 data rows.")
            row = dict(zip(["sku", "quantity", "unit_price"], values))
            errors = []
            sku = (row.get("sku") or "").strip()
            quantity = (row.get("quantity") or "").strip()
            price = (row.get("unit_price") or "").strip()
            if len(values) != 3:
                errors.append("Wrong number of columns")
            if sku not in CATALOG:
                errors.append("Unknown SKU")
            if sku in seen:
                errors.append("Duplicate SKU")
            seen.add(sku)
            qty_ok = bool(re.fullmatch(r"[0-9]{1,5}", quantity)) and 1 <= int(quantity) <= 10000
            price_ok = bool(re.fullmatch(r"[0-9]{1,7}(\.[0-9]{1,2})?", price)) and Decimal(price) <= Decimal("1000000")
            if not qty_ok:
                errors.append("Quantity must be a whole number from 1 to 10,000")
            if not price_ok:
                errors.append("Price must be 0 to 1,000,000, with at most two decimal places")
            subtotal = None
            if not errors:
                subtotal = (Decimal(price) * int(quantity)).quantize(Decimal("0.01"))
                total += subtotal
            rows.append({"line": line, "sku": sku, "name": CATALOG.get(sku, "Unrecognized item"),
                         "quantity": int(quantity) if qty_ok else quantity, "unit_price": price,
                         "subtotal": str(subtotal) if subtotal is not None else None, "errors": errors})
    except csv.Error as exc:
        raise ValueError("Malformed CSV quoting.") from exc
    if not rows:
        raise ValueError("Add at least one data row.")
    invalid = sum(bool(row["errors"]) for row in rows)
    return {"rows": rows, "valid_rows": len(rows) - invalid, "invalid_rows": invalid,
            "valid_subtotal": str(total), "currency": "USD", "export_ready": invalid == 0,
            "notice": "Synthetic estimate; no tax, shipping, billing, or purchase action."}


def assistant_query(query):
    """Deterministic intent routing plus allowlisted, read-only tools. No LLM."""
    if not isinstance(query, str) or not query.strip() or len(query) > 500:
        raise ValueError("Enter a question from 1 to 500 characters.")
    prompt = query.strip().lower()
    denied = re.search(r"\b(delete|remove|send|update|change|pay|cancel|approve|write|ignore|export)\b", prompt)
    if denied:
        return {"answer": "This demo only reads fictional orders. No changes, messages, payments, or exports were performed.",
                "trace": [{"tool": "policy_check", "status": "blocked", "detail": "Requested action is outside the read-only tool allowlist"}], "records": []}
    ids = re.findall(r"demo-\d+", prompt)
    if ids:
        records = [dict(order) for order in ORDERS if order["id"].lower() in ids]
        detail = "Lookup requested synthetic order IDs"
        answer = f"Found {len(records)} matching order(s)." if records else "No matching order exists in the demo dataset."
    elif "blocked" in prompt:
        records = [dict(order) for order in ORDERS if order["status"] == "blocked"]
        detail = "Filter orders where status = blocked"
        answer = f"{len(records)} orders need attention. Review the reasons below; no orders were changed."
    elif "summary" in prompt or "overview" in prompt or "summarize" in prompt:
        records = [dict(order) for order in ORDERS]
        detail = "Read the four-record synthetic dataset"
        answer = f"{len(records)} orders: {sum(x['status'] == 'ready' for x in records)} ready, {sum(x['status'] == 'pending' for x in records)} pending, {sum(x['status'] == 'blocked' for x in records)} blocked."
    else:
        return {"answer": "Try 'Which orders are blocked?', 'Show DEMO-1001', or 'Give me an order summary'. I cannot answer beyond these demo tools.",
                "trace": [{"tool": "intent_router", "status": "unsupported", "detail": "No supported intent; no facts invented"}], "records": []}
    return {"answer": answer, "trace": [
        {"tool": "intent_router", "status": "ok", "detail": "Deterministic rule routing; no model call"},
        {"tool": "orders.read", "status": "ok", "detail": detail},
        {"tool": "render_evidence", "status": "ok", "detail": f"Answer derived from {len(records)} returned records"}], "records": records}

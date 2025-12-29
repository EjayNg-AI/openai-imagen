from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

from jinja2 import Environment, BaseLoader, select_autoescape


TEMPLATE = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Purchase Request {{ pr.request_id }}</title>
  <style>
    :root {
      --bg: #0b0f19;
      --card: #111827;
      --card2: #0f172a;
      --text: #e5e7eb;
      --muted: #9ca3af;
      --border: rgba(255,255,255,.10);
      --accent: #60a5fa;
      --good: #34d399;
      --warn: #fbbf24;
      --bad: #f87171;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      --sans: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
    }
    body {
      margin: 0; font-family: var(--sans);
      background: radial-gradient(1200px 600px at 20% 10%, rgba(96,165,250,.15), transparent 60%),
                  radial-gradient(900px 500px at 80% 30%, rgba(52,211,153,.10), transparent 55%),
                  var(--bg);
      color: var(--text);
    }
    .wrap { max-width: 980px; margin: 40px auto; padding: 0 18px; }
    .header { display: flex; gap: 16px; align-items: baseline; flex-wrap: wrap; }
    .title { font-size: 28px; font-weight: 750; letter-spacing: .2px; margin: 0; }
    .pill {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 6px 10px; border-radius: 999px;
      border: 1px solid var(--border); background: rgba(255,255,255,.04);
      color: var(--muted); font-size: 13px;
    }
    .pill strong { color: var(--text); font-weight: 650; }
    .grid { display: grid; grid-template-columns: 1fr; gap: 14px; margin-top: 18px; }
    @media (min-width: 860px) { .grid { grid-template-columns: 1.2fr .8fr; } }
    .card {
      background: linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px 16px 14px;
      box-shadow: 0 14px 40px rgba(0,0,0,.35);
    }
    h2 { margin: 0 0 10px; font-size: 16px; letter-spacing: .2px; }
    .kv { display: grid; grid-template-columns: 170px 1fr; gap: 8px 14px; }
    .k { color: var(--muted); font-size: 13px; }
    .v { font-size: 14px; }
    .mono { font-family: var(--mono); }
    .section { margin-top: 16px; }
    .item {
      border-top: 1px solid var(--border);
      padding-top: 12px; margin-top: 12px;
    }
    .item:first-child { border-top: 0; padding-top: 0; margin-top: 0; }
    .item-title { font-weight: 650; margin: 0 0 6px; }
    .item-meta { display: flex; gap: 10px; flex-wrap: wrap; color: var(--muted); font-size: 13px; }
    .badge {
      display: inline-flex; align-items: center;
      padding: 2px 8px; border-radius: 999px;
      border: 1px solid var(--border);
      background: rgba(255,255,255,.03);
    }
    table { width: 100%; border-collapse: collapse; }
    th, td { text-align: left; padding: 10px 10px; border-top: 1px solid var(--border); vertical-align: top; }
    th { color: var(--muted); font-weight: 650; font-size: 13px; }
    td { font-size: 14px; }
    .status { font-weight: 650; }
    .status.approved { color: var(--good); }
    .status.pending { color: var(--warn); }
    .status.rejected { color: var(--bad); }
    .small { color: var(--muted); font-size: 13px; }
    .footer { margin-top: 16px; color: var(--muted); font-size: 12px; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <h1 class="title">Purchase Request</h1>
      <span class="pill"><strong>ID</strong> <span class="mono">{{ pr.request_id }}</span></span>
      <span class="pill"><strong>Urgency</strong> {{ pr.urgency|capitalize }}</span>
      <span class="pill"><strong>Needed By</strong> {{ pr.needed_by_fmt }}</span>
      <span class="pill"><strong>Budget</strong> <span class="mono">{{ pr.budget_code }}</span></span>
    </div>

    <div class="grid">
      <div class="card">
        <h2>Request Summary</h2>
        <div class="kv">
          <div class="k">Requestor</div><div class="v">{{ pr.requestor.name }}</div>
          <div class="k">Email</div><div class="v mono">{{ pr.requestor.email }}</div>
          <div class="k">Department</div><div class="v">{{ pr.requestor.department }}</div>
          <div class="k">Budget Code</div><div class="v mono">{{ pr.budget_code }}</div>
          <div class="k">Needed By</div><div class="v">{{ pr.needed_by_fmt }}</div>
          <div class="k">Urgency</div><div class="v">{{ pr.urgency|capitalize }}</div>
        </div>

        <div class="section">
          <h2>Requested Items</h2>
          {% for it in pr.items %}
            <div class="item">
              <p class="item-title">{{ loop.index }}. {{ it.description }}</p>
              <div class="item-meta">
                <span class="badge">{{ it.item_type|capitalize }}</span>
                <span class="badge">Qty: {{ it.quantity }}</span>
                <span class="badge">
                  {{ it.estimated_cost_range.currency }} {{ it.estimated_cost_range.min }} – {{ it.estimated_cost_range.max }}
                  {% if it.cost_is_per_unit %}<span class="small">&nbsp;(per unit)</span>{% endif %}
                </span>
              </div>
              <p class="small" style="margin: 8px 0 0;">{{ it.purpose }}</p>
            </div>
          {% endfor %}
        </div>
      </div>

      <div class="card">
        <h2>Approval Status</h2>
        <table>
          <thead>
            <tr>
              <th style="width: 22%;">Role</th>
              <th style="width: 23%;">Approver</th>
              <th style="width: 15%;">Status</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {% for ap in pr.approvals %}
            <tr>
              <td>{{ ap.role }}</td>
              <td>{{ ap.approver }}</td>
              <td class="status {{ ap.status|lower }}">{{ ap.status|capitalize }}</td>
              <td>{{ ap.note }}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>

        <div class="section">
          <h2>At-a-Glance</h2>
          <div class="small">
            <div><strong>Scope:</strong> {{ pr.scope_summary }}</div>
            <div><strong>Next blockers:</strong> {{ pr.blockers_summary }}</div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer">
      Rendered {{ pr.rendered_at }}.
    </div>
  </div>
</body>
</html>
"""


def _parse_date_iso(d: str) -> Optional[datetime]:
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except Exception:
        return None


def _fmt_date(d: str) -> str:
    dt = _parse_date_iso(d)
    return dt.strftime("%-d %B %Y") if dt else d  # keeps original if unexpected format


def _scope_summary(items: List[Dict[str, Any]]) -> str:
    # e.g. "Hardware + Software + Service"
    types = []
    for it in items:
        t = str(it.get("item_type", "")).strip().lower()
        if t and t not in types:
            types.append(t)
    if not types:
        return "—"
    return " + ".join(t.capitalize() for t in types)


def _blockers_summary(approvals: List[Dict[str, Any]]) -> str:
    pending_roles = [a.get("role") for a in approvals if str(a.get("status", "")).lower() == "pending"]
    pending_roles = [r for r in pending_roles if r]
    return ", ".join(pending_roles) if pending_roles else "None"


def _normalize_pr(pr: Dict[str, Any]) -> Dict[str, Any]:
    pr = dict(pr)  # shallow copy
    pr["needed_by_fmt"] = _fmt_date(str(pr.get("needed_by", "")))
    pr["rendered_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    items = pr.get("items") or []
    approvals = pr.get("approvals") or []

    # Heuristic: if quantity > 1 and cost range looks like per unit, tag as per-unit
    for it in items:
        qty = int(it.get("quantity") or 0)
        it["cost_is_per_unit"] = True if qty > 1 else False

    pr["scope_summary"] = _scope_summary(items)
    pr["blockers_summary"] = _blockers_summary(approvals)

    # Ensure required nested keys exist to avoid template explosions
    pr.setdefault("requestor", {})
    pr["requestor"].setdefault("name", "")
    pr["requestor"].setdefault("email", "")
    pr["requestor"].setdefault("department", "")

    pr.setdefault("items", items)
    pr.setdefault("approvals", approvals)
    pr.setdefault("urgency", "")
    pr.setdefault("budget_code", "")
    pr.setdefault("request_id", "")

    return pr


def render_html_from_json(json_input: str) -> str:
    """
    Accepts JSON text in the format: [ { ...purchase request... } ] or { ... }.
    Returns a full HTML document string.
    """
    data = json.loads(json_input)

    # Accept either list-of-PRs or single PR object; render the first PR if list
    if isinstance(data, list):
        if not data:
            raise ValueError("JSON input is an empty list; expected at least one PR object.")
        pr_obj = data[0]
    elif isinstance(data, dict):
        pr_obj = data
    else:
        raise TypeError("JSON root must be a list or an object.")

    pr = _normalize_pr(pr_obj)

    env = Environment(
        loader=BaseLoader(),
        autoescape=select_autoescape(enabled_extensions=("html", "xml"), default=True),
    )
    tmpl = env.from_string(TEMPLATE)
    return tmpl.render(pr=pr)


def main() -> None:
    # Example usage: read JSON from a file and write HTML output
    in_path = Path("input.json")
    out_path = Path("purchase_request.html")
    html = render_html_from_json(in_path.read_text(encoding="utf-8"))
    out_path.write_text(html, encoding="utf-8")
    print(f"Wrote {out_path.resolve()}")


if __name__ == "__main__":
    main()

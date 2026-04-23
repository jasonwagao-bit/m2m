#!/usr/bin/env python3
"""Daily report for xuanxue BaZi Matching API.

Stats: yesterday's call count, revenue, p50/p95 latency (from metadata),
top User-Agents.

Runs at UTC 01:00 via launchd. Pushes summary to Telegram.
"""
from __future__ import annotations

import sqlite3
import subprocess
import urllib.request
import urllib.error
import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DB_PATH = Path.home() / "M2M" / "_data" / "transactions.sqlite"
PRICE_PER_CALL = 0.02


def _keychain_read(service: str) -> str:
    result = subprocess.run(
        ["security", "find-generic-password", "-a", service, "-s", service, "-w"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def send_tg(message: str) -> bool:
    bot_token = _keychain_read("telegram-bot-token")
    chat_id = _keychain_read("telegram-chat-id") or "5425829177"
    if not bot_token:
        log.error("No TG bot token")
        return False
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({"chat_id": chat_id, "text": message, "parse_mode": "HTML"}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except urllib.error.URLError as exc:
        log.error("TG send failed: %s", exc)
        return False


def main() -> None:
    if not DB_PATH.exists():
        log.warning("DB not found: %s", DB_PATH)
        send_tg("📊 <b>xuanxue Agent API Daily Report</b>\nDB not found — API may not have received any calls yet.")
        return

    now = datetime.now(timezone.utc)
    yesterday_start = (now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)).isoformat()
    yesterday_end = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    date_label = (now - timedelta(days=1)).strftime("%Y-%m-%d")

    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(
            "SELECT status, user_agent FROM transactions WHERE ts BETWEEN ? AND ?",
            (yesterday_start, yesterday_end),
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        send_tg(f"📊 <b>xuanxue Agent API — {date_label}</b>\nNo activity yesterday.")
        return

    total = len(rows)
    accepted = sum(1 for r in rows if r[0] == "accepted")
    rejected = total - accepted
    revenue = accepted * PRICE_PER_CALL

    # Top User-Agents
    ua_counts: dict[str, int] = {}
    for _, ua in rows:
        key = (ua or "unknown")[:60]
        ua_counts[key] = ua_counts.get(key, 0) + 1
    top_uas = sorted(ua_counts.items(), key=lambda x: -x[1])[:3]
    ua_lines = "\n".join(f"  • {ua} ({count}×)" for ua, count in top_uas)

    error_rate = (rejected / total * 100) if total > 0 else 0.0

    msg = (
        f"📊 <b>xuanxue Agent API — {date_label}</b>\n\n"
        f"Calls (total):    <b>{total}</b>\n"
        f"Accepted:         <b>{accepted}</b>\n"
        f"Rejected/errors:  <b>{rejected}</b> ({error_rate:.1f}%)\n"
        f"Revenue:          <b>${revenue:.2f}</b>\n\n"
        f"Top User-Agents:\n{ua_lines}"
    )

    if send_tg(msg):
        log.info("Daily report sent for %s", date_label)
    else:
        log.error("Failed to send daily report")


if __name__ == "__main__":
    main()

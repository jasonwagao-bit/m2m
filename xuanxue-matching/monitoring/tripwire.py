#!/usr/bin/env python3
"""Tripwire monitoring for xuanxue BaZi Matching API.

Checks every hour:
  1. Silent period: no calls for 10+ min after active period → TG alert
  2. Error rate > 5% in last hour → TG alert
  3. Yesterday's revenue < $0.10 → TG alert (UTC 00:00 window)

TG credentials read from macOS Keychain:
  security find-generic-password -a telegram-bot-token -s telegram-bot-token -w
  security find-generic-password -a telegram-chat-id -s telegram-chat-id -w

DB: ~/M2M/_data/transactions.sqlite (created by x402 middleware)
"""
from __future__ import annotations

import sqlite3
import subprocess
import sys
import urllib.request
import urllib.error
import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

DB_PATH = Path.home() / "M2M" / "_data" / "transactions.sqlite"
PRICE_PER_CALL = 0.02  # USD


# ---------------------------------------------------------------------------
# Keychain helpers
# ---------------------------------------------------------------------------

def _keychain_read(service: str) -> str:
    """Read a secret from macOS Keychain. Returns empty string on failure."""
    result = subprocess.run(
        ["security", "find-generic-password", "-a", service, "-s", service, "-w"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        log.warning("Keychain read failed for %s: %s", service, result.stderr.strip())
        return ""
    return result.stdout.strip()


def _get_tg_creds() -> tuple[str, str]:
    bot_token = _keychain_read("telegram-bot-token")
    chat_id = _keychain_read("telegram-chat-id")
    if not chat_id:
        chat_id = "5425829177"
    return bot_token, chat_id


# ---------------------------------------------------------------------------
# Telegram send
# ---------------------------------------------------------------------------

def send_tg(message: str) -> bool:
    bot_token, chat_id = _get_tg_creds()
    if not bot_token:
        log.error("No TG bot token — cannot send alert")
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


# ---------------------------------------------------------------------------
# DB queries
# ---------------------------------------------------------------------------

def _open_db() -> sqlite3.Connection | None:
    if not DB_PATH.exists():
        log.warning("DB not found: %s", DB_PATH)
        return None
    return sqlite3.connect(DB_PATH)


def _check_silent_period() -> bool:
    """Return True if alert should fire: no calls in last 10 min but had calls in prior 50 min."""
    conn = _open_db()
    if conn is None:
        return False
    now = datetime.now(timezone.utc)
    ten_min_ago = (now - timedelta(minutes=10)).isoformat()
    sixty_min_ago = (now - timedelta(minutes=60)).isoformat()
    try:
        recent = conn.execute(
            "SELECT COUNT(*) FROM transactions WHERE ts > ? AND status = 'accepted'",
            (ten_min_ago,),
        ).fetchone()[0]
        prior = conn.execute(
            "SELECT COUNT(*) FROM transactions WHERE ts BETWEEN ? AND ? AND status = 'accepted'",
            (sixty_min_ago, ten_min_ago),
        ).fetchone()[0]
    finally:
        conn.close()
    return recent == 0 and prior > 0


def _check_error_rate() -> tuple[bool, float]:
    """Return (should_alert, error_rate_pct) for last hour."""
    conn = _open_db()
    if conn is None:
        return False, 0.0
    one_hour_ago = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    try:
        total = conn.execute(
            "SELECT COUNT(*) FROM transactions WHERE ts > ?", (one_hour_ago,)
        ).fetchone()[0]
        errors = conn.execute(
            "SELECT COUNT(*) FROM transactions WHERE ts > ? AND status NOT IN ('accepted','rejected_no_payment','rejected_wrong_network')",
            (one_hour_ago,),
        ).fetchone()[0]
    finally:
        conn.close()
    if total == 0:
        return False, 0.0
    rate = errors / total * 100
    return rate > 5.0, rate


def _check_daily_revenue() -> tuple[bool, float]:
    """Return (should_alert, revenue_usd) for UTC yesterday.
    Only fires during UTC 00:00–01:00 window.
    """
    now = datetime.now(timezone.utc)
    if now.hour != 0:
        return False, 0.0

    yesterday_start = (now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)).isoformat()
    yesterday_end = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    conn = _open_db()
    if conn is None:
        return False, 0.0
    try:
        calls = conn.execute(
            "SELECT COUNT(*) FROM transactions WHERE ts BETWEEN ? AND ? AND status = 'accepted'",
            (yesterday_start, yesterday_end),
        ).fetchone()[0]
    finally:
        conn.close()

    revenue = calls * PRICE_PER_CALL
    return revenue < 0.10, revenue


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    log.info("Tripwire check starting")
    alerts_sent = 0

    # Check 1: silent period
    if _check_silent_period():
        msg = (
            "🔕 <b>xuanxue Agent API — Silent Period</b>\n"
            "No accepted calls in last 10 min, but had calls in prior 50 min.\n"
            "Check Render logs: https://dashboard.render.com"
        )
        if send_tg(msg):
            log.info("Alert sent: silent period")
            alerts_sent += 1

    # Check 2: error rate
    should_alert, rate = _check_error_rate()
    if should_alert:
        msg = (
            f"⚠️ <b>xuanxue Agent API — High Error Rate</b>\n"
            f"Error rate in last hour: <b>{rate:.1f}%</b> (threshold: 5%)\n"
            "Check Render logs."
        )
        if send_tg(msg):
            log.info("Alert sent: error rate %.1f%%", rate)
            alerts_sent += 1

    # Check 3: daily revenue (only at UTC 00:xx)
    should_alert, revenue = _check_daily_revenue()
    if should_alert:
        msg = (
            f"💸 <b>xuanxue Agent API — Low Daily Revenue</b>\n"
            f"Yesterday revenue: <b>${revenue:.2f}</b> (threshold: $0.10)\n"
            "Check Base explorer for wallet activity."
        )
        if send_tg(msg):
            log.info("Alert sent: low revenue $%.2f", revenue)
            alerts_sent += 1

    log.info("Tripwire check complete — %d alerts sent", alerts_sent)


if __name__ == "__main__":
    main()

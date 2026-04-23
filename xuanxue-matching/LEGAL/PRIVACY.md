# Agent API Privacy Policy

**Publisher:** xuanxue.app (Oslov Technology Pty Ltd)  
**Contact:** oslovtech@gmail.com  
**Last updated:** 2026-04-23

---

## 1. Scope

This policy applies to the xuanxue BaZi Matching API ("Agent API"). It describes what data is processed when an AI agent or application calls the Agent API.

## 2. Data Received Per Request

| Data field | Source | Stored? |
|------------|--------|---------|
| Birth year/month/day/hour, gender (×2) | Request body | **No** — in-memory only |
| SHA-256 hash of full request body | Computed | Yes (SQLite `request_hash`) |
| On-chain transaction hash | X-Payment header | Yes |
| Wallet address (`from`) | X-Payment header | Yes |
| User-Agent (truncated 256 chars) | HTTP header | Yes |
| IP address | TCP connection | No — in-memory rate limiter only, discarded after 60s |
| Timestamp (UTC) | Server clock | Yes |

## 3. SQLite Transaction Log — Schema

```sql
CREATE TABLE transactions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ts          TEXT    NOT NULL,   -- UTC ISO-8601
    tx_hash     TEXT,               -- on-chain hash
    amount      TEXT,               -- "0.02"
    from_addr   TEXT,               -- wallet address
    endpoint    TEXT,               -- "/agents/v1/bazi-matching"
    user_agent  TEXT,               -- truncated UA string
    status      TEXT                -- "accepted" | "rejected_*"
    -- NOTE: no person_a/person_b raw fields; only request_hash added for audit
);
```

Birth data is **never** written to this table or any other persistent store.

## 4. Legal Basis (GDPR)

- **Role:** We act as a *data processor* on behalf of the API caller (data controller).
- **Basis for transaction log:** Legitimate interest (fraud prevention, billing reconciliation).
- **Basis for in-memory processing:** Performance of contract (API service delivery).

## 5. Retention

| Data | Retention |
|------|-----------|
| Birth data | 0 seconds (in-memory only) |
| Transaction log rows | 12 months, then deleted |
| IP address | 60 seconds (in-memory rate limiter only) |

## 6. Data Sharing

We do not sell, trade, or share the transaction log or any derived data with third parties, except as required by applicable law.

## 7. CCPA (California Consumer Privacy Act)

We do not sell personal information. California residents may request disclosure of transaction log data associated with their wallet address by contacting us.

## 8. GDPR Data Subject Rights

Because birth data is never stored in identifiable form:
- **Right of access / erasure for birth data**: cannot be fulfilled (data was never stored).
- **Transaction log data** (associated with a wallet address): we will respond to access or erasure requests within 30 days.

## 9. Security

- SQLite database stored on server-local filesystem with restricted OS permissions.
- All API traffic served over HTTPS/TLS.
- No credentials or secrets are logged.

## 10. Changes

Material changes to this policy will be announced at `https://xuanxue.app/legal/agents-privacy` with a new "Last updated" date.

## 11. Contact

**oslovtech@gmail.com**

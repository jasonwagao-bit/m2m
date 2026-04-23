# xuanxue-bazi-matching

> **Deterministic BaZi (八字) API for AI agents. No LLM drift.**

[![npm version](https://img.shields.io/npm/v/xuanxue-bazi-matching)](https://www.npmjs.com/package/xuanxue-bazi-matching)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![x402 compatible](https://img.shields.io/badge/payment-x402%20USDC-blue)](https://x402.org)

Rule-based Chinese metaphysics engine — same inputs always return the same score. No token unpredictability, no hallucinated charts, no per-LLM-call cost. Pay only per API call via **x402 USDC on Base**.

**Publisher**: [xuanxue.app](https://xuanxue.app) · **Contact**: oslovtech@gmail.com · **Docs**: [api.decodeyourming.com/docs/agents](https://api.decodeyourming.com/docs/agents)

---

## Use Cases

1. **Matchmaking agent** — feed two users' birth data, get a compatibility report with scores, five-elements balance, strengths, and actionable recommendations. Works in any Claude workflow or autonomous agent loop.
2. **Content planning** — determine auspicious days for publishing, product launches, or live-stream scheduling based on the creator's BaZi day-flow.
3. **Decision timing** — let an AI assistant advise on the best day to sign contracts, start projects, or make major purchases using the daily fortune luck score.

---

## Install

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "xuanxue-bazi": {
      "command": "npx",
      "args": ["-y", "xuanxue-bazi-matching"],
      "env": {
        "XUANXUE_PAYMENT_TOKEN": "<your x402 payment token>"
      }
    }
  }
}
```

### Any MCP client

```bash
npx -y xuanxue-bazi-matching
```

Set `XUANXUE_PAYMENT_TOKEN` to a valid x402 token, or omit to receive 402 payment challenges.

---

## Tools

### `marriage_compatibility_check`

BaZi (八字) compatibility between two birth charts.

**Input**:
```json
{
  "person_a": {"year": 1990, "month": 5, "day": 15, "hour": 10, "gender": "male"},
  "person_b": {"year": 1993, "month": 8, "day": 22, "hour": 14, "gender": "female"}
}
```

**Output**:
```json
{
  "score": 78,
  "elements_balance": {"wood": 0.28, "fire": 0.18, "earth": 0.22, "metal": 0.17, "water": 0.15},
  "narrative": "Strong day-pillar resonance...",
  "strengths": ["complementary elements", "shared earth anchor"],
  "challenges": ["competing fire energy"],
  "recommendations": ["schedule key decisions on water days"]
}
```

### `bazi_daily_fortune`

BaZi day-flow luck analysis for a given date.

**Input**:
```json
{
  "year": 1990, "month": 5, "day": 15, "hour": 10, "gender": "male",
  "query_date": "2026-04-22"
}
```

**Output**:
```json
{
  "luck_score": 82,
  "dominant_element": "wood",
  "favorable_activities": ["negotiation", "creative work", "networking"],
  "unfavorable_activities": ["surgery", "major financial moves"],
  "timing_advice": "Morning hours amplify wood energy..."
}
```

---

## Example — curl direct

```bash
# Marriage compatibility (returns 402 without token)
curl -X POST https://api.decodeyourming.com/agents/v1/bazi-matching \
  -H "Content-Type: application/json" \
  -H "X-PAYMENT: <token>" \
  -d '{"person_a":{"year":1990,"month":5,"day":15,"hour":10,"gender":"male"},"person_b":{"year":1993,"month":8,"day":22,"hour":14,"gender":"female"}}'

# Daily fortune
curl -X POST https://api.decodeyourming.com/agents/v1/bazi-daily-fortune \
  -H "Content-Type: application/json" \
  -H "X-PAYMENT: <token>" \
  -d '{"year":1990,"month":5,"day":15,"hour":10,"gender":"male","query_date":"2026-04-22"}'
```

---

## Pricing

| Tool | Price |
|------|-------|
| `marriage_compatibility_check` | $0.02 USDC / call |
| `bazi_daily_fortune` | $0.005 USDC / call |

Payment via **x402 protocol** on Base. Address: `0xcb99bf3d45d5f8bdeb72d00792fe77dffed2c6de`.  
No subscription. No sign-up. Pay as you go.

---

## FAQ

**Why deterministic instead of LLM-based?**  
LLM responses vary per run and hallucinate chart data. BaZi is a rule-based system with precisely defined algorithms — the same birth data always produces the same pillars, ten-gods, and interactions. Deterministic = testable, auditable, and cheaper at scale.

**Why x402 / USDC instead of a credit card API key?**  
x402 enables true pay-per-call from any agent without account creation. An autonomous agent can acquire a payment token, execute calls, and stop paying when done — no OAuth flow, no monthly minimums. No surprise overages.

**How is BaZi different from Western astrology?**  
Western astrology maps to solar positions and broad archetypes. BaZi (Eight Characters / 八字) encodes the precise interaction between year, month, day, and hour pillars in a five-elements framework, producing day-specific energy states rather than monthly forecasts. The ruleset has ~1000 years of empirical refinement.

---

## License

MIT · [xuanxue.app](https://xuanxue.app) · [oslovtech@gmail.com](mailto:oslovtech@gmail.com)

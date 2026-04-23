# Building a Deterministic Divination API for AI Agents with x402

*Tags: mcp, agents, blockchain, chinese-metaphysics, x402*

---

## Why Deterministic?

Most "AI fortune-telling" products layer an LLM on top of some birth data and ask it to "interpret" the chart. That sounds powerful until you notice the same query returns different answers on Tuesday vs Thursday. For an autonomous agent making decisions — scheduling a product launch, advising a user on timing — non-determinism is a bug, not a feature.

BaZi (八字, Eight Characters) is a Chinese metaphysics system that encodes a person's birth year, month, day, and hour into four "pillars," each representing a Heavenly Stem and Earthly Branch. The compatibility and day-flow calculations are fully rule-based: given the same inputs, the output is always identical. No LLM needed.

That makes it a perfect fit for agents: testable, auditable, and predictable cost.

---

## The Stack

- **Backend**: Python rule engine. No neural net — just ~3000 lines of classical BaZi rules encoded as lookup tables and interaction matrices.
- **API layer**: FastAPI on Render, deployed at `api.decodeyourming.com`.
- **Payment**: [x402 protocol](https://x402.org) — HTTP 402 challenges resolved with USDC on Base. Agents pay per call, no account required.
- **MCP server**: TypeScript stdio server wrapping the two endpoints. Distributed via npm.

---

## The Two Endpoints

### `POST /agents/v1/bazi-matching` — $0.02/call

Takes two birth charts, returns:

```json
{
  "score": 78,
  "elements_balance": {"wood": 0.28, "fire": 0.18, "earth": 0.22, "metal": 0.17, "water": 0.15},
  "narrative": "Strong day-pillar resonance between the two charts...",
  "strengths": ["complementary water-fire dynamic"],
  "challenges": ["competing fire energy in month pillars"],
  "recommendations": ["schedule key decisions on water days"]
}
```

### `POST /agents/v1/bazi-daily-fortune` — $0.005/call

Takes one birth chart + a target date, returns:

```json
{
  "luck_score": 82,
  "dominant_element": "wood",
  "favorable_activities": ["negotiation", "creative work"],
  "unfavorable_activities": ["surgery", "major financial moves"],
  "timing_advice": "Morning hours amplify wood energy..."
}
```

---

## The Python Rule Engine

The core compatibility function looks like this (simplified):

```python
def compute_compatibility(chart_a: BaziChart, chart_b: BaziChart) -> CompatibilityResult:
    score = 0.0

    # Day-pillar resonance (highest weight: 35%)
    dp_harmony = DAY_PILLAR_HARMONY_TABLE[chart_a.day_stem][chart_b.day_stem]
    score += dp_harmony * 0.35

    # Five-elements balance (25%)
    balance_a = chart_a.element_distribution()
    balance_b = chart_b.element_distribution()
    complement_score = element_complement(balance_a, balance_b)
    score += complement_score * 0.25

    # Ten-Gods interaction (20%)
    tg_score = ten_gods_interaction(chart_a.ten_gods, chart_b.ten_gods)
    score += tg_score * 0.20

    # ... remaining rules ...

    return CompatibilityResult(score=round(score * 100), ...)
```

No LLM call. No prompt injection surface. Same inputs → same output every time.

---

## x402 Middleware

The payment middleware intercepts requests before they hit the business logic:

```python
from x402.middleware import X402Middleware

app.add_middleware(
    X402Middleware,
    facilitator_url="https://x402.org/facilitator",
    endpoints={
        "/agents/v1/bazi-matching": {"price": "0.02", "currency": "USDC", "network": "base"},
        "/agents/v1/bazi-daily-fortune": {"price": "0.005", "currency": "USDC", "network": "base"},
    },
    payment_address="0xcb99bf3d45d5f8bdeb72d00792fe77dffed2c6de",
)
```

If no `X-PAYMENT` header, the response is:

```http
HTTP/1.1 402 Payment Required
X-Payment-Challenge: eyJ...
```

The agent resolves the challenge, retries with the token, and the request goes through. No OAuth, no API key management, no subscription.

---

## Claude Desktop Integration

Install the MCP server:

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

Claude now has two new tools: `marriage_compatibility_check` and `bazi_daily_fortune`. You can ask:

> "Check compatibility between someone born 1990-05-15 10am male and 1993-08-22 2pm female."

Claude calls the tool, gets the JSON, and narrates the result — without ever hallucinating a chart.

---

## What's Next

- **Smithery / MCP Registry listing** — making the server discoverable to all Claude users
- **Streamable HTTP transport** — so agents can connect without local npx
- **More tools** — Zi Wei Dou Shu (紫微斗数) yearly forecast, Qi Men Dun Jia (奇门遁甲) event timing

---

## Try It

3 free calls available to dev.to readers — DM me or open an issue on the [repo](https://github.com/jasonwagao/m2m) for a payment token.

Docs: [api.decodeyourming.com/docs/agents](https://api.decodeyourming.com/docs/agents)

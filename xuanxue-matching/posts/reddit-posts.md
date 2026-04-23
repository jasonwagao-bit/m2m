# Reddit Posts — xuanxue-bazi-matching MCP Server

---

## r/ClaudeAI

**Title**: I built an MCP server that gives Claude deterministic BaZi (Chinese metaphysics) tools — pay-per-call via x402

Hey r/ClaudeAI,

Just shipped `xuanxue-bazi-matching`, an MCP server that adds two new tools to Claude:

- **`marriage_compatibility_check`** — takes two birth charts, returns a 0-100 score, five-elements balance, strengths/challenges, and recommendations. $0.02/call via x402 USDC.
- **`bazi_daily_fortune`** — takes a birth chart + target date, returns a luck score, dominant element, and favorable/unfavorable activities. $0.005/call.

The key differentiator: these are fully **deterministic** — no LLM involved in the calculation, just a Python rule engine encoding classical BaZi (八字) algorithms. Same birth data always returns the same score. Claude uses the output as tool results and narrates them, but the computation is reproducible and auditable.

Payment is x402 — Claude can call these tools from any agent workflow, the API issues a 402 challenge, the agent pays ~$0.02 in USDC on Base, done. No API key signup needed.

**Install** (30 seconds):

```json
{
  "mcpServers": {
    "xuanxue-bazi": {
      "command": "npx",
      "args": ["-y", "xuanxue-bazi-matching"],
      "env": {"XUANXUE_PAYMENT_TOKEN": "<token>"}
    }
  }
}
```

Repo: https://github.com/jasonwagao/m2m  
npm: `xuanxue-bazi-matching`

Happy to answer questions about the BaZi rule encoding or the x402 integration.

---

## r/LocalLLaMA

**Title**: Built a deterministic Chinese metaphysics API for autonomous agents — no LLM in the hot path, x402 micropayments

For anyone building tool-use agents: I published an MCP server (`xuanxue-bazi-matching`) wrapping two BaZi (八字) calculation endpoints.

BaZi is a Chinese metaphysics system that encodes birth year/month/day/hour into four pillars and derives compatibility + day-flow luck from their interactions. The entire calculation is a rule engine (~3000 lines of classical interaction tables). Zero LLM in the computation path.

Why this matters for agent builders:
- **Deterministic outputs** — you can unit-test against it, cache aggressively, audit results
- **x402 payment** — no OAuth, no signup, agents pay per-call in USDC on Base; great for workflows where you want usage-proportional costs without subscription overhead
- **Sub-200ms** — fast enough for multi-step agent loops

Two tools: `marriage_compatibility_check` ($0.02) and `bazi_daily_fortune` ($0.005).

Works with any MCP client. npm package: `xuanxue-bazi-matching`. Docs at api.decodeyourming.com/docs/agents.

The interesting engineering challenge was the rule encoding — Ten Gods interaction matrices, Earthly Branch combination tables, seasonal strength adjustments. If anyone's curious about the data model I'm happy to go deeper.

---

## r/mcp (or r/modelcontextprotocol)

**Title**: New MCP server: deterministic BaZi (八字) compatibility + daily fortune — pay-per-call via x402 USDC

**xuanxue-bazi-matching** — an MCP server exposing two tools:

| Tool | What it does | Price |
|------|-------------|-------|
| `marriage_compatibility_check` | 0-100 BaZi compatibility score between two birth charts | $0.02/call |
| `bazi_daily_fortune` | Luck score + timing advice for a given date | $0.005/call |

**Why it might be interesting to this sub:**

1. **x402 native** — first MCP server I've seen using x402 micropayments rather than a bearer API key. The server returns 402 challenges; any agent with a funded wallet can call it without registration.

2. **Fully deterministic** — the calculation is a Python rule engine, not LLM prompting. Same inputs, same output. This makes it composable with other agent tools without worrying about output variance.

3. **Minimal setup** — `npx -y xuanxue-bazi-matching` + one env var.

Server is live on npm. Repo: https://github.com/jasonwagao/m2m

Open to feedback on the server.json schema, tool descriptions, or the x402 integration pattern.

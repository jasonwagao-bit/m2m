# Show HN: Xuanxue — Pay-per-call BaZi compatibility API for AI agents (x402/USDC)

**Title**: Show HN: Xuanxue — Pay-per-call BaZi (八字) compatibility API for AI agents (x402/USDC)

---

BaZi (Eight Characters / 八字) is a Chinese metaphysics system that computes compatibility and day-flow luck from birth pillars. Unlike LLM-based fortune apps, the calculation is fully deterministic — same inputs always return the same score. No prompt, no drift, no hallucinated charts.

I built two MCP tools around a Python rule engine:
- `marriage_compatibility_check` — 0-100 score, five-elements balance, recommendations. $0.02/call.
- `bazi_daily_fortune` — luck score, dominant element, favorable activities for any date. $0.005/call.

Payment is x402 over Base/USDC. The API returns HTTP 402 with a challenge; agents resolve it and retry. No API keys, no subscriptions, no account required — works natively in autonomous agent loops.

The MCP server is on npm (`npx -y xuanxue-bazi-matching`), connects in ~10 seconds via Claude Desktop config.

What's non-obvious: the hard part wasn't the x402 plumbing — it was encoding ~3000 lines of classical BaZi interaction rules (Ten Gods, Earthly Branch combinations, seasonal adjustments) accurately enough that practitioners don't laugh at the output.

Repo: https://github.com/jasonwagao/m2m  
Docs: https://api.decodeyourming.com/docs/agents  
Publisher: xuanxue.app

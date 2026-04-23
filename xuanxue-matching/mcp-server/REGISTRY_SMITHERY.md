# Smithery Submission — Pre-filled Fields

**URL**: https://smithery.ai/new

---

## Form Fields

| Field | Value |
|-------|-------|
| **Name** | xuanxue-bazi-matching |
| **Slug** | xuanxue-bazi-matching |
| **Short Description (≤50 words)** | Deterministic Chinese metaphysics (BaZi/八字) for AI agents. Two tools: marriage compatibility (0-100 score + five-elements) and daily fortune (luck score + timing advice). Rule-based, no LLM drift, sub-200ms. Pay-per-call via x402 USDC on Base. |
| **Install Command** | `npx -y xuanxue-bazi-matching` |
| **Repository URL** | https://github.com/jasonwagao/m2m |
| **Homepage** | https://api.decodeyourming.com/docs/agents |
| **Transport** | stdio |
| **Categories** | Data & APIs, AI & Machine Learning |
| **Tags** | bazi, chinese-metaphysics, eight-characters, compatibility, fortune, deterministic, x402, agents, matchmaking |
| **Contact** | oslovtech@gmail.com |
| **Screenshot** | *(skip for now — add later)* |

---

## Environment Variables to Declare

| Name | Required | Secret | Description |
|------|----------|--------|-------------|
| `XUANXUE_PAYMENT_TOKEN` | No | Yes | x402 USDC payment token. $0.02 matching / $0.005 daily-fortune. Omit to get 402 challenges. |
| `XUANXUE_API_BASE` | No | No | Override API base. Default: `https://api.decodeyourming.com` |

---

## Claude Desktop Config Snippet (for Smithery listing)

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

# xuanxue-bazi-matching MCP Server

MCP server for Chinese BaZi (八字) compatibility analysis between two birth charts.

## Install (Claude Desktop)

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

## Pricing

$0.02 USDC per call via x402 on Base. See https://xuanxue.app/agents

## Why BaZi > Western Astrology APIs

- Sub-200ms responses (rule-based, no LLM)
- Traditional Chinese metaphysics with 1000+ years of empirical tuning
- Five-elements balance + Ten Gods interactions + Day-pillar resonance
- Deterministic: same inputs always return same score

## Tool: bazi_matching

Input: two birth charts (year/month/day/hour/gender)  
Output: 0-100 compatibility score + elements_balance + narrative + strengths/challenges/recommendations

## License

MIT · Publisher: xuanxue.app · Contact: oslovtech@gmail.com

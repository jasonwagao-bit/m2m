# MCP Registry Submission Guide

> Docs-only. No actual submission until Jason runs the CLI commands below.

---

## Tools in This Server

| Tool | Endpoint | Price |
|------|---------|-------|
| `marriage_compatibility_check` | `POST /agents/v1/bazi-matching` | $0.02 USDC |
| `bazi_daily_fortune` | `POST /agents/v1/bazi-daily-fortune` | $0.005 USDC |

---

## 1. Official MCP Registry (registry.modelcontextprotocol.io)

**Prerequisite**: npm package published + GitHub OAuth.

```bash
# Step 1 — add mcpName to package.json (one-time edit)
# "mcpName": "io.github.jasonwagao/xuanxue-bazi-matching"

# Step 2 — npm publish
cd ~/M2M/xuanxue-matching/mcp-server
npm login
npm run build
npm publish --access public

# Step 3 — mcp-publisher
brew install mcp-publisher
mcp-publisher login github   # browser: enter device code from CLI
mcp-publisher publish        # reads server.json in cwd

# Verify
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=xuanxue-bazi-matching"
```

**server.json** pre-filled at `./server.json`. Two manual edits before publish:
1. Bump `version` to match npm publish version.
2. `package.json` — add `"mcpName": "io.github.jasonwagao/xuanxue-bazi-matching"`.

---

## 2. Smithery (smithery.ai/new)

**Form fields** — see `REGISTRY_SMITHERY.md`.

**CLI alternative** (after npm publish):
```bash
npm install -g @smithery/cli
smithery mcp publish "https://github.com/jasonwagao/m2m" -n xuanxue-bazi-matching
```

> Note: Smithery prefers Streamable HTTP transport. stdio works but integration is via `npx`.

---

## 3. Glama (glama.ai)

No manual submission. Glama auto-crawls public GitHub repos.

- Make repo public → Glama indexes within ~24h.
- Accelerate: paste `https://github.com/jasonwagao/m2m` on https://glama.ai/mcp/servers.
- Glama reads `README.md` — optimized version already in `./README.md`.

---

## 4. mcpservers.org (mcpservers.org/submit)

**Form fields** — see `REGISTRY_MCPSERVERS.md`.

Free tier: manual review ~3-5 days.
Premium $39: badge + dofollow link + priority review. Recommended.

---

## Pre-flight Checklist (all registries)

- [ ] `gh repo create jasonwagao/m2m --public` or set existing repo to public
- [ ] `npm run build` passes (tsc clean)
- [ ] `npm login` + `npm publish --access public` → `xuanxue-bazi-matching@0.1.0` on npmjs.com
- [ ] Add `"mcpName": "io.github.jasonwagao/xuanxue-bazi-matching"` to `package.json`
- [ ] Confirm live: `curl https://api.decodeyourming.com/agents/v1/bazi-matching` → 402 (not 404)
- [ ] Confirm live: `curl https://api.decodeyourming.com/agents/v1/bazi-daily-fortune` → 402 (not 404)

# Go-Live Checklist — xuanxue-bazi-matching MCP Registry Launch

> Sequential order. Complete each step before the next.  
> Estimated total: ~45 minutes Jason-time.

---

## Phase 1 — Repo & Package (15 min)

### 1. Make GitHub repo public
```bash
gh repo edit jasonwagao/m2m --visibility public
# OR: GitHub.com → Settings → Danger Zone → Make Public
```
- **Expected**: repo visible at https://github.com/jasonwagao/m2m
- **Risk**: source code becomes public; MIT licensed, intended
- **Benefit**: unlocks Glama auto-crawl + Smithery CLI submit

### 2. Add `mcpName` to package.json
Edit `~/M2M/xuanxue-matching/mcp-server/package.json`, add:
```json
"mcpName": "io.github.jasonwagao/xuanxue-bazi-matching"
```
- Required for official MCP Registry (`mcp-publisher` reads this)

### 3. Build + npm publish
```bash
cd ~/M2M/xuanxue-matching/mcp-server
npm run build           # must pass tsc clean
npm login               # Jason's npmjs.com account
npm publish --access public
```
- **Expected**: `xuanxue-bazi-matching@0.1.0` visible at https://www.npmjs.com/package/xuanxue-bazi-matching
- **Risk**: package name squatting if `xuanxue-bazi-matching` is taken — check first: `npm view xuanxue-bazi-matching`
- **Estimated time**: 5 min

---

## Phase 2 — Official MCP Registry (10 min)

### 4. Install mcp-publisher
```bash
brew install mcp-publisher
# fallback: npm i -g @modelcontextprotocol/mcp-publisher
```

### 5. Login + publish
```bash
cd ~/M2M/xuanxue-matching/mcp-server
mcp-publisher login github    # browser opens, enter device code
mcp-publisher publish         # reads server.json
```
- **Expected**: listed at https://registry.modelcontextprotocol.io
- **Verify**: `curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=xuanxue-bazi-matching"`
- **Risk**: GitHub account must match `io.github.jasonwagao/` prefix; if account is different username, update `server.json` name field first
- **Estimated time**: 5 min

---

## Phase 3 — Smithery (5 min)

### 6. Submit to Smithery
Option A (web form): https://smithery.ai/new → paste fields from `REGISTRY_SMITHERY.md`  
Option B (CLI, after npm publish):
```bash
npm install -g @smithery/cli
smithery mcp publish "https://github.com/jasonwagao/m2m" -n xuanxue-bazi-matching
```
- **Expected**: listed at https://smithery.ai/server/xuanxue-bazi-matching
- **Risk**: Smithery may require Streamable HTTP transport for full integration; stdio works for now
- **Estimated time**: 5 min

---

## Phase 4 — mcpservers.org (5 min)

### 7. Submit to mcpservers.org
Go to https://mcpservers.org/submit → paste fields from `REGISTRY_MCPSERVERS.md`  
Select **Premium $39** (dofollow link + badge + priority review).
- **Expected**: review within 24h (premium) vs 3-5 days (free)
- **Cost**: $39 one-time
- **Risk**: low — submission is non-binding
- **Estimated time**: 3 min + payment

---

## Phase 5 — Glama (0 min active)

### 8. Glama auto-crawl
No action needed after repo is public. Glama indexes within ~24h.  
Accelerate: https://glama.ai/mcp/servers → "Submit a server" → paste `https://github.com/jasonwagao/m2m`
- **Expected**: indexed within 24h
- **Risk**: none

---

## Phase 6 — Content (10 min)

### 9. dev.to post
Go to https://dev.to/new → paste content from `posts/dev-to-post.md`  
Add tags: `mcp`, `agents`, `blockchain`, `webdev`  
Publish.
- **Expected**: indexed by Google within ~24h; HN/Reddit traffic if cross-posted
- **Estimated time**: 5 min

### 10. Hacker News — Show HN
Go to https://news.ycombinator.com/submit → paste from `posts/hn-post.md`  
**Best time to post**: Tuesday–Thursday 8–10am US EST.
- **Risk**: HN penalizes "Show HN" posts with obvious commercial intent; lead with the technical angle (deterministic rule engine + x402)
- **Estimated time**: 2 min

### 11. Reddit posts
- r/ClaudeAI: paste `## r/ClaudeAI` section from `posts/reddit-posts.md`
- r/LocalLLaMA: paste `## r/LocalLLaMA` section
- r/mcp or r/modelcontextprotocol: paste last section
- **Estimated time**: 5 min total
- **Risk**: don't cross-post all three on the same day — space by 24h

---

## Verification After Each Registry

```bash
# npm
npm view xuanxue-bazi-matching

# Official Registry
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=xuanxue-bazi-matching"

# Quick API smoke test
curl -s -o /dev/null -w "%{http_code}" \
  -X POST https://api.decodeyourming.com/agents/v1/bazi-matching \
  -H "Content-Type: application/json" \
  -d '{"person_a":{"year":1990,"month":5,"day":15,"hour":10,"gender":"male"},"person_b":{"year":1993,"month":8,"day":22,"hour":14,"gender":"female"}}'
# Expected: 402
```

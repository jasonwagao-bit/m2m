# MCP Registry 上架提交文档

> 实际 PR / 提交需要 Jason 本人的 GitHub/npm 账号。本文档提供预填内容，零步骤遗漏。

---

## 1. 官方 MCP Registry（modelcontextprotocol.io）

**提交地址**：https://registry.modelcontextprotocol.io  
**方式**：CLI 工具 `mcp-publisher`（GitHub OAuth 认证）

### 步骤

```bash
# 1. 先 npm publish（需要 Jason 的 npm 账号）
cd ~/M2M/xuanxue-matching/mcp-server
npm install && npm run build
npm adduser          # 如已登录可跳过
npm publish --access public

# 2. package.json 需先加 mcpName 字段（见下方 diff）
# 3. 安装 mcp-publisher
brew install mcp-publisher

# 4. 生成 server.json（已预生成，见 server.json）
mcp-publisher init   # 可跳过，server.json 已就绪

# 5. GitHub 登录
mcp-publisher login github
# 浏览器打开 https://github.com/login/device，输入 CLI 给出的 device code

# 6. 发布
mcp-publisher publish
```

### package.json 需追加的字段

```json
"mcpName": "io.github.jasonwagao/xuanxue-bazi-matching"
```

注意：`mcpName` 前缀必须是 `io.github.<你的GitHub用户名>/`，与 GitHub 账号绑定。

### 必填字段汇总

| 字段 | 值 |
|------|-----|
| name (mcpName) | `io.github.jasonwagao/xuanxue-bazi-matching` |
| description | Chinese BaZi compatibility analysis between two birth charts. Rule-based, sub-200ms, pay-per-call $0.02 USDC. |
| repository | https://github.com/jasonwagao/m2m |
| npm identifier | `xuanxue-bazi-matching` |
| license | MIT |
| author | xuanxue.app \<oslovtech@gmail.com\> |

**验证发布**：
```bash
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.jasonwagao/xuanxue-bazi-matching"
```

---

## 2. Smithery（smithery.ai）

**提交地址**：https://smithery.ai/new  
**方式**：Web 表单 + 可选 CLI

> ⚠️ Smithery 要求 Streamable HTTP transport。本 server 目前是 stdio only。
> **选项 A**：先用 stdio 模式提交，填 GitHub repo URL 而非 HTTPS 端点。
> **选项 B**：后续给后端加 `/agents/v1/mcp` Streamable HTTP 端点，再补交。

### 当前可提交的方式（选项 A - CLI 发布 npm 包）

```bash
# 安装 smithery CLI
npm install -g @smithery/cli

# 发布（需 GitHub 账号登录）
smithery mcp publish "https://github.com/jasonwagao/m2m/tree/main/xuanxue-matching/mcp-server" \
  -n xuanxue-bazi-matching
```

### 表单字段（https://smithery.ai/new）

| 字段 | 值 |
|------|-----|
| Server Name | xuanxue-bazi-matching |
| Short Description | Chinese BaZi (八字) compatibility analysis. 0-100 score + five-elements balance + narrative. Pay-per-call $0.02 USDC. |
| GitHub URL | https://github.com/jasonwagao/m2m |
| Transport | stdio |
| Contact | oslovtech@gmail.com |

---

## 3. mcpservers.org

**提交地址**：https://mcpservers.org/submit  
**方式**：Web 表单（免费）或 Premium $39（加急审核 + badge + dofollow link）

### 表单字段

| 字段 | 值 |
|------|-----|
| Server Name | xuanxue-bazi-matching |
| Short Description | Chinese BaZi (八字) compatibility analysis between two birth charts. Returns 0-100 score, five-elements balance, strengths/challenges/recommendations. Rule-based (no LLM), sub-200ms, pay-per-call $0.02 USDC via x402 on Base. |
| Link | https://github.com/jasonwagao/m2m/tree/main/xuanxue-matching/mcp-server |
| Category | Other（或 Development） |
| Contact Email | oslovtech@gmail.com |

建议选 **Premium $39**，获得 badge + dofollow link，有助于 SEO 和曝光。

---

## 4. Glama（glama.ai）

**提交地址**：https://glama.ai/mcp/servers  
**方式**：通过 GitHub 仓库 URL 自动索引（无需手动 PR，抓取公开仓库）

- 确保 `package.json` 有 `name`、`description`、`repository` 字段 ✅
- 确保仓库是 public
- Glama 会自动发现并索引

可手动加速：在 https://glama.ai/mcp/servers 页面搜索 `xuanxue-bazi-matching`，若未出现则提交 GitHub URL。

---

## 前置清单（所有 Registry 通用）

- [ ] GitHub repo `jasonwagao/m2m` 设为 public（或专为此创建 `xuanxue-bazi-matching` 独立 repo）
- [ ] npm publish `xuanxue-bazi-matching@0.1.0`（需 Jason npm 账号）
- [ ] `package.json` 加 `mcpName` 字段（官方 Registry 必须）
- [ ] 确认 `https://api.xuanxue.app/agents/v1/bazi-matching` 端点 live

---

## 提交者身份

- 发布者：xuanxue.app
- 联系邮箱：oslovtech@gmail.com
- GitHub：jasonwagao
- npm：（使用 Jason 的 npm 账号）

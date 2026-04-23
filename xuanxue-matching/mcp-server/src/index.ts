#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const API_BASE = process.env.XUANXUE_API_BASE ?? "https://api.decodeyourming.com";
const PAYMENT_HEADER = process.env.XUANXUE_PAYMENT_TOKEN; // x402 payment token

const server = new Server(
  { name: "xuanxue-bazi-matching", version: "0.1.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "marriage_compatibility_check",
      description: "Deterministic marriage compatibility API for AI agents. Rule-based BaZi analysis between two birth charts. Returns 0-100 compatibility score, five-elements balance, strengths, challenges, recommendations. No LLM drift, sub-200ms response, x402 payable on Base. $0.02/call.",
      inputSchema: {
        type: "object",
        properties: {
          person_a: {
            type: "object",
            description: "Person A birth info",
            properties: {
              year: {type: "integer"},
              month: {type: "integer"},
              day: {type: "integer"},
              hour: {type: "integer"},
              gender: {type: "string", enum: ["male", "female"]}
            },
            required: ["year", "month", "day", "hour", "gender"]
          },
          person_b: {
            type: "object",
            description: "Person B birth info (same schema as person_a)",
            properties: {
              year: {type: "integer"},
              month: {type: "integer"},
              day: {type: "integer"},
              hour: {type: "integer"},
              gender: {type: "string", enum: ["male", "female"]}
            },
            required: ["year", "month", "day", "hour", "gender"]
          }
        },
        required: ["person_a", "person_b"]
      }
    },
    {
      name: "bazi_daily_fortune",
      description: "Deterministic daily fortune API for AI agents. Rule-based BaZi day-flow analysis. Returns 0-100 luck score, dominant element, favorable/unfavorable activities, timing advice. No LLM drift, sub-200ms response, x402 payable on Base. $0.005/call.",
      inputSchema: {
        type: "object",
        properties: {
          year: {type: "integer", description: "Birth year"},
          month: {type: "integer", description: "Birth month (1-12)"},
          day: {type: "integer", description: "Birth day"},
          hour: {type: "integer", description: "Birth hour (0-23)"},
          gender: {type: "string", enum: ["male", "female"]},
          query_date: {type: "string", description: "Date to forecast, ISO 8601 (YYYY-MM-DD). Defaults to today."}
        },
        required: ["year", "month", "day", "hour", "gender"]
      }
    },
    {
      name: "qimen_timing",
      description: "QiMen Dunjia (奇门遁甲) timing analysis for AI agents. Returns auspicious/inauspicious directions, optimal action window, and full palace grid. Strictly action_timing & luck_onset only — NOT investment advice, NOT medical diagnosis, NOT legal judgment. No LLM drift, sub-300ms, x402 payable on Base. $0.05/call.",
      inputSchema: {
        type: "object",
        properties: {
          query: {type: "string", description: "Natural language description of the intended action (Chinese or English)"},
          target_time: {type: "string", description: "ISO 8601 datetime for the chart. Defaults to now (UTC)."},
          target_category: {type: "string", enum: ["action_timing", "luck_onset"], description: "action_timing = best moment to act; luck_onset = when a luck cycle begins"}
        },
        required: ["query"]
      }
    }
  ]
}));

const TOOL_CONFIG: Record<string, { endpoint: string; price: string }> = {
  marriage_compatibility_check: { endpoint: "/agents/v1/bazi-matching", price: "$0.02" },
  bazi_daily_fortune:           { endpoint: "/agents/v1/bazi-daily-fortune", price: "$0.005" },
  qimen_timing:                 { endpoint: "/agents/v1/qimen-timing", price: "$0.05" },
};

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const tool = TOOL_CONFIG[request.params.name];
  if (!tool) throw new Error(`Unknown tool: ${request.params.name}`);

  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (PAYMENT_HEADER) headers["X-PAYMENT"] = PAYMENT_HEADER;

  const resp = await fetch(`${API_BASE}${tool.endpoint}`, {
    method: "POST",
    headers,
    body: JSON.stringify(request.params.arguments)
  });
  const text = await resp.text();
  if (resp.status === 402) {
    return {
      content: [{
        type: "text",
        text: `Payment required. This tool costs ${tool.price} USDC via x402 on Base. Set XUANXUE_PAYMENT_TOKEN env var with a valid payment. Challenge:\n${text}`
      }],
      isError: true
    };
  }
  if (!resp.ok) {
    return { content: [{type: "text", text: `Error ${resp.status}: ${text}`}], isError: true };
  }
  return { content: [{type: "text", text}] };
});

const transport = new StdioServerTransport();
await server.connect(transport);

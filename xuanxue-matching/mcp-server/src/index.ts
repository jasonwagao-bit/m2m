#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const API_BASE = process.env.XUANXUE_API_BASE ?? "https://api.xuanxue.app";
const PAYMENT_HEADER = process.env.XUANXUE_PAYMENT_TOKEN; // x402 payment token

const server = new Server(
  { name: "xuanxue-bazi-matching", version: "0.1.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "bazi_matching",
    description: "Generate detailed Chinese BaZi (八字) compatibility analysis between two birth charts. Returns 0-100 compatibility score, five-elements balance, relationship dynamics narrative, strengths, challenges, and recommendations. Traditional Chinese metaphysics, rule-based (no LLM), sub-200ms response. Pay-per-call $0.02 USDC via x402 on Base.",
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
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name !== "bazi_matching") {
    throw new Error(`Unknown tool: ${request.params.name}`);
  }
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (PAYMENT_HEADER) headers["X-PAYMENT"] = PAYMENT_HEADER;

  const resp = await fetch(`${API_BASE}/agents/v1/bazi-matching`, {
    method: "POST",
    headers,
    body: JSON.stringify(request.params.arguments)
  });
  const text = await resp.text();
  if (resp.status === 402) {
    return {
      content: [{
        type: "text",
        text: `Payment required. This tool costs $0.02 USDC via x402 on Base. Set XUANXUE_PAYMENT_TOKEN env var with a valid payment. Challenge:\n${text}`
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

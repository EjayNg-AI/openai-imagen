# Web Search Tool Integration

- Pick a search API you can call server-side (e.g., SerpAPI, Bing Web Search, Google Programmable Search).
- Add a thin wrapper that calls the API and returns sanitized results (title, URL, snippet); handle rate limits, caching, and errors there.
- Expose the wrapper as a callable tool to the assistant (OpenAI functions/tools schema or an MCP server) with parameters like `query` and optional `top_k`.
- Keep API keys and secrets on your side; only send non-sensitive result data back.
- When the assistant needs web data, it calls the tool; your wrapper runs the real HTTP request and returns the results.

Example tool schema:

```json
{
  "name": "web_search",
  "description": "Search the web and return results.",
  "parameters": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "top_k": { "type": "integer", "default": 5 }
    },
    "required": ["query"]
  }
}
```

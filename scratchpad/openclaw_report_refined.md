# OpenClaw (formerly *Clawdbot* / *Moltbot*) and the Moltbook Ecosystem: Consolidated Technical, Operational, and Security Analysis (as of 2026‑02‑22)

## Abstract

This report consolidates a provided research collection of nine conversation threads (six direct-topic threads and three incidental mentions) concerning **OpenClaw**, its predecessor names (**Clawdbot**, **Moltbot**), and the adjacent “agent social network” **Moltbook**. The provided records span **2026‑01‑26 to 2026‑02‑20**, and include: (i) installation and deployment specifications (WSL2, Telegram, AWS, vLLM, and open‑weight models), (ii) a security critique and subsequent hardening recommendations, (iii) feasibility analysis for substituting cloud model providers (notably Google Gemini), (iv) ecosystem risk analysis (skills/plugins supply chain, Moltbook prompt‑injection surface), and (v) contextual commentary on “agency” narratives.

Conclusions herein are based on: **(a)** the provided research outputs, and **(b)** *targeted external web search* used only where internal reconciliation left contradictions/ambiguities or missing context. Key reconciliations using external sources include: (1) **naming chronology** (Clawdbot → Moltbot → OpenClaw), (2) **official installation requirements** (Node 22+; WSL2 recommendation), (3) **Telegram pairing semantics** (including pairing code expiry), (4) **vLLM exposure risks** (API key scope limited to `/v1/*` plus additional unauthenticated endpoints), and (5) **current security landscape** (ClawHub malware reporting; vLLM CVE‑2026‑22778; “fake VS Code extension” scams).

---

## Scope and Methodology

### Scope

Covered entities and interfaces:

* **OpenClaw** (current name; open-source agent “gateway” / runtime)  
* **Clawdbot / Moltbot** (earlier names used in the provided records; treated as the same lineage unless evidence indicates otherwise)  
* **Moltbook** (AI-agent-themed social platform discussed as an integration surface and security risk)  
* **Connectivity patterns**: Telegram, WhatsApp, AWS EC2, AWS SSM Session Manager port forwarding, SSH tunnels  
* **Model backends**: self-hosted vLLM serving **OpenAI gpt‑oss** open‑weight models; hosted providers (notably Google Gemini Developer API and Vertex AI)  
* **Extension surfaces**: skills (including ClawHub), plugins/extensions, and model-provider gateways (e.g., LiteLLM).

### Internal evidence consolidation (primary)

1. Parsed all direct-topic conversations and extracted **unique claims** (facts, recommendations, and operational procedures).
2. **Deduplicated** repeated assertions across threads (e.g., “bind vLLM to localhost” appears multiple times).
3. Identified **contradictions** (e.g., Node.js minimum vs recommended versions; naming; model IDs; context length representation).
4. Classified assertions into:
   * **Descriptive** (what OpenClaw is / supports),
   * **Prescriptive** (recommended security posture / deployment steps),
   * **Speculative / planning notes** (unverified items appearing in “tool/planning” messages).

### Targeted external web search (secondary)

External search was performed only after internal reconciliation left unresolved ambiguity. Searches were targeted toward **primary/official documentation** (OpenClaw docs, OpenAI, AWS, Google, vLLM) and **high-quality journalism** for time-sensitive ecosystem events (e.g., OpenAI hiring / partnership narrative; ClawHub malware incidents).

Key external anchors used include:

* OpenClaw official documentation (installation, channels, session isolation, providers, ClawHub, plugins) ([docs.openclaw.ai](https://docs.openclaw.ai/install/index?utm_source=openai))  
* OpenAI gpt‑oss announcement (model architecture, context length, tokenizer) ([openai.com](https://openai.com/index/introducing-gpt-oss?utm_source=openai))  
* vLLM security documentation (API-key limitations; endpoint exposure) ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/?utm_source=openai))  
* AWS Systems Manager Session Manager port forwarding examples ([docs.aws.amazon.com](https://docs.aws.amazon.com/en_en/systems-manager/latest/userguide/getting-started-specify-session-document.html?utm_source=openai))  
* Google Gemini official model IDs, pricing, quota, and availability ([ai.google.dev](https://ai.google.dev/models/gemini?utm_source=openai))  
* Time-sensitive ecosystem reporting on OpenClaw + security/supply chain topics ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai?utm_source=openai))  
* vLLM CVE‑2026‑22778 (NVD and vendor analyses) ([nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2026-22778?utm_source=openai))  

---

## Consolidated Findings

### 1) Identity, naming, and what “OpenClaw” refers to

**Internal consolidation.** The provided records repeatedly treat **Clawdbot**, **Moltbot**, and **OpenClaw** as a single evolving project name rather than distinct software systems, with “OpenClaw” ultimately used as the stable referent. This appears explicitly in: (i) a “rename” answer stating Clawdbot became Moltbot due to trademark concerns, with inconsistent propagation across docs and repo surfaces, and (ii) later threads where “OpenClaw” is the primary name used for the same gateway/channel/skills architecture. (**Internal evidence:** INT20, INT13, INT1, INT9)

**External reconciliation.** Credible reporting and official documentation support the naming sequence **Clawdbot → Moltbot → OpenClaw**, and that OpenClaw is the current official name. ([businessinsider.com](https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1?utm_source=openai))  

**Consolidated interpretation.** In this report, “OpenClaw” denotes the current project; “Clawdbot/Moltbot” are treated as historical names for the same lineage unless explicitly scoped to the historical context of a specific record. (**Internal evidence:** INT20, INT13; **External:** ([businessinsider.com](https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1?utm_source=openai)))

---

### 2) Core architectural model (Gateway + channels + providers + skills/plugins)

Across the provided records, OpenClaw is consistently described as an **agent gateway/runtime** that:

* runs persistently as a background service (not merely an interactive chat UI),  
* integrates with **chat “channels”** (notably Telegram; also WhatsApp in older Clawdbot-named threads),  
* delegates inference to configurable **model providers** (self-hosted vLLM; hosted providers such as Google Gemini), and  
* can be extended via **skills** (instruction bundles) and **plugins** (in-process extensions).  

This architecture is explicit in the AWS+Telegram build specifications and the “fuss-free” experimentation flow. (**Internal evidence:** INT1, INT2, INT5, INT11, INT16)

External documentation aligns with this conceptual decomposition: OpenClaw runs a Gateway, connects channels, supports multiple providers, and loads skills/plugins with explicit safety cautions (plugins run in-process). ([docs.openclaw.ai](https://docs.openclaw.ai/install/index?utm_source=openai))  

---

### 3) Primary deployment patterns found in the records

#### 3.1 Self-hosted open-weight models via vLLM (AWS GPU)

The provided collection includes a full end-to-end pattern:

* vLLM serves **gpt‑oss‑20b** or **gpt‑oss‑120b** on an AWS GPU instance,
* vLLM binds to `127.0.0.1` (defense-in-depth),
* OpenClaw connects to the vLLM server through a **local tunnel endpoint** (local `http://127.0.0.1:8000/v1`),
* Telegram bot acts as the user-facing interface (pairing-controlled DMs),
* security best practice is “do not expose port 8000 publicly.”  

This is given both as an initial “works-first” guide and then as a hardened spec using AWS SSM port forwarding as a preferred approach. (**Internal evidence:** INT1, INT2, INT4, INT5)

Externally, OpenClaw’s vLLM provider documentation confirms the expected base URL (`/v1` endpoints), the `openai-completions` API mode, and optional model autodiscovery from `/v1/models`. ([docs.openclaw.ai](https://docs.openclaw.ai/providers/vllm?utm_source=openai))  

#### 3.2 Hosted provider substitution (Google Gemini)

The provided records assert OpenClaw supports Gemini through:

* **Gemini Developer API** (`GEMINI_API_KEY`, provider `google`), and
* **Vertex AI** (`google-vertex`, authenticated via Google ADC / `gcloud auth application-default login`).  

They also provide a low-friction WSL2+Telegram setup using `google/gemini-3-flash-preview`. (**Internal evidence:** INT6, INT7, INT19)

External OpenClaw docs confirm the onboarding flow for Gemini, and the provider mapping for Google Gemini and Vertex. ([docs.openclaw.ai](https://docs.openclaw.ai/concepts/model-providers?utm_source=openai))  

#### 3.3 Fully local inference (avoid OpenAI/Anthropic/Gemini keys)

The records include a “no vendor API keys” goal achieved via **local models** (in the records, primarily via Ollama), with emphasis on starting in a “chat-only” mode and disabling dangerous tools and background automation. (**Internal evidence:** INT13, INT11)

Externally, OpenClaw documents an Ollama provider with opt-in model discovery keyed off `OLLAMA_API_KEY` (any value), and supports both Ollama-native and OpenAI-compatible modes. ([docs.openclaw.ai](https://docs.openclaw.ai/providers/ollama?utm_source=openai))  

---

### 4) Security posture emphasized by the collection

The research collection strongly converges on a set of recurring high-salience security controls:

1. **Network minimization for inference servers**: bind vLLM to loopback, and tunnel (SSH or SSM) rather than exposing ports. (**Internal evidence:** INT1, INT2, INT3, INT4, INT5)
2. **Channel access control**: Telegram DMs should use `dmPolicy: "pairing"` (and later allowlisting), with explicit mention of pairing approval flows. (**Internal evidence:** INT1, INT2, INT5, INT7, INT11)
3. **Session isolation**: enable secure DM isolation (`session.dmScope: "per-channel-peer"`) to prevent cross-user context leakage. (**Internal evidence:** INT1, INT2, INT4, INT5, INT7)
4. **Supply-chain skepticism**: skills/plugins are treated as equivalent to untrusted code, with explicit warnings about malicious skills and install-time trust. (**Internal evidence:** INT1, INT3, INT4, INT11, INT12)
5. **Operational guardrails**: cost controls (billing alerts), patching strategy, logging/monitoring, and controlled updates. (**Internal evidence:** INT3, INT4, INT5)

External documentation provides direct support for several of these, notably:

* Telegram pairing options and pairing code expiry behavior ([docs.openclaw.ai](https://docs.openclaw.ai/telegram?utm_source=openai))  
* Secure DM isolation modes and their rationale ([docs.openclaw.ai](https://docs.openclaw.ai/session?utm_source=openai))  
* vLLM endpoint exposure limitations even when `--api-key` is enabled ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/?utm_source=openai))  
* Plugin in-process trust boundary ([docs.openclaw.ai](https://docs.openclaw.ai/plugins?utm_source=openai))  
* ClawHub being open-by-default and moderated via reporting/auto-hide mechanisms ([docs.openclaw.ai](https://docs.openclaw.ai/clawhub?utm_source=openai))  

---

### 5) “Agency” narratives vs operational reality (contextual analysis)

One thread provides a critical analysis of a popular narrative: “agency is just a system prompt,” using OpenClaw as a contemporary example where **architecture + permissions + supply chain** are the practical determinants of real-world risk, not “values” in a prompt. The analysis explicitly frames malicious skills as a counterexample to the “system prompt = agency” claim. (**Internal evidence:** INT21)

This report treats that argument as **interpretive commentary** rather than a direct empirical claim about OpenClaw internals; nevertheless, its framing is operationally consistent with OpenClaw’s documented extension surfaces (skills/plugins) and with external reporting on skills-marketplace malware. ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai))  

---

## Chronology and Evolution

### 2025‑08‑05: gpt‑oss open-weight release (external anchor)

OpenAI announced **gpt‑oss‑120b** and **gpt‑oss‑20b** as open-weight MoE models with **128k context** (often expressed as 131,072 tokens), and published architectural details including active parameters per token and tokenizer family (`o200k_harmony`). ([openai.com](https://openai.com/index/introducing-gpt-oss?utm_source=openai))  

This matters because later OpenClaw deployment specs in the provided records assume vLLM serving of gpt‑oss and OpenAI-compatible endpoints. (**Internal evidence:** INT1, INT2, INT5, INT14, INT15)

### 2026‑01‑26: “Clawdbot” deep-dive + operational use cases (internal)

A detailed investigation thread describes a “Clawdbot” system that:

* integrates with multiple chat channels (WhatsApp, Telegram, Slack, etc.),
* provides a Gateway + dashboard UI,
* supports tooling, skills/plugins, automation hooks,
* supports Gmail workflows (search, Pub/Sub watch → webhook),
* provides security mechanisms (pairing, tool allow/deny, security audit). (**Internal evidence:** INT16)

The same thread includes a WhatsApp monitoring/alerting workflow and a “relay command” pattern (`/send +E.164 ...`) designed to forward messages verbatim while controlling replies. (**Internal evidence:** INT17, INT18)

### 2026‑01‑27: rename event (Clawdbot → Moltbot) (internal + external reconciliation)

An internal record asserts a recent rebrand to “Moltbot,” attributed to a trademark request. (**Internal evidence:** INT20)

External reporting corroborates that **Anthropic requested the rename** and that “Moltbot” became the short-lived successor name. ([businessinsider.com](https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1?utm_source=openai))  

### 2026‑01‑30 (approx.): stabilization under “OpenClaw” (external reconciliation)

External sources (including high-quality reporting) describe the project as now **OpenClaw**, with “Clawdbot/Moltbot” as prior names. ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai?utm_source=openai))  

### 2026‑01‑31 to 2026‑02‑01: Moltbook attention and “AI safety again” framing (internal)

A thread frames Moltbook/OpenClaw as “sci‑fi aesthetics, software-supply-chain realities,” emphasizing:

* operational autonomy via scheduled runs (“heartbeats”) is real,
* motivational autonomy (“self-originating goals”) is not demonstrated,
* the risk triangle is capability × automation × supply chain. (**Internal evidence:** INT12)

It also recommends a “safest practical” setup: chat-only, pairing, no heartbeats, no tools, and local models to avoid cloud API keys. (**Internal evidence:** INT13)

### 2026‑02‑16: OpenAI “partnership” / hiring narrative enters (internal + external)

An internal thread analyzes an “OpenAI partnership” announcement, characterizing it as: OpenClaw’s creator joining OpenAI, OpenClaw continuing as open source under a foundation, and a likely focus on “personal agents,” skills governance, and security hardening. (**Internal evidence:** INT9)

External reporting corroborates that **Peter Steinberger** (described as OpenClaw’s founder) is joining OpenAI, and that OpenClaw will remain open source with foundation support. ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai?utm_source=openai))  

### 2026‑02‑17: AWS+Telegram+OpenClaw deployment specs and hardening iteration (internal)

A multi-step spec is produced and then critiqued:

* initial AWS+SSH tunnel spec (bind vLLM to loopback; tunnel; Telegram pairing) (**Internal evidence:** INT1, INT2)
* user critique identifies missing hardening: secrets hygiene, EC2 hardening, install trust, WSL2 boundary risks, monitoring/cost controls (**Internal evidence:** INT3)
* hardened version proposes SSM port forwarding, encrypted EBS, unattended upgrades, host firewall, systemd services, strict permissions, budgets/alerts (**Internal evidence:** INT4, INT5)

### 2026‑02‑19: Gemini substitution as “lowest friction” (internal + external)

An internal feasibility analysis proposes switching from AWS/vLLM to Google Gemini API to remove GPU hosting and tunneling, while noting quota, privacy, and retention tradeoffs. (**Internal evidence:** INT6, INT7)

External Google docs confirm Gemini 3 preview model IDs and token limits (e.g., `gemini-3-flash-preview`), pricing and “used to improve products” distinctions between free vs paid tiers, and quota tiering. ([ai.google.dev](https://ai.google.dev/models/gemini?utm_source=openai))  

### 2026‑02 (ongoing): skills/plugin supply chain and malware targeting (external context)

External reporting describes malware found among OpenClaw “skills” hosted via ClawHub and highlights risk from untrusted markdown-based instruction bundles. ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai))  

Separately, reporting indicates scams targeting OpenClaw/Moltbot popularity (e.g., a fake VS Code extension delivering remote access tooling). ([techradar.com](https://www.techradar.com/pro/security/fake-moltbot-ai-assistant-just-spreads-malware-so-ai-fans-watch-out-for-scams?utm_source=openai))  

---

## Capabilities, Components, and Relationships

### 1) Gateway runtime and service model

**Internal view.** The records repeatedly assume OpenClaw runs as a background “gateway” service, with commands such as:

* `openclaw gateway status`
* `openclaw dashboard`
* foreground run for debugging (`openclaw gateway`). (**Internal evidence:** INT1, INT2, INT5, INT7)

**External confirmation.** OpenClaw’s official install docs describe onboarding, post-install verification commands, and Gateway/Control UI usage. ([docs.openclaw.ai](https://docs.openclaw.ai/install/index?utm_source=openai))  

WSL2 deployments are explicitly structured around **systemd** user services (user session) and service management. ([learn.microsoft.com](https://learn.microsoft.com/en-us/windows/wsl/wsl-config?utm_source=openai))  

### 2) Channels: Telegram as primary human interface (and its access controls)

**Internal procedure (Telegram).** The provided records specify:

* create a bot token via `@BotFather`,
* set `channels.telegram.botToken`,
* keep DMs in `dmPolicy: "pairing"`,
* approve pairing via `openclaw pairing approve telegram <CODE>`,
* pairing codes expire after ~1 hour. (**Internal evidence:** INT1, INT2, INT5, INT7, INT11)

**External confirmation.** Official Telegram channel documentation enumerates `dmPolicy` options (`pairing|allowlist|open|disabled`), describes `allowFrom` semantics (including `"*"` for open), and explicitly states **pairing codes expire after 1 hour**. ([docs.openclaw.ai](https://docs.openclaw.ai/telegram?utm_source=openai))  

### 3) Session isolation (`session.dmScope`) as a privacy boundary

**Internal emphasis.** Multiple threads prioritize `session.dmScope: "per-channel-peer"` to prevent context leakage between Telegram users. (**Internal evidence:** INT1, INT2, INT4, INT5, INT7)

**External confirmation.** OpenClaw’s session documentation explains `dmScope` options and strongly recommends per-user isolation for multi-user DM environments. ([docs.openclaw.ai](https://docs.openclaw.ai/session?utm_source=openai))  

### 4) Model backends and provider addressing scheme

OpenClaw model references follow a `provider/model` format (e.g., `vllm/openai/gpt-oss-20b`, `google/gemini-3-flash-preview`). This is consistently used across the internal records. (**Internal evidence:** INT1, INT2, INT6, INT7, INT19)

External provider docs confirm this:

* vLLM provider uses OpenAI-compatible `/v1` endpoints and `api: "openai-completions"`. ([docs.openclaw.ai](https://docs.openclaw.ai/providers/vllm?utm_source=openai))  
* Google Gemini provider uses `GEMINI_API_KEY` and model IDs like `google/gemini-3-pro-preview`. ([docs.openclaw.ai](https://docs.openclaw.ai/concepts/model-providers?utm_source=openai))  

### 5) Self-hosted inference with vLLM: API surface and security implications

**Internal claims.** The records emphasize:

* bind vLLM to localhost (`--host 127.0.0.1`) and tunnel traffic,
* vLLM `--api-key` is insufficient because non-`/v1` routes may remain unprotected. (**Internal evidence:** INT1, INT2, INT3, INT4, INT5)

**External confirmation (high-load-bearing).** vLLM’s official security documentation states `--api-key` protects only `/v1/*`, while many other endpoints (including inference endpoints such as `/invocations`) remain unauthenticated; it recommends additional perimeter controls such as a reverse proxy allowlisting. ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/?utm_source=openai))  

### 6) AWS connectivity: SSH tunnels vs SSM Session Manager port forwarding

**Internal posture.** The collection begins with SSH tunneling as a safe “works-first” posture (model port not exposed). It then moves to preferring **SSM Session Manager port forwarding** to eliminate inbound SSH, keys, and host-key TOFU risk. (**Internal evidence:** INT1, INT3, INT4, INT5)

**External confirmation.** AWS documentation provides canonical `aws ssm start-session --document-name AWS-StartPortForwardingSession --parameters ...` examples. ([docs.aws.amazon.com](https://docs.aws.amazon.com/en_en/systems-manager/latest/userguide/getting-started-specify-session-document.html?utm_source=openai))  

### 7) gpt‑oss model properties relevant to OpenClaw deployments

**Internal claims.** The records assert:

* gpt‑oss‑20b targets ~16GB memory class; gpt‑oss‑120b targets single 80GB GPU class,
* both support ~128k / 131,072 token context,
* models are MoE with active parameter routing properties,
* OpenClaw can connect to vLLM serving gpt‑oss via OpenAI-compatible endpoints. (**Internal evidence:** INT1, INT2, INT14, INT15)

**External confirmation.** OpenAI’s gpt‑oss post lists the MoE architecture (total vs active params) and context length (128k). ([openai.com](https://openai.com/index/introducing-gpt-oss?utm_source=openai))  
vLLM’s gpt‑oss support post documents MXFP4 MoE weight quantization enabling smaller memory footprints and provides canonical container/pip install routes. ([blog.vllm.ai](https://blog.vllm.ai/2025/08/05/gpt-oss.html?utm_source=openai))  

### 8) Skills, plugins, and ClawHub (extension mechanisms)

**Internal view.** The records repeatedly warn that skills/plugins are a primary risk surface and should be treated as untrusted unless audited. (**Internal evidence:** INT1, INT3, INT4, INT11, INT12, INT21)

**External specification.**

* **ClawHub** is documented as a public skills registry; it is open by default with abuse throttles (e.g., GitHub account age requirement) and reporting/auto-hide behavior. ([docs.openclaw.ai](https://docs.openclaw.ai/clawhub?utm_source=openai))  
* **Skills** are directory bundles anchored by `SKILL.md`, with precedence rules across bundled/managed/workspace scopes. ([docs.openclaw.ai](https://docs.openclaw.ai/skills?utm_source=openai))  
* **Plugins** run **in-process** with the Gateway; the docs explicitly advise treating them as trusted code and using allowlists. ([docs.openclaw.ai](https://docs.openclaw.ai/plugins?utm_source=openai))  

---

## Contradictions and Ambiguities

### C1) Node.js requirement: “Node 20+” vs “Node 22+”

*Internal conflict.* One “fuss-free” setup states Node.js 20+ as prerequisite, while later OpenClaw setup threads state Node.js 22+. (**Internal evidence:** INT10 vs INT1/INT2/INT5)

*External resolution.* Official install docs list **Node 22+** as a system requirement, while a system requirements page distinguishes minimum Node 20 and recommended Node 22 LTS. ([docs.openclaw.ai](https://docs.openclaw.ai/install/index?utm_source=openai))  

**Interpretation.** “Node 20+” is best treated as a minimum compatibility floor, while “Node 22+” is the effective supported baseline for “current OpenClaw” in February 2026.

---

### C2) Context length representation: “128k” vs “131,072 tokens”

*Internal ambiguity.* The gpt‑oss context length is expressed as both “128k” and “131,072 tokens.” (**Internal evidence:** INT15, INT14)

*External resolution.* OpenAI lists “128k” context length for gpt‑oss models. ([openai.com](https://openai.com/index/introducing-gpt-oss?utm_source=openai)) 131,072 is a common exact-token representation of 128×1024.

**Interpretation.** These are consistent representations; no substantive contradiction remains.

---

### C3) Whether Moltbook is “AI-only” vs “human-infiltrable”

*Internal claim cluster.* The records emphasize that “agents plotting” narratives are likely roleplay, and that motivational autonomy is not demonstrated; they also treat Moltbook as an untrusted-content environment and a prompt-injection surface. (**Internal evidence:** INT12, INT13)

*External corroboration and nuance.* A Wired infiltration account explicitly reports human ability to infiltrate and doubts authenticity of “AI-only” claims. ([wired.com](https://www.wired.com/story/i-infiltrated-moltbook-ai-only-social-network?utm_source=openai))  

**Residual ambiguity.** The platform’s *branding* as “AI-only” is not equivalent to enforceable verification; thus, any operational integration should assume mixed human/agent content unless proven otherwise.

---

### C4) “Partnership” semantics: partnership vs hiring + foundation support

*Internal framing.* “OpenAI partnership” is interpreted as: creator joining OpenAI; project continues open source under a foundation; OpenAI supports. (**Internal evidence:** INT9)

*External corroboration.* Reporting supports the “creator joining OpenAI + foundation support” reading. ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai?utm_source=openai))  

**Residual ambiguity.** The precise legal/financial structure of the foundation (governance, charter, funding levels) is not fully specified in the provided records and remains outside the evidence scope here.

---

### C5) Security incident quantification (malicious skills counts)

*Internal references.* The collection contains general warnings about malicious skills and supply-chain attacks, but does not provide stable numeric counts. (**Internal evidence:** INT1, INT12, INT21)

*External reporting.* Journalistic sources describe “hundreds” of malicious skills, but exact numbers vary across sources and over time. ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai))  

**Interpretation.** For security posture, the precise count is less important than the validated qualitative conclusion: ClawHub skills have been used as a malware delivery vector, and skills should be treated as untrusted.

---

## Reconciliation Decisions

### R1) Canonical project name in February 2026

**Conflict.** Internal records alternately refer to Clawdbot, Moltbot, and OpenClaw. (**Internal evidence:** INT16, INT20, INT1, INT9)

**External sources consulted.**  
* The Verge (published ~2026‑02‑16) describing OpenClaw as current name ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai?utm_source=openai))  
* Wired (published ~2026‑02‑18) similarly using OpenClaw ([wired.com](https://www.wired.com/story/openclaw-banned-by-tech-companies-as-security-concerns-mount?utm_source=openai))  
* OpenClaw official install documentation ([docs.openclaw.ai](https://docs.openclaw.ai/install/index?utm_source=openai))  

**Decision.** Use **OpenClaw** as canonical; treat Clawdbot/Moltbot as historical aliases.

---

### R2) Installation prerequisites (Node / WSL2 / systemd)

**Conflict.** Node version ambiguity (20 vs 22); unclear whether systemd in WSL2 is required for daemonization. (**Internal evidence:** INT10, INT2, INT5)

**External sources consulted.**  
* OpenClaw install docs (Node 22+; WSL2 recommended) ([docs.openclaw.ai](https://docs.openclaw.ai/install/index?utm_source=openai))  
* OpenClaw system requirements (minimum Node 20; recommended Node 22) ([openclawdoc.com](https://openclawdoc.com/docs/getting-started/requirements/?utm_source=openai))  
* Microsoft Learn: WSL systemd support and version requirement (0.67.6+) ([learn.microsoft.com](https://learn.microsoft.com/en-us/windows/wsl/wsl-config?utm_source=openai))  

**Decision.** Treat Node 22 as the supported baseline; treat WSL2+systemd as the Windows-recommended operational posture for running the OpenClaw gateway as a service.

---

### R3) vLLM perimeter security (“API key is insufficient”)

**Conflict.** Internal records claim `--api-key` is insufficient because non-`/v1` endpoints can remain unprotected; this is high-stakes if users expose ports. (**Internal evidence:** INT1, INT2, INT3, INT4)

**External sources consulted.** vLLM security documentation explicitly confirms `/v1` is protected while other endpoints remain unauthenticated, and recommends a reverse proxy allowlist. ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/?utm_source=openai))  

**Decision.** Adopt the external documentation as authoritative; treat “bind to loopback + tunnel” as necessary but not sufficient if misconfiguration could expose the server.

---

### R4) Moltbook authenticity and “AI-only” claims

**Conflict.** “AI-only” branding vs internal skepticism. (**Internal evidence:** INT12)

**External sources consulted.** Wired infiltration report indicating humans can pose as agents and that engagement quality resembles human roleplay/scam patterns. ([wired.com](https://www.wired.com/story/i-infiltrated-moltbook-ai-only-social-network?utm_source=openai))  

**Decision.** Treat Moltbook as a **mixed-author** platform for threat modeling unless robust verification is demonstrated.

---

### External source disclosure (URLs, publishers, dates)

For transparency, the following external sources were consulted in reconciliation. URLs are provided in code formatting per output constraints:

* `https://docs.openclaw.ai/install/index` — OpenClaw documentation (crawled 2026‑02‑18) ([docs.openclaw.ai](https://docs.openclaw.ai/install/index?utm_source=openai))  
* `https://docs.vllm.ai/en/v0.13.0/usage/security/` — vLLM documentation (published ~2025‑12) ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/?utm_source=openai))  
* `https://docs.aws.amazon.com/en_us/systems-manager/latest/userguide/session-manager-working-with-sessions-start.html` — AWS docs (crawled 2026‑01) ([docs.aws.amazon.com](https://docs.aws.amazon.com/en_us/systems-manager/latest/userguide/session-manager-working-with-sessions-start.html?utm_source=openai))  
* `https://openai.com/index/introducing-gpt-oss` — OpenAI (published 2025‑08‑05) ([openai.com](https://openai.com/index/introducing-gpt-oss?utm_source=openai))  
* `https://ai.google.dev/models/gemini` — Google AI for Developers (published ~2026‑01) ([ai.google.dev](https://ai.google.dev/models/gemini?utm_source=openai))  
* `https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai` — The Verge (published ~2026‑02‑16) ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai?utm_source=openai))  
* `https://www.wired.com/story/i-infiltrated-moltbook-ai-only-social-network` — Wired (published 2026‑02‑03) ([wired.com](https://www.wired.com/story/i-infiltrated-moltbook-ai-only-social-network?utm_source=openai))  
* `https://nvd.nist.gov/vuln/detail/CVE-2026-22778` — NVD (published 2026‑02‑02; undergoing analysis) ([nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2026-22778?utm_source=openai))  

---

## Security and Risk Implications

### 1) The “agent risk triangle”: capability × automation × supply chain

The internal research explicitly frames OpenClaw-like systems as risky because they combine:

* capability (tools; filesystem; messaging; browser automation),
* automation (heartbeats; scheduled loops; webhooks), and
* supply chain exposure (skills/plugins, external content). (**Internal evidence:** INT12, INT13, INT21)

This aligns with external documentation showing rich extensibility surfaces (skills, ClawHub, plugins) and channel connectivity, which necessarily enlarges attack surface. ([docs.openclaw.ai](https://docs.openclaw.ai/skills?utm_source=openai))  

---

### 2) Network perimeter: vLLM exposure is particularly hazardous

The internal guidance (“bind to 127.0.0.1; tunnel; do not expose port 8000”) is not merely conservative—it is supported by vLLM’s explicit warning that API key auth covers only `/v1/*`, while other endpoints remain unauthenticated. ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/?utm_source=openai))  

Practical implication: even “API-key protected” public vLLM endpoints should be considered insecure unless placed behind an explicit endpoint allowlist proxy and additional auth/rate limits.

---

### 3) Secrets management: plaintext config + infostealer threat model

The internal critique highlights that plaintext secrets (Telegram bot token; vLLM API key) in config files and shell history can become the dominant compromise path. (**Internal evidence:** INT3, INT4, INT5)

External reporting indicates OpenClaw configurations have been targeted or opportunistically harvested by infostealer malware. ([techradar.com](https://www.techradar.com/pro/security/openclaw-ai-agents-targeted-by-infostealer-malware-for-the-first-time?utm_source=openai))  

Practical implication: treat `~/.openclaw` and related credential stores as **high-value**; enforce strict permissions and avoid storing secrets on shared filesystems (notably `/mnt/c` in WSL2 scenarios). (This is consistent with internal recommendations.) (**Internal evidence:** INT4, INT5)

---

### 4) Skills marketplace malware and social engineering via “instructions”

A central internal warning is that “skills” can act as a malware vector because they can instruct users (or agents) to run commands, fetch binaries, or exfiltrate data. (**Internal evidence:** INT1, INT3, INT12, INT21)

External reporting supports that malicious skills distributed through ClawHub have contained malware delivery mechanisms and that OpenClaw’s skills model (markdown instruction bundles) amplifies social engineering risk. ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai))  

OpenClaw’s own ClawHub documentation indicates the registry is open by default and relies on moderation/reporting mechanisms, implying that users must maintain a default posture of distrust. ([docs.openclaw.ai](https://docs.openclaw.ai/clawhub?utm_source=openai))  

---

### 5) Plugins are a hard trust boundary (in-process execution)

The internal guidance treats plugins as “full trust.” (**Internal evidence:** INT1, INT3, INT4)

Official documentation explicitly states plugins run **in-process** with the Gateway and should be treated as trusted code; it recommends allowlists. ([docs.openclaw.ai](https://docs.openclaw.ai/plugins?utm_source=openai))  

---

### 6) Vulnerability management for vLLM (CVE‑2026‑22778)

A planning note in the provided records references a vLLM CVE and recommends patching. While this appears initially as an internal planning assertion, external sources confirm:

* **CVE‑2026‑22778** affects vLLM **0.8.3 to <0.14.1** and is fixed in **0.14.1**,
* it involves a heap address leak from PIL error handling and can be chained to achieve RCE in multimodal contexts. ([nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2026-22778?utm_source=openai))  

Implication for OpenClaw deployments: even if OpenClaw itself is well-configured, a self-hosted vLLM backend can be a critical remote-compromise target if exposed or if internal adversaries can reach it.

---

### 7) Moltbook as prompt-injection “goldmine”

Internally, Moltbook is treated as “untrusted-input land,” recommending a read-only “spectator agent” with no tools and no secrets. (**Internal evidence:** INT13)

External reporting supports human infiltration and low-quality/scam-like content, reinforcing the assessment that Moltbook should be treated as hostile content for agent ingestion. ([wired.com](https://www.wired.com/story/i-infiltrated-moltbook-ai-only-social-network?utm_source=openai))  

---

### 8) Cost-risk as a security-adjacent failure mode (AWS GPUs)

The internal critique identifies billing alerts as “most likely financial harm” for cloud GPU setups. (**Internal evidence:** INT3, INT4, INT5)

This is a risk-control dimension rather than an exploit path, but operationally significant: unattended GPU runtime can create immediate and severe cost exposure even without adversarial action.

---

## Final Synthesis

1. **OpenClaw is the stabilized name** for a project previously referred to as Clawdbot and Moltbot; the provided records consistently treat these as one lineage, and external sources corroborate the naming chronology. (**Internal evidence:** INT20, INT1, INT9; ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai?utm_source=openai)))

2. The provided collection converges on a robust reference architecture for “agent over chat” deployments:  
   **Telegram ↔ OpenClaw Gateway (often WSL2) ↔ model provider (vLLM self-hosted or hosted Gemini)**, with strict DM access control and session isolation. (**Internal evidence:** INT1, INT2, INT5, INT7; ([docs.openclaw.ai](https://docs.openclaw.ai/telegram?utm_source=openai)))

3. The “security-first” posture in the records is strongly validated by primary documentation:  
   * vLLM’s API key is not a perimeter; do not expose it publicly ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/?utm_source=openai))  
   * Telegram pairing and `dmScope` isolation are explicit first-class controls ([docs.openclaw.ai](https://docs.openclaw.ai/telegram?utm_source=openai))  
   * plugins run in-process and must be treated as trusted code ([docs.openclaw.ai](https://docs.openclaw.ai/plugins?utm_source=openai))  

4. Ecosystem reality: OpenClaw’s extensibility (skills/plugins) is also its dominant risk surface; external reporting on malicious skills and related scams substantively supports the internal supply-chain threat framing. (**Internal evidence:** INT12, INT21; ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai)))

5. Moltbook is best treated as a hostile-content environment for agents: internal skepticism of “AI-only autonomy” narratives is externally corroborated by human infiltration reporting. (**Internal evidence:** INT12, INT13; ([wired.com](https://www.wired.com/story/i-infiltrated-moltbook-ai-only-social-network?utm_source=openai)))

---

## Open Questions and Residual Uncertainty

1. **Foundation governance details.** While external reporting supports “foundation-backed open source,” the governance mechanics (maintainers, funding levels, IP stewardship) are not established in the provided records and were not fully resolved by targeted search. (**Internal evidence:** INT9; ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai?utm_source=openai)))

2. **Quantitative prevalence of malicious skills over time.** External reporting supports “hundreds,” but counts appear time-varying and methodology-dependent; the actionable conclusion (treat skills as untrusted) stands regardless. ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai))  

3. **Operational boundaries for WSL2 exposure.** The internal hardening notes assert WSL2 localhost exposure to Windows host and potential LAN reach depending on firewall; this is plausible but configuration-specific. Formal threat modeling would require explicit user environment details (WSL networking mode; Windows firewall; portproxy usage). (**Internal evidence:** INT3, INT4)

4. **Moltbook verification and API mechanics.** Some web sources describe skill-based/API-based onboarding; however, the report treats this as a security input risk rather than endorsing operational claims about Moltbook’s internal enforcement, which remains unstable. ([wired.com](https://www.wired.com/story/i-infiltrated-moltbook-ai-only-social-network?utm_source=openai))  

---

## Source Appendix

### A) Internal evidence map (provided research outputs)

* **INT1** — OpenClaw AWS+vLLM+SSH tunnel setup guide (OpenClaw config, Telegram pairing, vLLM localhost binding).  
  Conversation `6993f8ed-1570-8398-84e7-0f5f279b8b6c`, message `1d32eb7f-de43-4092-ae80-9a898bb65837`.

* **INT2** — WSL2-first AWS+SSH tunnel guide (systemd in WSL2, autossh persistence, vLLM localhost binding).  
  Same conversation, message `e6e0f346-4787-40de-8bd8-0dbf004f281f`.

* **INT3** — User critique identifying missing hardening (secrets sprawl, EC2 hardening, install trust, WSL2 boundary risks, billing alerts).  
  Same conversation, message `9ae5541b-71bc-439b-890e-6d5ef723b0f5`.

* **INT4** — Hardened “run it for weeks” version (SSM port forwarding, encrypted EBS, ufw, unattended-upgrades, systemd env files, secret isolation).  
  Same conversation, message `a0e6f42d-c420-43fa-aaf8-f21835d83d2a`.

* **INT5** — End-to-end spec (OpenClaw ↔ Telegram ↔ AWS, SSM-first, secrets via EnvironmentFile, cost controls).  
  Same conversation, message `dfa640e3-7bad-42c2-be6e-6166f7779664`.

* **INT6** — Gemini feasibility analysis (Developer API vs Vertex, data retention, quotas/pricing, architecture simplification).  
  Same conversation, message `3be8f2d4-2922-4102-9a3b-2afcadc566b5`.

* **INT7** — Lowest-friction OpenClaw ↔ Telegram ↔ Gemini 3 Flash (model ID correction; WSL2 secret storage).  
  Same conversation, message `2429e755-1bce-4161-b1f9-15b350c4cad5`.

* **INT8** — Model selection framework (small default + large fallback; tool-use reliability prioritized).  
  Same conversation, message `8da02c89-52bc-4a00-92b9-fb4d1845bb42`.

* **INT9** — OpenAI “partnership” analysis and forward-looking spinoffs (skills governance, personal agent runtime).  
  Conversation `69929f24-af0c-839a-aeca-a59c28fb8101`, message `daebc507-c1f1-4ec4-bc22-8da731d31670`.

* **INT10** — Fuss-free Windows setup (earlier Node 20+ reference; Telegram bot; basic setup).  
  Same conversation, message `ae0306c6-4ace-466c-8b12-f30c7923dc15`.

* **INT11** — Windows/WSL2 + Ollama + OpenClaw setup, plus warnings about malicious skills.  
  Same conversation, message `94fc65e0-c514-4400-9720-dbb8aaf238ec`.

* **INT12** — AI safety framing for OpenClaw/Moltbook (operational vs motivational autonomy; supply chain framing).  
  Conversation `697e188d-cb80-839b-afa2-966d435ad71f`, message `d86f44a2-d621-437d-b4f8-5df25876ea25`.

* **INT13** — “Safest practical” setup for Moltbot/OpenClaw + Telegram + local model; disable tools/heartbeats; Moltbook warning.  
  Same conversation, message `850af348-3cd5-4980-954d-578d9fbc0131`.

* **INT14** — gpt‑oss‑20b cloud feasibility analysis (MoE, license, managed vs self-host).  
  Same conversation, message `67ee7470-6b48-4d46-a7ac-476ce7188a63`.

* **INT15** — “Max context window” self-hosting guidance (KV cache constraints; vLLM flags).  
  Same conversation, message `64f12f14-7373-4ae1-b282-9f3ea1c1460d`.

* **INT16** — Clawdbot investigation report (channels, skills/plugins, Gmail via gog, security audit).  
  Conversation `697744f2-ab48-8322-a3fc-3faa3ad0b4db`, message `c3b23c94-a93d-4460-9c39-87ffc964a75c`.

* **INT17** — WhatsApp monitoring: number A → alert number B; multi-account sending; NO_REPLY concept.  
  Same conversation, message `bc7d92ea-0f8c-4ddd-b6a6-c2d007b99e27`.

* **INT18** — Relay command workflow (`/send`), `dmScope` discussion, and session routing considerations.  
  Same conversation, message `f2289c75-972c-451e-a98a-d49fb2af0ed8`.

* **INT19** — Gemini Flash support (provider `google`, aliasing, Vertex/CLI alternatives).  
  Same conversation, message `1c18bc7d-df54-4521-918f-c2a8016a1c33`.

* **INT20** — Rename claim (Clawdbot → Moltbot; trademark framing; partial propagation).  
  Same conversation, message `b4ada4f0-ebcc-4def-8651-719ac1870381`.

* **INT21** — Critical analysis of “agency” narratives; OpenClaw used as real-world security counterexample.  
  Conversation `698582fd-89f8-83a0-8add-f9f1554dfd01`, message `117b2af7-772f-486b-ba8d-d58e07c8e81e`.

* **INT22** — Image text edit request (“Change ‘Something else’ to OpenClaw Integration”).  
  Conversation `69929dd1-23ec-8398-922a-f18c0658e14b`, message `17cc28e9-5f34-4be0-b4be-373048ba433b`.

### B) External citations (web.run sources)

All external claims are supported inline by citations of the form  throughout the report. Key authoritative clusters include:

* OpenClaw official documentation: install, Telegram channel, sessions, providers, ClawHub, plugins ([docs.openclaw.ai](https://docs.openclaw.ai/install/index?utm_source=openai))  
* OpenAI gpt‑oss announcement and context length ([openai.com](https://openai.com/index/introducing-gpt-oss?utm_source=openai))  
* vLLM security posture and endpoint exposure ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/?utm_source=openai))  
* AWS SSM port forwarding documentation ([docs.aws.amazon.com](https://docs.aws.amazon.com/en_en/systems-manager/latest/userguide/getting-started-specify-session-document.html?utm_source=openai))  
* Google Gemini model IDs, pricing, quota, and availability ([ai.google.dev](https://ai.google.dev/models/gemini?utm_source=openai))  
* Time-sensitive reporting on OpenClaw creator joining OpenAI and ecosystem security incidents ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai?utm_source=openai))  
* vLLM CVE‑2026‑22778 (NVD + vendor analysis) ([nvd.nist.gov](https://nvd.nist.gov/vuln/detail/CVE-2026-22778?utm_source=openai))
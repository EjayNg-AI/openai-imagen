## 1. Executive Summary

- **OpenClaw is the current name** of an open‑source “personal agent” / autonomous assistant software stack that runs on a user-controlled host (laptop, WSL2 VM, VPS, etc.) and exposes the agent through messaging channels (Telegram/WhatsApp/Discord/etc.) and other surfaces. It is implemented as a **Gateway** service plus configuration/state on disk. ([docs.openclaw.ai](https://docs.openclaw.ai/install/index))  
- **Clawdbot → Moltbot → OpenClaw** is a rapid rebrand sequence that occurred in late January 2026. The **Moltbot** rename was driven by a trademark request from Anthropic; OpenClaw became the “final” name shortly after. ([businessinsider.com](https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1))  
- **Peter Steinberger** is consistently identified (in the dataset and on the open web) as the creator/founder of the project and the person driving its technical direction. ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/))  
- On **February 15, 2026**, reporting and primary quotes indicate Steinberger **joined OpenAI**, while OpenClaw will remain **open source** and “live in a foundation” that OpenAI will continue to support. This is better characterized as an **acqui-hire / talent move + OSS foundation support**, not a classic product acquisition (though many writeups use “partnership” colloquially). ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/))  
- **Moltbook** is a separate product: a “Reddit-like” social network marketed as “for AI agents,” with onboarding via a prompt instructing an agent to read a `skill.md` and follow instructions. It is not synonymous with OpenClaw, but is tightly associated with it culturally and through integration patterns. ([moltsbooks.com](https://moltsbooks.com/?utm_source=openai))  
- The dataset and external sources converge on a core safety thesis: most major risks are **operational** (misconfiguration, secrets sprawl, untrusted “skills/plugins,” supply chain, exposed ports, weak access control), not “spontaneously goal-seeking AIs.” ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/security?utm_source=openai))  
- Several **real-world security incidents** are reported in February 2026:  
  - **Malicious skills on ClawHub** (hundreds reported by multiple outlets, with varying counts/timelines). ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai))  
  - **Moltbook database exposure** (Wiz findings: exposed API tokens/emails/DMs due to misconfigured Supabase/RLS). ([techradar.com](https://www.techradar.com/pro/security/ai-agent-social-media-network-moltbook-is-a-security-disaster-millions-of-credentials-and-other-details-left-unsecured))  
  - **Infostealer exfiltration of OpenClaw configs/secrets** reported via Hudson Rock coverage. ([techradar.com](https://www.techradar.com/pro/security/openclaw-ai-agents-targeted-by-infostealer-malware-for-the-first-time?utm_source=openai))  

---

## 2. Consolidated Fact Base (exhaustive, de-duplicated)

### 2.1 Dataset scope, provenance, and limitations

- The dataset topic is `"OpenClaw / Clawdbot / Moltbot"` with keyword regex `clawdbot|moltbot|openclaw`. (Dataset root)  
- The dataset was assembled at **2026‑02‑22T07:19:36Z**. (Dataset root)  
- It aggregates content from two ChatGPT conversation-history archives and deduplicates conversation IDs by latest `update_time`. (Dataset root)  
- It reports **9 matched conversation IDs**, with **6 direct-topic threads** and **3 incidental mentions**. (Dataset root)  
- Many assistant messages inside the dataset contain inline “citations” of the form `turnX...`; these refer to browsing done *in those historical chats*, not in the current run. For this report, those are treated as **non-verifiable within the JSON itself**, and are reconciled using **fresh web evidence** when needed.

**Internal evidence IDs used below** are defined in §9.1.

---

### 2.2 Entity definitions and relationships (OpenClaw, Clawdbot, Moltbot, ClawHub, Moltbook)

#### OpenClaw (software)

- OpenClaw is an open-source repository at `openclaw/openclaw` with the tagline “Your own personal AI assistant. Any OS. Any Platform. The lobster way.” ([github.com](https://github.com/openclaw/openclaw))  
- The GitHub repository indicates **MIT license**. ([github.com](https://github.com/openclaw/openclaw))  
- The repository shows very large community activity (e.g., ~217k stars and ~40.8k forks at time of crawl), which is **time-volatile** but establishes that it is “viral-scale” OSS. ([github.com](https://github.com/openclaw/openclaw))  

#### Clawdbot and Moltbot (historical names / branding)

- The dataset repeatedly treats “Clawdbot” and “Moltbot” as names for the same lineage that ends in OpenClaw. Examples:  
  - A direct-topic thread is titled “Clawdbot Investigation Request” (I‑C1).  
  - Another is titled “Clawdbot Moltbot Timeline” (I‑T1).  
  - The “OpenClaw Setup Guide” thread is explicitly OpenClaw-focused but uses the same architecture pattern. (I‑S1)
- External reporting confirms **Clawdbot renamed to Moltbot** on **2026‑01‑27** after Anthropic reached out, and Steinberger said he was “forced” to rename; the mascot was renamed to “Molty.” ([businessinsider.com](https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1))  
- External reporting (TechCrunch) states the name changed **again** to OpenClaw because Steinberger “liked the new name better” (in addition to the initial trademark pressure). ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/))  

#### ClawHub (public “skills” registry)

- The dataset refers to a “skills marketplace” and warns it has been a malware target (I‑S1, I‑P1, I‑T1).  
- OpenClaw documentation defines **ClawHub** as the public registry for OpenClaw skills, describes it as free/public, and states skills are “just a folder with a `SKILL.md` file (plus supporting text files).” It also states the ClawHub site is `clawhub.ai` and provides a CLI installation path (`npm i -g clawhub` / `pnpm add -g clawhub`). ([docs.openclaw.ai](https://docs.openclaw.ai/clawhub?utm_source=openai))  
- The dataset includes multiple “do not install random skills” warnings and treats skills/plugins as a core supply-chain risk surface. (I‑S1, I‑T1)

#### Moltbook (AI-agent-themed social network)

- The dataset describes Moltbook as an “AI-agent social network,” and specifically claims Moltbook works by agents downloading a “skill” that enables posting via API. (I‑T1)  
- The Moltbook landing page describes itself as “the front page of the agent internet” and “a social network for AI agents,” with a **copyable onboarding prompt**:  
  - `Read https://moltbook.com/skill.md and follow the instructions to join Moltbook.` ([moltsbooks.com](https://moltsbooks.com/?utm_source=openai))  
- A third-party explainer (DigitalOcean) states Moltbook was launched publicly on **January 28, 2026**, is “like Reddit,” and was built by **Matt Schlicht** (distinct from Steinberger). ([digitalocean.com](https://www.digitalocean.com/resources/articles/what-is-moltbook?utm_source=openai))  
- Security reporting states Moltbook had a serious exposure due to Supabase misconfiguration / missing RLS, exposing API tokens, emails, and private messages; and also found that humans were operating fleets of bots, undermining “fully autonomous agents” narratives. ([techradar.com](https://www.techradar.com/pro/security/ai-agent-social-media-network-moltbook-is-a-security-disaster-millions-of-credentials-and-other-details-left-unsecured))  

---

### 2.3 People, organizations, and “partnership” claims

#### Peter Steinberger

- The dataset treats Steinberger as “OpenClaw’s creator” (I‑P1).  
- TechCrunch states Steinberger created the assistant now known as OpenClaw and joined OpenAI; it identifies him as Austrian. ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/))  
- Business Insider reports Steinberger founded PSPDFKit and returned from “retirement” to launch OpenClaw in late 2025. ([businessinsider.com](https://www.businessinsider.com/sam-altman-hires-openclaw-creator-peter-steinberger-personal-ai-agents-2026-2?utm_source=openai))  

#### OpenAI relationship (“partnership” vs. “hire” vs. “foundation support”)

- The dataset has a thread titled “OpenAI OpenClaw Partnership” and describes it as OpenAI’s “latest announcement of partnership” (I‑P1).  
- External sources clarify the core facts:  
  - OpenAI CEO Sam Altman posted that Steinberger is joining OpenAI to “drive the next generation of personal agents,” and OpenClaw will “live in a foundation as an open source project” that OpenAI will continue to support. ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/))  
- Therefore, “partnership” in the dataset is best reconciled as: **a hiring + ongoing OSS support / foundation structure**, not necessarily an acquisition of the codebase as a proprietary product.

---

### 2.4 OpenClaw architecture and on-disk configuration/state

#### Core runtime: “Gateway” + config + state

- The dataset consistently frames OpenClaw as an **agent/gateway** that runs locally or on a host, and connects to model providers and chat channels. (I‑S1, I‑P1, I‑T1)  
- Official docs:  
  - Config is JSON5 and lives at `~/.openclaw/openclaw.json` by default. ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/configuration?utm_source=openai))  
  - State defaults under `~/.openclaw` (or `$OPENCLAW_STATE_DIR`), including per-agent sessions and credential stores. ([docs.openclaw.ai](https://docs.openclaw.ai/start/faq/?utm_source=openai))  

#### Install requirements (Node, WSL2)

- Dataset claims: OpenClaw prerequisite **Node.js 22+**; installer handles Node detection/installation. (I‑S1)  
- Official docs confirm: **Node 22+** is required; on Windows, WSL2 is strongly recommended; installation includes `install.sh` and `install.ps1` scripts. ([docs.openclaw.ai](https://docs.openclaw.ai/install/index))  
- Dataset also contains an older/incorrect instruction implying **Node.js 20+** for OpenClaw (in the “fuss-free Windows setup” assistant message inside I‑P1). This conflicts with official docs and is reconciled in §6.1.

#### Channels: Telegram + pairing + DM policy

- Dataset setup sequences repeatedly use: Telegram bot created via **@BotFather** `/newbot`, then placing a bot token into config. (I‑S1, I‑P1, I‑T1)  
- Official docs define DM policy options across channels: `pairing` (default), `allowlist`, `open`, `disabled`. `open` requires `allowFrom: ["*"]`. ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/configuration-reference?utm_source=openai))  
- Official docs define pairing details:  
  - Pairing codes are **8 characters**, uppercase, avoiding ambiguous chars;  
  - Codes **expire after 1 hour**;  
  - Pending DM pairing requests are capped at **3 per channel by default**. ([docs.openclaw.ai](https://docs.openclaw.ai/pairing?utm_source=openai))  
- Dataset aligns on: pairing code expiration “~1 hour,” and CLI approval flow `openclaw pairing list telegram` + `openclaw pairing approve telegram <CODE>`. (I‑S1, I‑S1b)

#### Session isolation: `session.dmScope`

- Dataset recommends `session.dmScope: "per-channel-peer"` to prevent cross-user context leakage. (I‑S1, I‑S1b, I‑S1c)  
- Official docs strongly support this recommendation and explain the default risk: default DM scope (`main`) can cause one sender to see another’s prior context. They recommend secure DM mode using `per-channel-peer`. ([docs.openclaw.ai](https://docs.openclaw.ai/session?utm_source=openai))  

---

### 2.5 Models and providers referenced in the dataset (vLLM, Ollama, GPT‑OSS, Gemini / Vertex)

#### vLLM provider and OpenAI-compatible `/v1` API

- Dataset: OpenClaw can connect to a model server (e.g., vLLM) through an **OpenAI-compatible HTTP API** (notably `/v1/models` and `/v1/chat/completions`). (I‑S1, I‑S1b, I‑S1c)  
- Official OpenClaw docs:  
  - vLLM provider uses `api: "openai-completions"` and expects `/v1/*` endpoints; default base URL often `http://127.0.0.1:8000/v1`. ([docs.openclaw.ai](https://docs.openclaw.ai/providers/vllm?utm_source=openai))  
  - It supports **auto-discovery** from `/v1/models` when `VLLM_API_KEY` is set and no explicit provider entry exists; “any value works if your server doesn’t enforce auth.” ([docs.openclaw.ai](https://docs.openclaw.ai/providers/vllm?utm_source=openai))  

#### vLLM `--api-key` is not a perimeter control

- Dataset repeatedly asserts vLLM’s `--api-key` only protects `/v1/*` endpoints and other endpoints can remain unprotected; therefore vLLM should not be exposed publicly. (I‑S1b, I‑S1c)  
- vLLM’s official security docs confirm: `--api-key` protects only `/v1` endpoints; “many other sensitive endpoints” remain unauthenticated, and you should not rely exclusively on `--api-key`. ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/?utm_source=openai))  

#### GPT‑OSS models referenced (20B / 120B), MXFP4, and deployment

- Dataset uses GPT‑OSS models as example self-hosted backends for OpenClaw via vLLM: `openai/gpt-oss-20b` and `openai/gpt-oss-120b`, including VRAM guidance and AWS instance suggestions. (I‑S1, I‑T1)  
- OpenAI’s official announcement states:  
  - `gpt-oss-120b` and `gpt-oss-20b` are open-weight models under Apache 2.0;  
  - Weights are natively quantized in **MXFP4**;  
  - `gpt-oss-120b` can run within **80GB memory**, and `gpt-oss-20b` can run with **16GB**. ([openai.com](https://openai.com/index/introducing-gpt-oss?utm_source=openai))  
- vLLM’s blog announcement states vLLM supports gpt-oss, provides a container image `vllm/vllm-openai:gptoss`, and shows `uv pip install --pre vllm==0.10.1+gptoss ...` as an installation method (matching dataset commands). ([blog.vllm.ai](https://blog.vllm.ai/2025/08/05/gpt-oss.html?utm_source=openai))  
- AWS confirms `p5.4xlarge` includes **1× H100 80GB** GPU memory. ([aws.amazon.com](https://aws.amazon.com/ec2/instance-types/p5/?utm_source=openai))  

#### Ollama (local models) to avoid cloud API keys

- Dataset repeatedly recommends using a local model runtime such as **Ollama** to avoid using OpenAI/Anthropic/Gemini API keys and to keep traffic local. (I‑P1, I‑T1)  
- Official OpenClaw docs explicitly list Ollama support and indicate model refs like `ollama/llama3.3`. ([docs.openclaw.ai](https://docs.openclaw.ai/concepts/model-providers?utm_source=openai))  

#### Google Gemini API and Vertex

- Dataset states OpenClaw has built-in Gemini support:  
  - Provider `google` (Gemini Developer API via API key `GEMINI_API_KEY`), and  
  - Provider `google-vertex` (Vertex AI via ADC). (I‑S1d, I‑C1)  
- Official OpenClaw docs confirm:  
  - Provider `google`, auth `GEMINI_API_KEY`, example model `google/gemini-3-pro-preview`, CLI path `openclaw onboard --auth-choice gemini-api-key`;  
  - `google-vertex`, `google-antigravity`, and `google-gemini-cli` exist as distinct providers with distinct auth flows; some OAuth flows ship as bundled plugins that must be enabled. ([docs.openclaw.ai](https://docs.openclaw.ai/concepts/model-providers?utm_source=openai))  
- Google’s official Gemini 3 API docs list model IDs including `gemini-3-flash-preview` and state that Gemini 3 models are in preview. ([ai.google.dev](https://ai.google.dev/gemini-api/docs/gemini-3?utm_source=openai))  

---

### 2.6 Deployment patterns in the dataset (Telegram + laptop/WSL2 + AWS model host)

The dataset includes three progressively more security-hardened “reference architectures”:

#### Pattern A: SSH tunnel to a cloud-hosted model server (initial “works-first” approach)

- Dataset architecture:  
  - Telegram ↔ OpenClaw (laptop) ↔ (localhost:8000 via SSH tunnel) ↔ vLLM (AWS EC2) ↔ GPT‑OSS. (I‑S1)  
- Key controls emphasized: bind vLLM to `127.0.0.1`, do not open model port publicly, use SSH tunnel; pairing mode and DM session isolation. (I‑S1, I‑S1b)

#### Pattern B: WSL2-hosted OpenClaw (Windows laptop) + SSH tunneling

- Dataset adds:  
  - OpenClaw on Windows is “intended” to run in WSL2; daemon install uses a systemd **user** unit; systemd-in-WSL enablement is necessary. (I‑S1b)  
- Microsoft documentation confirms systemd-in-WSL steps: requires WSL **0.67.6+**, set `/etc/wsl.conf` with `[boot] systemd=true`, then `wsl.exe --shutdown`. ([learn.microsoft.com](https://learn.microsoft.com/es-es/windows/wsl/systemd))  

#### Pattern C: AWS SSM port-forwarding (preferred hardened approach)

- Dataset’s hardened approach prefers AWS SSM Session Manager port forwarding over SSH: “No inbound 22, no SSH keys, less TOFU risk.” (I‑S1c)  
- AWS documentation confirms `aws ssm start-session --document-name AWS-StartPortForwardingSession ...` usage. ([aws.amazon.com](https://aws.amazon.com/blogs/aws/new-port-forwarding-using-aws-system-manager-sessions-manager/?utm_source=openai))  

---

### 2.7 Security posture: controls, footguns, and incident patterns

#### Skills / plugin supply chain risk

- Dataset repeatedly warns that skills/plugins can be malicious and should be treated as untrusted unless audited. (I‑S1, I‑P1, I‑T1)  
- OpenClaw documentation states plugins are loaded **in-process** and explicitly says: “treat plugin installs like running code” and prefer pinned versions. ([docs.openclaw.ai](https://docs.openclaw.ai/cli/plugins?utm_source=openai))  
- Reporting documents “hundreds” of malicious skills on ClawHub, often delivered via social engineering and commands that pull infostealers. ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai))  

#### Secrets management risk (plaintext configs, env files, /mnt/c)

- Dataset critique highlights plaintext storage risk in `~/.openclaw/openclaw.json`, and recommends chmod restrictions (600/700), plus avoiding `/mnt/c` on WSL2 because Windows-side malware can read it. (I‑S1c)  
- OpenClaw’s official security docs confirm `openclaw security audit --fix` tightens permissions on `~/.openclaw` and config/state files. ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/security?utm_source=openai))  

#### WSL2 trust boundary caveat

- Dataset claims WSL2 is not a strong security boundary vs the Windows host and warns that forwarded ports may be reachable from Windows. (I‑S1c)  
- While the dataset’s exact “host reachability” claims are nuanced, the general operational point is consistent with typical WSL networking behavior and the need to treat Windows+WSL as the same trust zone in many threat models (see §6.6 for residual uncertainty and scope).

#### “Security audit” as a built-in practice

- Dataset mentions schema validation and “bad keys can prevent startup,” but not a formal audit command. (I‑S1)  
- Official docs provide a first-class `openclaw security audit` with modes `--deep` and `--fix`, covering gateway exposure, elevated tools, permissions, etc. ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/security?utm_source=openai))  

#### Notable February 2026 incident pattern: malware and data exposure

- Moltbook: exposed Supabase API key / missing RLS led to exposure of API tokens/emails/DMs, and Wiz found humans operating bot fleets. ([techradar.com](https://www.techradar.com/pro/security/ai-agent-social-media-network-moltbook-is-a-security-disaster-millions-of-credentials-and-other-details-left-unsecured))  
- OpenClaw configs: infostealer extracted configuration data (API keys/auth tokens) from an OpenClaw setup. ([techradar.com](https://www.techradar.com/pro/security/openclaw-ai-agents-targeted-by-infostealer-malware-for-the-first-time?utm_source=openai))  

---

## 3. Timeline / Evolution

> Dates below are reconciled from (a) dataset narrative fragments and (b) external reporting and primary-source quotes.

### 3.1 High-level timeline (reconciled)

| Date (UTC) | Event | Evidence |
|---|---|---|
| **Dec 2025** | Clawdbot “debuted in December” (viral agent). | ([businessinsider.com](https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1)) |
| **2026‑01‑27** | Rebrand: **Clawdbot → Moltbot** after Anthropic trademark request; Steinberger says “forced”; mascot renamed “Molty.” | ([businessinsider.com](https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1)) |
| **Late Jan 2026 (days after 01‑27)** | Second rebrand to **OpenClaw** (TechCrunch: changed again because Steinberger liked the new name better). | ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/)) |
| **2026‑01‑28** | **Moltbook** launched publicly (per DigitalOcean explainer). | ([digitalocean.com](https://www.digitalocean.com/resources/articles/what-is-moltbook?utm_source=openai)) |
| **2026‑02‑03** | TechRadar publishes Moltbook exposure report (Wiz findings). | ([techradar.com](https://www.techradar.com/pro/security/ai-agent-social-media-network-moltbook-is-a-security-disaster-millions-of-credentials-and-other-details-left-unsecured)) |
| **2026‑02‑15** | Steinberger joining OpenAI publicly reported; Altman posts about “next generation of personal agents”; OpenClaw to live in a foundation supported by OpenAI. | ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/)) |
| **2026‑02 (ongoing)** | Multiple reports of ClawHub malicious skills and OpenClaw security concerns; multiple companies banning OpenClaw reported. | ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai)) |
| **2026‑02 (ongoing)** | Infostealer exfiltration targeting OpenClaw configs reported. | ([techradar.com](https://www.techradar.com/pro/security/openclaw-ai-agents-targeted-by-infostealer-malware-for-the-first-time?utm_source=openai)) |

### 3.2 Dataset-internal timeline anchors (as a “secondary chronicle”)

- The dataset’s most operationally detailed OpenClaw deployment discussion occurred **Feb 17–20, 2026** in the “OpenClaw Setup Guide” thread (I‑S1).  
- The dataset’s OpenAI “partnership” prompt is dated **Feb 16, 2026** (I‑P1), aligning with external reporting timing.  
- The dataset’s “Clawdbot Investigation Request” is dated **Jan 26–27, 2026** (I‑C1), consistent with the rebrand window.

---

## 4. Capabilities / Components / Relationships

### 4.1 OpenClaw Gateway as the integration hub

- In the dataset, OpenClaw is repeatedly described as the **agent runtime / gateway** that:  
  - receives inbound chat messages via a channel (Telegram, etc.),  
  - forwards prompts to a configured model provider,  
  - returns responses to the channel. (I‑S1, I‑P1, I‑T1)  
- In official documentation, this maps to: Gateway config (`~/.openclaw/openclaw.json`), state dir (`~/.openclaw`), and CLI workflows (`openclaw onboard`, `openclaw dashboard`, `openclaw doctor`). ([docs.openclaw.ai](https://docs.openclaw.ai/install/index))  

### 4.2 Channels, access control, and “pairing” workflow

- **Telegram** is central in the dataset:  
  - Create bot token via BotFather. (I‑S1, I‑P1)  
  - Configure `channels.telegram.botToken`. (I‑S1)  
  - Use `dmPolicy: "pairing"` to block strangers. (I‑S1, I‑S1c)  
- Official docs generalize the same policy model across channels (`pairing`, `allowlist`, `open`, `disabled`). ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/configuration-reference?utm_source=openai))  
- Pairing codes: 8 chars; expire after 1 hour; pending requests capped at 3/channel by default. ([docs.openclaw.ai](https://docs.openclaw.ai/pairing?utm_source=openai))  

### 4.3 Sessions and DM isolation (`session.dmScope`)

- Dataset: “DM session isolation (per-channel-peer) prevents context leakage between Telegram users.” (I‑S1 critique + response)  
- Official docs: secure DM mode is `per-channel-peer`; default is `main` for continuity; additional modes exist (`per-peer`, `per-account-channel-peer`). ([docs.openclaw.ai](https://docs.openclaw.ai/session?utm_source=openai))  

### 4.4 Tools, skills, plugins, sandboxing, automation (“agency surface area”)

- The dataset’s safety framing explicitly differentiates: chat-only vs tool-using “agent.” (I‑T1, I‑C2)  
- Official docs define:  
  - **Tools** with allow/deny policy and tool profiles such as `minimal`, `coding`, `messaging`, `full`. ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/configuration-reference?utm_source=openai))  
  - **Elevated tools** as an explicit “escape hatch” gated by allowlists. ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/configuration-reference?utm_source=openai))  
  - **Skills** as AgentSkills-compatible folders, with load precedence: bundled, `~/.openclaw/skills`, and `<workspace>/skills` (workspace wins). ([docs.openclaw.ai](https://docs.openclaw.ai/skills?utm_source=openai))  
  - **ClawHub** as a public skills registry. ([docs.openclaw.ai](https://docs.openclaw.ai/clawhub?utm_source=openai))  
  - **Sandboxing** (Docker-based controls) and its interaction with tool policy and elevated tools. ([docs.openclaw.ai](https://docs.openclaw.ai/sandboxing?utm_source=openai))  
  - **Heartbeat**: default every 30m, reads `HEARTBEAT.md` if present; can be disabled with `0m`. ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/heartbeat?utm_source=openai))  

### 4.5 Model-provider relationships in practice

- Dataset suggests a pattern:  
  - prefer local model servers or tunneled private endpoints,  
  - avoid exposing raw model ports,  
  - treat API keys as insufficient perimeter controls for some servers (vLLM). (I‑S1b, I‑S1c)  
- vLLM provider docs explicitly match dataset configuration idioms (`baseUrl`, `/v1`, `openai-completions`, `VLLM_API_KEY` opt-in). ([docs.openclaw.ai](https://docs.openclaw.ai/providers/vllm?utm_source=openai))  
- Gemini provider docs in OpenClaw match dataset guidance: provider `google`, `GEMINI_API_KEY`, models like `google/gemini-3-*-preview`. ([docs.openclaw.ai](https://docs.openclaw.ai/concepts/model-providers?utm_source=openai))  

### 4.6 Cloud connectivity patterns (SSH vs SSM port-forwarding)

- Dataset’s initial approach uses SSH `-L` local port forwarding; later hardening prefers SSM for fewer exposed surfaces. (I‑S1, I‑S1c)  
- AWS supports port forwarding via SSM using `AWS-StartPortForwardingSession`. ([aws.amazon.com](https://aws.amazon.com/blogs/aws/new-port-forwarding-using-aws-system-manager-sessions-manager/?utm_source=openai))  

---

## 5. Ambiguities and Contradictions Identified

### 5.1 Node.js requirement: “Node 20+” vs “Node 22+”

- **Conflict**: Dataset contains a “fuss-free” guide claiming OpenClaw prerequisites include “Node.js 20+” (I‑P1), while other dataset parts claim “Node.js 22+” (I‑S1).  
- **Resolution**: Official OpenClaw docs specify **Node 22+** as the system requirement. ([docs.openclaw.ai](https://docs.openclaw.ai/install/index))  
- **Status**: Resolved in favor of official docs.

### 5.2 Naming sequence timing and labels (Clawdbot → Moltbot → OpenClaw)

- **Conflict**: Dataset narrative implies “Clawdbot → Moltbot → OpenClaw,” but various secondary sources online sometimes collapse or mis-order intermediate names.  
- **Resolution**: Business Insider fixes the first pivot at **2026‑01‑27** (Clawdbot → Moltbot). TechCrunch confirms that OpenClaw was “previously known as Clawdbot, then Moltbot,” and that it changed again shortly after. ([businessinsider.com](https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1))  
- **Status**: Resolved as: **Clawdbot → Moltbot (Jan 27, 2026) → OpenClaw (late Jan 2026)**.

### 5.3 “Partnership” vs “acquisition” vs “hire + foundation support”

- **Conflict**: Dataset labels the event as “OpenAI’s partnership with OpenClaw” (I‑P1). Some external blogs even use “acquires.”  
- **Resolution**: Primary quotes in TechCrunch and The Verge indicate a **hire** and an OSS **foundation** arrangement, not a classic acquisition announcement. ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/))  
- **Status**: Reconciled as “acqui-hire + foundation support,” with “partnership” treated as informal wording.

### 5.4 “Are these really autonomous AI agents on Moltbook with no human input?”

- **Conflict**: Dataset asks whether Moltbook is “really all AI agents talking autonomously with no human guidance,” and earlier assistant guidance warns against over-interpreting this as “independent lifeforms.” (I‑T1)  
- **Resolution**: Security reporting states Wiz found humans operating fleets of bots, undermining autonomy narratives. ([techradar.com](https://www.techradar.com/pro/security/ai-agent-social-media-network-moltbook-is-a-security-disaster-millions-of-credentials-and-other-details-left-unsecured))  
- **Status**: Reconciled as: operational automation exists, but “no human guidance/input” is not supported.

### 5.5 ClawHub malicious skills counts (“over 400”, “hundreds”, “28+386”, “341”, “14”)

- **Conflict**: Different sources cite different counts and windows for malicious skills on ClawHub/ClawHub-related registries; dataset contains general “malicious skills exist” warnings but no consistent count.  
- **Partial reconciliation**:
  - The Verge reports researchers found “hundreds,” and provides a breakdown: 28 malicious skills (Jan 27–29) + 386 malicious add-ons (Jan 31–Feb 2). ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai))  
  - The Verge also separately uses “over 400” language in a Feb 15 update piece. ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai))  
  - Tom’s Hardware mentions “at least 14” between Jan 27 and Jan 29 (potentially a narrower subset or earlier disclosure). ([tomshardware.com](https://www.tomshardware.com/tech-industry/cyber-security/malicious-moltbot-skill-targets-crypto-users-on-clawhub?utm_source=openai))  
- **Status**: Reconciled as “multiple incident windows + multiple counting methods”; exact canonical number remains somewhat unsettled (see §8).

### 5.6 Unverified/unclear config keys in dataset (example: `configWrites: false`)

- **Conflict**: Dataset proposes `configWrites: false` in channel config to prevent Telegram-triggered config writes (I‑T1).  
- **Resolution attempt**: No matching key was found in official OpenClaw configuration reference during this run; official docs instead describe `/config` commands gated by `commands.config: true` and other mechanisms. ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/configuration-reference?utm_source=openai))  
- **Status**: Unresolved; treated as **dataset-only / possibly outdated / possibly incorrect**.

### 5.7 Gemini key rotation variables claimed (`GEMINI_API_KEYS`, `GEMINI_API_KEY_1`, etc.)

- **Conflict**: Dataset claims OpenClaw supports rotation patterns like `GEMINI_API_KEYS` / `GEMINI_API_KEY_1`. (I‑S1e)  
- **Resolution attempt**: Official docs confirm only `GEMINI_API_KEY` as the provider auth env var, and do not document the claimed rotation env var patterns. ([docs.openclaw.ai](https://docs.openclaw.ai/concepts/model-providers?utm_source=openai))  
- **Status**: Unresolved; treat as **unverified**.

---

## 6. Reconciliation Log (internal + web steps)

### Method summary

1. **Internal reconciliation**: Compared statements across dataset threads for the same concept (requirements, naming, security guidance).  
2. **External reconciliation**: Consulted authoritative sources in order of priority:
   - Official OpenClaw documentation (`docs.openclaw.ai`) and official GitHub repo (`openclaw/openclaw`)
   - Primary/major reporting (TechCrunch, The Verge, Business Insider, Wired, TechRadar)
   - Vendor docs (vLLM security docs, AWS SSM docs, Microsoft WSL docs, OpenAI GPT‑OSS announcement, Google Gemini API docs)

### 6.1 Node.js requirement

- **What conflicted**: “Node 20+” vs “Node 22+.” (I‑P1 vs I‑S1)  
- **Internal evidence checked**:  
  - I‑P1 includes “Node.js 20+” in a Windows setup.  
  - I‑S1 includes “Node.js 22+” and says installer can handle it.  
- **External sources consulted**: Official OpenClaw install docs state Node 22+. ([docs.openclaw.ai](https://docs.openclaw.ai/install/index))  
- **Judgment**: Node 22+ is correct; Node 20+ in dataset is treated as incorrect/outdated.

### 6.2 Rebrand sequence and dates

- **What conflicted**: Inconsistent naming in dataset and potential confusion about which name was final.  
- **Internal evidence checked**: Dataset contains “Clawdbot → Moltbot → OpenClaw” storyline (I‑T1, I‑S1, I‑P1).  
- **External sources consulted**:
  - Business Insider timestamped rename to Moltbot (2026‑01‑27). ([businessinsider.com](https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1))  
  - TechCrunch clarifies prior names and later rename. ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/))  
- **Judgment**: Rebrand is reconciled as Clawdbot → Moltbot (Jan 27) → OpenClaw (late Jan).

### 6.3 OpenAI “partnership” nature

- **What conflicted**: Dataset framed as “partnership”; some sources call it “acquisition.”  
- **Internal evidence checked**: I‑P1.  
- **External sources consulted**: TechCrunch/The Verge quote Altman that Steinberger is joining OpenAI; OpenClaw in foundation supported by OpenAI. ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/))  
- **Judgment**: This is best described as a hire + foundation support (not a product acquisition announcement).

### 6.4 vLLM `--api-key` sufficiency

- **What conflicted**: Dataset asserts `--api-key` is insufficient; needed verification.  
- **Internal evidence checked**: I‑S1b, I‑S1c.  
- **External sources consulted**: vLLM security docs explicitly warn `--api-key` only protects `/v1`, leaving many endpoints unprotected. ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/?utm_source=openai))  
- **Judgment**: Dataset claim confirmed.

### 6.5 Moltbook autonomy vs human control

- **What conflicted**: Dataset asked if Moltbook is “really autonomous agents with no human input.”  
- **Internal evidence checked**: I‑T1 emphasizes “operational autonomy real; motivational autonomy not demonstrated.”  
- **External sources consulted**: TechRadar reports Wiz found humans operating fleets of bots. ([techradar.com](https://www.techradar.com/pro/security/ai-agent-social-media-network-moltbook-is-a-security-disaster-millions-of-credentials-and-other-details-left-unsecured))  
- **Judgment**: Dataset skepticism is supported; “no human guidance/input” is not supported.

### 6.6 ClawHub malicious skills counts

- **What conflicted**: Different figures across sources (14 vs hundreds vs over 400; different time windows).  
- **Internal evidence checked**: Dataset offers general warnings (I‑S1, I‑T1) without precise counts.  
- **External sources consulted**:
  - The Verge: “hundreds,” plus explicit 28 + 386 breakdown. ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai))  
  - Tom’s Hardware: at least 14 in Jan 27–29 window. ([tomshardware.com](https://www.tomshardware.com/tech-industry/cyber-security/malicious-moltbot-skill-targets-crypto-users-on-clawhub?utm_source=openai))  
  - The Verge (Feb 15 update): “over 400.” ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai))  
- **Judgment**: Treat as multiple overlapping disclosure windows and counting frames; report both the “breakdown” and the “over 400” phrasing and mark the canonical number as uncertain.

---

## 7. Final Reconciled View

### 7.1 What OpenClaw is (today, Feb 22, 2026)

- OpenClaw is an open-source, MIT-licensed personal-agent system (Gateway + tools/skills/plugins + channels) that runs on user-controlled hardware and can connect to multiple model providers (cloud or self-hosted). ([github.com](https://github.com/openclaw/openclaw))  
- It is the “final name” in a late-Jan 2026 rebrand sequence that began with Clawdbot, briefly became Moltbot, and then stabilized as OpenClaw. ([businessinsider.com](https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1))  

### 7.2 What “Clawdbot” and “Moltbot” mean in practice

- They primarily matter for:
  - **outdated tutorials** using older CLI names/config paths, and  
  - **security/scam risk** (handle sniping, typosquats, malicious forks) during rapid renames (explicitly noted in multiple narratives in the dataset and reporting). (I‑T1; also see ecosystem reporting) ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai))  

### 7.3 How Moltbook fits

- Moltbook is a separate “agent social network” product that can be joined via an agent prompt to read a `skill.md`, and is closely associated with OpenClaw culturally and operationally. ([moltsbooks.com](https://moltsbooks.com/?utm_source=openai))  
- Claims that Moltbook is purely autonomous agents without human control are not supported; reporting indicates human bot fleets were involved. ([techradar.com](https://www.techradar.com/pro/security/ai-agent-social-media-network-moltbook-is-a-security-disaster-millions-of-credentials-and-other-details-left-unsecured))  

### 7.4 The reconciled “secure baseline” pattern (from dataset + confirmed docs)

A consistent best-practice baseline emerges across dataset threads and official docs:

- **Access control**: use `dmPolicy: "pairing"` (or allowlist) and enable **secure DM mode** (`session.dmScope: "per-channel-peer"`) when multiple senders may DM. ([docs.openclaw.ai](https://docs.openclaw.ai/pairing?utm_source=openai))  
- **Minimize capability**: start with tool profile `minimal` or tightly scoped profiles; treat elevated tools as high risk. ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/configuration-reference?utm_source=openai))  
- **Treat skills/plugins as code**: prefer audited/pinned installs; be cautious with ClawHub skills given active malware reports. ([docs.openclaw.ai](https://docs.openclaw.ai/clawhub?utm_source=openai))  
- **Secrets hygiene**: keep secrets out of broadly readable locations; enforce strict permissions; regularly run `openclaw security audit` (and `--fix` after config changes). ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/security?utm_source=openai))  
- **If self-hosting vLLM**: do not rely on `--api-key` as perimeter; keep ports private/tunneled. ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/))  
- **If on Windows**: prefer WSL2 with systemd for daemon/service management, as reflected in both dataset and Microsoft’s documented systemd enablement process. ([learn.microsoft.com](https://learn.microsoft.com/es-es/windows/wsl/systemd))  

---

## 8. Open Questions / Residual Uncertainty

1. **Foundation governance details**: External reporting states OpenClaw will live in a foundation supported by OpenAI, but the dataset does not include governance documents, bylaws, board structure, or funding details; those remain unknown from the JSON alone. ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/))  
2. **Canonical count of malicious skills**: reporting provides multiple overlapping counts and windows (e.g., “hundreds,” “over 400,” “28 + 386,” “at least 14”). Without a single authoritative incident report, the exact number depends on definitions and time window. ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai))  
3. **Dataset-only config keys** (`configWrites: false`) and Gemini key-rotation env vars (`GEMINI_API_KEYS`, etc.) were not found in official docs in this run and may be outdated/incorrect or refer to forks/older builds. ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/configuration-reference?utm_source=openai))  
4. **WSL2 port exposure nuances**: The dataset warns that WSL2 localhost services can be reachable from Windows (and possibly LAN depending on settings). This is plausible but configuration-dependent; the report treats it as a caution rather than a universal fact because official OpenClaw docs do not centrally define WSL networking semantics. (I‑S1c)  
5. **Moltbook “agent count” validity**: Moltbook pages show very large agent counts, but external reporting suggests many are human-controlled or spam-like; therefore “agent counts” should not be interpreted as “independent AI entities.” ([moltsbooks.com](https://moltsbooks.com/?utm_source=openai))  

---

## 9. Source Appendix (input evidence mapping + web citations)

### 9.1 Internal evidence index (from the provided JSON)

> Format: **Internal ID** → (conversation_id, message_id(s), timestamps) → description

- **I‑S1** → (`6993f8ed-1570-8398-84e7-0f5f279b8b6c`, msg `1d32eb7f-de43-4092-ae80-9a898bb65837`, 2026‑02‑17) → “Works-first, secure-by-default” OpenClaw ↔ Telegram ↔ AWS vLLM spec (SSH tunnel, Node requirement claim, config examples, pairing flow).  
- **I‑S1b** → same conversation, msg `e6e0f346-4787-40de-8bd8-0dbf004f281f`, 2026‑02‑17 → WSL2-first setup; systemd; autossh; vLLM localhost binding; warnings about `--api-key` limitations; model ID discovery.  
- **I‑S1c** → same conversation, msg `a0e6f42d-c420-43fa-aaf8-f21835d83d2a`, 2026‑02‑17 → Hardened security critique response: SSM port forwarding, encrypted EBS, ufw, unattended-upgrades, env-file secrets, systemd services, WSL2 hardening, cost controls.  
- **I‑S1d** → same conversation, msg `3be8f2d4-2922-4102-9a3b-2afcadc566b5`, 2026‑02‑19 → Gemini feasibility analysis (Developer API vs Vertex, data retention concerns, key handling pattern).  
- **I‑S1e** → same conversation, msg `2429e755-1bce-4161-b1f9-15b350c4cad5`, 2026‑02‑19 → “Lowest friction” Gemini integration steps, `google/gemini-3-flash-preview` model string, pairing + secrets file approach; unverified key-rotation env-var claim.  
- **I‑S1f** → same conversation, msg `8da02c89-52bc-4a00-92b9-fb4d1845bb42`, 2026‑02‑20 → Model selection framework for agent reliability vs cost (tool-use, instruction adherence, etc.).  

- **I‑P1** → (`69929f24-af0c-839a-aeca-a59c28fb8101`, msg `daebc507-c1f1-4ec4-bc22-8da731d31670`, 2026‑02‑16) → “Investigate partnership” narrative; predicted spinoffs; early “fuss-free” Windows setup; open-source model path via Ollama.  
- **I‑P1b** → same conversation, msg `94fc65e0-c514-4400-9720-dbb8aaf238ec`, 2026‑02‑16 → Detailed Windows + Telegram + Ollama instructions; WSL2 recommended; `/model` commands noted.

- **I‑T1** → (`697e188d-cb80-839b-afa2-966d435ad71f`, msg `d86f44a2-d621-437d-b4f8-5df25876ea25`, 2026‑02‑01) → AI-safety framing around Moltbook/OpenClaw; operational vs motivational autonomy; heartbeats; skills supply chain.  
- **I‑T1b** → same conversation, msg `850af348-3cd5-4980-954d-578d9fbc0131`, 2026‑02‑01 → “Safest practical” setup: Telegram pairing, heartbeat disabled, no tools, local model via Ollama; includes `configWrites: false` key (unverified).  
- **I‑T1c** → same conversation, msgs `67ee7470-6b48-4d46-a7ac-476ce7188a63` + `64f12f14-7373-4ae1-b282-9f3ea1c1460d`, 2026‑02‑01 → gpt‑oss‑20b cloud feasibility discussion + long-context tuning flags.

- **I‑C1** → (`697744f2-ab48-8322-a3fc-3faa3ad0b4db`, msg `c3b23c94-a93d-4460-9c39-87ffc964a75c`, 2026‑01‑26) → Clawdbot capability report (channels, tools/skills/plugins, Gmail via gogcli, security audit, risks).  
- **I‑C1b** → same conversation, msg `bc7d92ea-0f8c-4ddd-b6a6-c2d007b99e27`, 2026‑01‑26 → WhatsApp monitor/alert workflow; multi-account notion; `NO_REPLY` mention.  
- **I‑C1c** → same conversation, msg `b4ada4f0-ebcc-4def-8651-719ac1870381`, 2026‑01‑27 → “Clawdbot renamed to Moltbot” claim (later reconciled with BI and TechCrunch).

- **I‑M1** → (`69929dd1-23ec-8398-922a-f18c0658e14b`, msg `17cc28e9-5f34-4be0-b4be-373048ba433b`, 2026‑02‑16) → Minor: “Change the words ‘Something else’ to OpenClaw Integration” in an image-edit request.

### 9.2 External sources consulted (URLs + publisher + date)

> URLs are shown in code formatting to satisfy the “no raw URLs in prose” constraint. Citations for each source appear throughout the report.

| Publisher | Date (as shown on page/snippet) | URL |
|---|---:|---|
| OpenClaw Docs | (crawled Feb 2026) | `https://docs.openclaw.ai/install/index` ([docs.openclaw.ai](https://docs.openclaw.ai/install/index)) |
| OpenClaw Docs | (crawled Feb 2026) | `https://docs.openclaw.ai/gateway/configuration-reference` ([docs.openclaw.ai](https://docs.openclaw.ai/gateway/configuration-reference?utm_source=openai)) |
| OpenClaw Docs | (crawled Feb 2026) | `https://docs.openclaw.ai/pairing` (redirects to channels/pairing) ([docs.openclaw.ai](https://docs.openclaw.ai/pairing)) |
| OpenClaw Docs | (crawled Feb 2026) | `https://docs.openclaw.ai/session` ([docs.openclaw.ai](https://docs.openclaw.ai/session?utm_source=openai)) |
| OpenClaw Docs | (crawled Feb 2026) | `https://docs.openclaw.ai/providers/vllm` ([docs.openclaw.ai](https://docs.openclaw.ai/providers/vllm?utm_source=openai)) |
| OpenClaw Docs | (crawled Feb 2026) | `https://docs.openclaw.ai/clawhub` ([docs.openclaw.ai](https://docs.openclaw.ai/clawhub?utm_source=openai)) |
| OpenClaw GitHub | (crawled Feb 2026) | `https://github.com/openclaw/openclaw` ([github.com](https://github.com/openclaw/openclaw)) |
| TechCrunch | 2026‑02‑15 | `https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/` ([techcrunch.com](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/)) |
| The Verge | Updated 2026‑02‑15 | `https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai` ([theverge.com](https://www.theverge.com/ai-artificial-intelligence/879623/openclaw-founder-peter-steinberger-joins-openai)) |
| Business Insider | 2026‑01‑27T16:28:39Z | `https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1` ([businessinsider.com](https://www.businessinsider.com/clawdbot-changes-name-moltbot-anthropic-trademark-2026-1)) |
| OpenAI | 2025‑08‑05 | `https://openai.com/index/introducing-gpt-oss` ([openai.com](https://openai.com/index/introducing-gpt-oss?utm_source=openai)) |
| vLLM Blog | 2025‑08‑05 | `https://blog.vllm.ai/2025/08/05/gpt-oss.html` ([blog.vllm.ai](https://blog.vllm.ai/2025/08/05/gpt-oss.html?utm_source=openai)) |
| vLLM Docs | v0.13.0 (published ~Dec 2025) | `https://docs.vllm.ai/en/v0.13.0/usage/security/` ([docs.vllm.ai](https://docs.vllm.ai/en/v0.13.0/usage/security/)) |
| AWS | (current docs) | `https://aws.amazon.com/ec2/instance-types/p5/` ([aws.amazon.com](https://aws.amazon.com/ec2/instance-types/p5/?utm_source=openai)) |
| AWS Blog | (port forwarding) | `https://aws.amazon.com/blogs/aws/new-port-forwarding-using-aws-system-manager-sessions-manager/` ([aws.amazon.com](https://aws.amazon.com/blogs/aws/new-port-forwarding-using-aws-system-manager-sessions-manager/)) |
| Microsoft Learn | (systemd in WSL) | `https://learn.microsoft.com/windows/wsl/systemd` ([learn.microsoft.com](https://learn.microsoft.com/es-es/windows/wsl/systemd)) |
| Google AI for Developers | (Gemini 3 docs) | `https://ai.google.dev/gemini-api/docs/gemini-3` ([ai.google.dev](https://ai.google.dev/gemini-api/docs/gemini-3?utm_source=openai)) |
| TechRadar | published 2026‑02‑03 | `https://www.techradar.com/pro/security/ai-agent-social-media-network-moltbook-is-a-security-disaster-millions-of-credentials-and-other-details-left-unsecured` ([techradar.com](https://www.techradar.com/pro/security/ai-agent-social-media-network-moltbook-is-a-security-disaster-millions-of-credentials-and-other-details-left-unsecured)) |
| Business Insider | (Moltbook breach) | `https://www.businessinsider.com/moltbook-ai-agent-hack-wiz-security-email-database-2026-2` ([businessinsider.com](https://www.businessinsider.com/moltbook-ai-agent-hack-wiz-security-email-database-2026-2?utm_source=openai)) |
| The Verge | (ClawHub malware) | `https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare` ([theverge.com](https://www.theverge.com/news/874011/openclaw-ai-skill-clawhub-extensions-security-nightmare?utm_source=openai)) |
| Moltbook site | (snapshot) | `https://moltsbooks.com/` and/or `https://moltbook.com/skill.md` entrypoint referenced from site ([moltsbooks.com](https://moltsbooks.com/?utm_source=openai)) |
| DigitalOcean | (Moltbook explainer) | `https://www.digitalocean.com/resources/articles/what-is-moltbook` ([digitalocean.com](https://www.digitalocean.com/resources/articles/what-is-moltbook?utm_source=openai)) |

---
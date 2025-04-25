### Project Snapshot

| File                                   | Purpose                                                                                                                                  |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **`image_generation_instructions.md`** | ✅ Master reference for API usage: detailed, curated instructions & examples. This sets the standard for features to eventually support. |
| **`app.py`**                           | ✅ Flask backend: Implements image generation and editing endpoints. Uses OpenAI API with local image saving and basic error handling.   |
| **`index.html`**                       | ✅ Frontend: Clean HTML + vanilla JS interface to test `/generate` and `/edit` endpoints, with client-side preview and download options. |

---

### High-level summary of the **OpenAI Image API (`gpt-image-1`)**

| Area                   | Key points you need to remember                                                                                                                   |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ---- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Endpoints**          | **`images.generate`** – create from text. <br>**`images.edit`** – create or revise using 1-10 reference images, optional mask (first image only). |
| **Core inputs**        | `model="gpt-image-1"` (required) • `prompt` (natural-language description).                                                                       |
| **Generation options** | `n` (how many images in one call) • `size` (`1024×1024`, `1536×1024`, `1024×1536`, `auto`) • `quality` (`low                                      | medium | high | auto`) • `background` (`transparent`or omitted) •`output_format` (`png`default,`jpeg`, `webp`) • `output_compression` (0-100 for jpeg/webp). |
| **Editing specifics**  | Up to 10 _input_ images. <br>Mask must match first image’s size/format and **contain an α-channel**. Black = keep, transparent = replace.         |
| **Returns**            | JSON → `data[ ].b64_json` (base-64 image). Decode and write to disk or stream to browser.                                                         |
| **Moderation**         | `moderation="auto"` (default) or `"low"` for looser filtering.                                                                                    |
| **Typical latencies**  | Square / standard-quality images are fastest; larger or transparent/high-quality ones take longer.                                                |
| **Billing / limits**   | Same token-billing model as other OpenAI endpoints; each image counts as one completion. (No quota numbers were supplied in the docs you gave.)   |

---

### From API to **full-stack web app**: architecture & design plan

Below is a pragmatic design that exposes **all** the API’s capabilities while staying maintainable and scalable.

| Layer                                        | Recommended tech & why                                 | Responsibilities                                                                                                                                                                                                                                                                                                                                                                                                                              |
| -------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Front-end SPA**                            | ★ **React + TypeScript** (Next.js, Vite or CRA)        | – UI for entering prompt, picking size/quality/background, uploading images/masks. <br>– Mask-painting canvas (fabric.js or Konva) for in-browser inpainting. <br>– Live preview: convert base-64 from backend to `Blob` → `<img>`/download link. <br>– Job status via WebSocket/SSE if generation queues get long.                                                                                                                           |
| **API Gateway / BFF (backend-for-frontend)** | **FastAPI** (Python 3.12) or **Express** (Node)        | – Auth (JWT / session) & user throttling. <br>– Handles multipart uploads, streams files to OpenAI without persisting when possible. <br>– Normalises our own REST routes:<br>&nbsp;&nbsp;`POST /v1/generate` → wrapper around `images.generate`<br>&nbsp;&nbsp;`POST /v1/edit` → wrapper around `images.edit`<br>&nbsp;&nbsp;`POST /v1/mask/auto` → optional convenience endpoint that calls `images.edit` to _create_ a mask (per example). |
| **Worker / queue (optional but wise)**       | **Celery** + Redis (if Python) or BullMQ (if Node)     | – Off-loads long-running calls so web server stays snappy. <br>– Enables retry, concurrency limits, cost tracking.                                                                                                                                                                                                                                                                                                                            |
| **Object storage**                           | S3 / DigitalOcean Spaces / MinIO                       | – Persistent storage of user uploads, generated images, derived masks. <br>– Signed URLs let the front-end fetch large images directly.                                                                                                                                                                                                                                                                                                       |
| **Database**                                 | Postgres (Supabase or RDS)                             | – Users, jobs, parameters, billing counters, “gallery” metadata.                                                                                                                                                                                                                                                                                                                                                                              |
| **Secrets & config**                         | Vault, AWS Secrets Manager or `.env` mounted in Docker | – Stores `OPENAI_API_KEY`, DB creds, etc. Never expose to browser.                                                                                                                                                                                                                                                                                                                                                                            |
| **CI/CD**                                    | GitHub Actions → Docker images → Fly.io / AWS ECS      | – Lint, test, build images, deploy on main branch.                                                                                                                                                                                                                                                                                                                                                                                            |
| **Observability**                            | Grafana / Datadog; Sentry for FE                       | – Track API latency, OpenAI cost per user, error rates.                                                                                                                                                                                                                                                                                                                                                                                       |

---

#### Back-end flow (generate)

1. **POST `/v1/generate`** receives JSON:
   ```json
   {
     "prompt": “…”, "size":"1024x1536",
     "n":2, "quality":"high",
     "background":"transparent",
     "format":"png"
   }
   ```
2. Validate quota → enqueue job.
3. Worker calls `client.images.generate(**payload)`.
4. Decode `b64_json` → store PNG to S3.
5. Persist job record, return `{status:"succeeded", urls:[…]}`; stream via WebSocket to FE.

#### Back-end flow (edit / inpaint)

1. FE sends multipart form with: `prompt`, `files[]=image1…`, optional `mask`.
2. Gateway uploads originals to S3 (keeping signed URLs) or streams directly.
3. Worker builds `image=[ open(file1, "rb"), … ]`, plus `mask` if provided, and forwards to `client.images.edit`.
4. Decode, store, respond.

---

### Front-end UX blueprint

1. **Tabs:** “Generate”, “Edit / Inpaint”, “History”.
2. **Generate tab**
   - Prompt textbox (autosize).
   - Advanced drawer for _size, quality, background, n, format, compression_.
   - “Generate” button → spinner → gallery grid.
3. **Edit / Inpaint tab**
   - Drag-and-drop images (max 10).
   - Optional mask upload or **Paint Mask** button → opens canvas overlay.
   - Same advanced-options drawer.
   - “Generate new image” button.
4. **History**
   - Table or Masonry grid showing past jobs, parameters, costs.
   - Click → pops modal with full-res download & parameters JSON.

All state management can live in React Query/Zustand; images returned as signed URLs avoid huge blobs in Redux.

---

### Key engineering considerations & forward-thinking extensions

| Topic                       | Guidance                                                                                                                                            |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Cost control**            | Record every `usage.total_tokens` (if exposed) or estimate cost per call × «model rate». Add daily spending caps per user and a global kill-switch. |
| **Rate limiting & abuse**   | Short-term: `X-RateLimit-*` headers + Redis counters. Long-term: credit wallet tied to billing.                                                     |
| **Content policy**          | Expose the API’s `moderation` parameter, default to `auto`, offer “Low filter” only to verified/paid users.                                         |
| **Mask generation helpers** | Integrate Segment Anything model (Meta) in browser (WebAssembly) to let users click and auto-segment, then export as PNG mask with α-channel.       |
| **Streaming base-64**       | For huge images you can “chunk” the base-64 and progressively render; not necessary for ≤1536 px but future-proofs 4K support.                      |
| **Plugin style**            | Wrap the BFF in an OpenAI Function Calling manifest so the same backend serves ChatGPT plugins or Agent actions.                                    |
| **Mobile & offline**        | A React Native wrapper can share 80 % of code; caching via SQLite and resumable uploads (tus.io protocol) handles flaky networks.                   |
| **Future model drops**      | Keep the model name configurable; surface `/v1/models` to display supported image models once OpenAI exposes that.                                  |
| **Compliance / privacy**    | Storing user-uploaded images might constitute “biometric data” in some jurisdictions; add explicit consent and a GDPR deletion workflow.            |

---

### Road-map (sprints)

| Sprint                                       | Deliverables                                                         |
| -------------------------------------------- | -------------------------------------------------------------------- |
| **0 — Setup** (½ week)                       | Repo, Docker, CI/CD skeleton, ENV secret handling.                   |
| **1 — MVP Generate** (1 week)                | `/v1/generate` endpoint; React UI; single-image generation; history. |
| **2 — Image Edit** (1 week)                  | Multiple image upload, mask upload, OpenAI `images.edit` pipeline.   |
| **3 — Mask Painter & Auto-mask** (1 week)    | Canvas mask painting, optional SAM auto-mask.                        |
| **4 — Scalability & Observability** (1 week) | Redis/Bull queue, cost dashboard, Sentry alerts.                     |
| **5 — Polish & paywall** (1 week)            | Auth, Stripe, role-based limits, UI polish, docs.                    |

---

### Current Implementation Highlights

- Supports both **generation** and **multi-image editing** via `/generate` and `/edit` endpoints.
- Client-side image preview and save via `<img>` and `data_uri`.
- Saves image output locally in `saved_images/` with timestamped filenames.
- Environment config is via `.env` + `python-dotenv`.

---

- Set compression to 100 by default, make it non-resettable if png image type is chosen

---

This project aims to implement the OpenAI Image Generator API and allow the user to explore all its functionalities.

We have implemented a test bed for developmental and personal use only. The details are attached as follows.

First, let us continue enhancing our test bed to include all the features. Suggest the next step and prompt me for approval first before we begin coding.

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

### Current Implementation Highlights

- Supports both **generation** and **multi-image editing** via `/generate` and `/edit` endpoints.
- Client-side image preview and save via `<img>` and `data_uri`.
- Saves image output locally in `saved_images/` with timestamped filenames.
- Environment config is via `.env` + `python-dotenv`.

---

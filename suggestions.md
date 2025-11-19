# UX and Functionality Improvements

- Add inline validation and feedback on the playground form: surface remaining `n` range, block transparent backgrounds when `gFmt` is `jpeg`, and show server errors next to their related controls (not just via toast).
- Expand `/edit` output handling: the backend currently accepts `n` but always returns only `data[0]`; either remove `n` for edit or return all variants with a gallery like `/generate` to avoid silent loss of results.
- Make masking and out-painting touch-friendly: add pointer/touch events and a simple “tap to toggle mask” mode so tablets can use the canvas.
- Improve saved-asset discovery: render small “Download” / “Open saved copy” actions under each generated image using the `/saved/<file>` URL returned by the server.
- Provide quick-start presets: seed the page with example prompts (from `example_prompts.md`) and presets for size/quality (“speed”, “quality”, “outpaint”) to shorten first-success time.
- Preserve masking work across edits: avoid resetting the mask/blob state after a submit so users can chain edits without reloading images.
- Support drag-and-drop for reference images and masks to speed up multi-image workflows.
- Add short per-field help/constraints (background, moderation, quality, compression) to reduce retries and mirror API rules.

# Foundational and Validation

- Harden server-side validation in `app.py`: restrict `output_format` to `png|jpeg|webp`, clamp `size` to known values, and enforce `background=transparent` compatibility to stop crafted requests from bypassing client checks.
- Return structured error details to the UI (e.g., error id with link to `app.log`) so failures are debuggable without shell access.
- Add a call history panel (last ~5 requests with prompt + params + thumbnail) persisted in `localStorage` to aid iteration.
- For out-painting, show a checkerboard under the mask canvas and a “show only masked area” toggle to clarify what is removed/kept.

# Developer Experience

- Split the monolithic script in `templates/index.html` into small modules (mask tools, API client, UI state) for readability and maintenance.
- Add a smoke test that hits `/generate` with a 1×1 transparent stub to catch regressions before manual testing.

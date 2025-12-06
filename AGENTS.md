# Agent Notes

## docs/OPENAI_API_FLOW.md
- Describes how the Flask backends call OpenAI: image generation/edit endpoints use `gpt-image-1`; responses playground uses `gpt-5`.
- Shows shared client setup with `OPENAI_API_KEY` from `.env`, fail-fast behavior, and required dependencies.
- Details `/generate` flow (validation for prompt/n/transparency, allowed kwargs, persistence to `saved_images/`, structured 400/500 errors).
- Details `/edit` flow (reference image checks, mask validation/auto-mask, optional args, decoding/saving the returned image, error handling).
- Explains validation/fallback mechanics (size/mode/dimension guards, transparency rules, mask conversion, logging).
- Covers frontend interactions for image playground (FormData fetches, client-side checks, spinners/toasts, mask/out-paint UI) and responses playground (JSON POST, word limits, inline status).

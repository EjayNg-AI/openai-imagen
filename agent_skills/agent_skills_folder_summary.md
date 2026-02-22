# Agent Skills Folder Summary

This folder is a compact documentation set about the Agent Skills format and how to use skills with Codex. It combines:

- Conceptual overviews (what skills are and why they matter)
- Integration guidance (how an agent discovers, loads, and activates skills)
- Formal-ish specifications (required fields, directory structure, and best practices)
- Codex-specific usage notes

## Markdown Files and What They Contain

- `overview_of_agent_skills.md`: High-level explanation of Agent Skills, including purpose, benefits, and example capability areas (domain expertise, workflows, interoperability).
- `introduction_to_agent_skills.md`: Introductory guide to skill structure (`SKILL.md` + optional folders), progressive disclosure, and required frontmatter (`name`, `description`).
- `skill_integration.md`: Implementation-oriented guide for adding skills support to an agent, covering discovery, metadata loading, context injection, and activation flow.
- `skills_detailed_specifications.md`: Detailed format/spec reference for skills, including frontmatter constraints, optional fields, recommended sections, optional directories, and file-reference conventions.
- `codex_agent_skills_specifications.md`: Codex-focused specification describing how Codex invokes skills, where it searches for them, config toggles, optional `agents/openai.yaml`, and operational best practices.

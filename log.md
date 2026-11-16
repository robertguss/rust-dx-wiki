# Log

## [2026-11-16] panel | Wiki created, 35 claims listed, research panel seated

Goal set with the user: find something to build. Scope: everything short of language changes. Pain areas: edit-run loop, AI-agent loop, CI and build infrastructure, editor and diagnostics.

## [2026-11-16] panel | Three seats reported; claims reconciled

Primary (GPT-6.1 Sol): 28 confirmed, 1 refuted, 2 outdated, 4 unverified. Skeptic (Claude Fable 5.2): 30 confirmed, 5 outdated. Recency (Gemini 4 Carbon): 32 confirmed, 2 outdated, 1 refuted. Reconciled: 29 confirmed, 4 outdated (6, 7, 11, 16), 2 contested (9, 35). Disputed quotes were re-fetched into `raw/manual/`. One Recency date was wrong: rust#162848 merged 2026-11-13, not 2026-09-16.

Known breaches of the raw rule: the Skeptic overwrote two raw files on refetch, and its Reddit file holds only a bot wall.

## [2026-11-16] ingest | Wiki pages written from the panel reports

Created overview and five topic pages. Commercial build services, error messages, debugging and macro opacity are not yet covered.

## [2026-11-16] query | Why are Rust compile times slow?

Fetched eight explanatory sources into `raw/manual/` and filed the answer as `wiki/topics/why-rust-compiles-slowly.md`.

## [2026-11-16] query | Is a build-diagnosis tool worth building?

Ran a pre-registered kill test on ripgrep, helix, atuin, nushell and meilisearch (`experiments/build-diagnosis-kill-test/`). Verdict: no. The generic preset delivers most of the configuration-level win; project-specific fixes cleared the 20% bar on 2 of 5 projects against a required 3.

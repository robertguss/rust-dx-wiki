# Rust DX Wiki

An LLM-maintained wiki ([pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)) about speeding up Rust compile times and improving Rust developer experience without changing the language.

Goal: map what exists, find the gaps, and pick something worth building. In scope: rustc internals, backends, linkers, cargo, caches, build systems, editor tooling, AI-agent tooling, hosted services. Out of scope: language changes.

## Layers

- `raw/` holds fetched pages and search results exactly as retrieved. Never edit a file in `raw/` after it is written.
- `wiki/` holds the pages agents write and keep current.
- `index.md` lists every wiki page with a one-line summary. Read it first.
- `log.md` is an append-only timeline.

## raw/

- One file per fetched page: `raw/<role>/<YYYY-MM-DD>-<slug>.md`, starting with the source URL on line 1 and the fetch date on line 2.
- Search results go in `raw/<role>/searches.jsonl`, one JSON object per query.
- `<role>` is the panel seat that fetched it (`primary`, `skeptic`, `recency`) or `manual`.

## wiki/

- `wiki/claims.md`: the numbered claims ledger with verdict and evidence per claim.
- `wiki/projects/<name>.md`: one page per tool, project, or product.
- `wiki/topics/<name>.md`: one page per concept or pain area.
- `wiki/ideas/<name>.md`: buildable opportunities.
- `wiki/overview.md`: the current synthesis.

Page rules:

- Start each page with frontmatter: `updated` (date), `status` (for projects: active, stalled, dead, unstable, stable), `sources` (list of `raw/` paths).
- Every factual sentence cites a `raw/` file or a URL with the date it was fetched. A claim with no fetched source is marked `unverified`.
- Link related pages with relative markdown links.
- When a new source contradicts a page, fix the page and note the change in `log.md`.

## Workflows

- Ingest: save the source to `raw/`, update or create the affected wiki pages, update `index.md`, append to `log.md`.
- Query: read `index.md`, read the relevant pages, answer with citations, and file any answer worth keeping as a wiki page.
- Lint: look for contradictions, stale claims, orphan pages, and missing pages; fix them and log it.

Log entries start with `## [YYYY-MM-DD] <ingest|query|lint|panel> | <title>`.

## Tools

Exa is out of credits. Use TinyFish: `tinyfish search query "..."` and `tinyfish fetch content get <url>`.

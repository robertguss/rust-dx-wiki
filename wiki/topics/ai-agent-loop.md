---
updated: 2026-11-16
sources:
  - raw/skeptic/2026-11-16-report.md
  - raw/recency/2026-11-16-report.md
  - raw/primary/2026-11-16-report.md
  - raw/skeptic/2026-11-16-github-repo-metadata-discovery.md
---

# AI-agent loop

What happens when several coding agents work on one Rust project at once, each in its own git worktree.

## The pain

- Each worktree gets its own `target/`, so every agent recompiles the same dependencies and disk fills up (claims 20, 21, 25 in the [ledger](../claims.md)).
- Sharing one target directory instead makes agents queue behind Cargo's build-directory lock (claim 17).
- Demand signal from the Hacker News thread on the September 2026 compiler-speed post: "Most projects my fleet works on are in other languages (TS, Go, Elixir) and can comfortably handle 10+ agents working in parallel, but not rust. I had to cap the fleet to 5 workers and build a dedicated resource monitor to step in and tidy up every time the disk almost filled up" (`raw/skeptic/2026-11-16-hn-speed-up-rust-compiler-sept-2026.md`).
- The rust-analyzer side: "it becomes pretty common for folks to have a bunch of rust-analyzer instances running" ([rust-analyzer#22765](https://github.com/rust-lang/rust-analyzer/issues/22765); `raw/skeptic/2026-11-16-rust-analyzer-22765-daemonize.md`).

## Who is already here

Stars and dates are from the GitHub API on 2026-11-16.

| Tool | What it does | Traction |
| --- | --- | --- |
| [Worktrunk](https://github.com/max-sixty/worktrunk) | Git worktree manager "designed for running AI agents in parallel", with copy-on-write build caches. Not Rust-specific. | 12,549 stars |
| [kache](https://github.com/kunobi-ninja/kache) | Content-addressed compiler cache for Rust, C/C++ and CUDA; restores outputs across worktrees and CI. | 1,468 stars, created 2026-02-15 |
| [mbx (mr-boxington)](https://github.com/jdx/mr-boxington) | Cargo wrapper: shared store, target-directory cleanup, one job budget across concurrent builds. From the author of mise. | 773 stars, created 2026-08-20 |
| [Symposium](https://github.com/symposium-dev/symposium) | `cargo agents`: installs crate-matched skills, hooks and MCP servers into coding agents. | 438 stars |
| [cargo-reapi](https://github.com/TamedTornado/cargo-reapi) | Cross-worktree build reuse for multi-agent hosts. | 27 stars |
| [analyzed](https://github.com/zetaloop/analyzed) | One shared rust-analyzer daemon for many clients and agents. | 15 stars |
| [cargo-worktree](https://github.com/SuccinctPaul/cargo-worktree) | Build isolation between worktrees. One-day project. | 7 stars |
| [Ferry](https://lib.rs/crates/ferry-rs) | Builds one warm base per commit and forks warm worktrees for agents. | 2 stars, first published 2026-10-24 |
| [Sluice](https://github.com/josegarridodigio/sluice) | Runs each gate (tests, lints) once per git tree under a global budget, with an MCP server. | 2 stars |
| [Cargo Steward](https://github.com/0xdoublesharp/cargo-steward) | Warms worktree builds, prunes artifacts, bounds concurrent compiler work. | 1 star, created 2026-11-08 |
| [mcp-language-server](https://github.com/isaacphi/mcp-language-server) | Generic LSP-to-MCP bridge; the route rust-analyzer maintainers point to. | 1,619 stars |
| [rust-analyzer-mcp](https://github.com/zeenix/rust-analyzer-mcp) | MCP server over rust-analyzer. | 88 stars |

Upstream is moving too: Cargo's cross-workspace cache is a 2026 goal, aimed at nightly (`raw/primary/2026-11-16-cross-cache.md`), and sccache 0.19.0 added `SCCACHE_BASEDIRS` for cache hits across checkouts (`raw/recency/2026-11-16-sccache-rust-md-full.md`). rustup is getting process-safe toolchain operations for concurrent runs (`raw/recency/2026-11-16-goals-2026-process-safe-rustup.md`).

## What looks less crowded

- A shared rust-analyzer across agents and worktrees: one 15-star project and one open upstream issue.
- Machine-wide scheduling of concurrent Cargo runs: mbx advertises a shared job budget; Sluice and Cargo Steward are tiny.
- Deduplicating verification (the same `cargo test` or `clippy` on the same tree by several agents): only Sluice.
- Nothing fetched measures or reports where an agent's wall-clock and tokens go in a Rust loop (waiting on cargo, re-reading compiler errors). This is an absence in what the panel fetched, not a verified gap.

Related: [Cargo, caching and build infrastructure](cargo-caching-build-infra.md), [Inner loop and editor](inner-loop-editor.md).

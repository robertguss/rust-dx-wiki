---
updated: 2026-11-16
sources:
  - raw/primary/2026-11-16-report.md
  - raw/skeptic/2026-11-16-report.md
  - raw/recency/2026-11-16-report.md
  - raw/primary/2026-11-16-compiler-survey.md
---

# Inner loop and editor

The edit, build, run, test cycle and the editor around it.

## What the survey says hurts

From the [2025 Compiler Performance Survey](https://blog.rust-lang.org/2025/09/10/rust-compiler-performance-survey-2025-results) (2025-09-10; `raw/primary/2026-11-16-compiler-survey.md`):

- "Waiting too long for an incremental rebuild after making a small source code change was by far the most common complaint".
- "More than 35% users said that they consider the IDE and Cargo blocking one another to be a big problem."

A counterweight: a March 2026 synthesis of Rust Vision Doc interviews noted that no interviewee said compile time currently blocked them, though enterprise users worried about scale (`raw/recency/2026-11-16-rust-challenges-2026.md`). The State of Rust survey also moved debugging from 2nd to 4th among reported problems (`raw/primary/2026-11-16-state-survey.md`).

## Tools

| Tool | Role | Status |
| --- | --- | --- |
| [Bacon](https://github.com/Canop/bacon) | Background checker; replaced cargo-watch | Active, 3,478 stars |
| [cargo-watch](https://github.com/watchexec/cargo-watch) | File watcher | "on life support" (claim 28 in the [ledger](../claims.md)) |
| [cargo-nextest](https://nexte.st/) | Test runner, "Up to 3x as fast as cargo test" for execution | Active, release 2026-11-13 |
| [subsecond](https://docs.rs/subsecond/latest/subsecond/) | Hot-patching of running Rust code, plus "ThinLinking" for faster dev builds | Experimental; needs a runner such as the Dioxus CLI (claim 27) |
| Bevy dynamic linking | Link the engine as a dynamic library in dev | Recommended by Bevy (claim 32) |
| [cargo-wizard](https://github.com/Kobzol/cargo-wizard) | Applies fast-compile presets | Active, v0.2.3 2026-04-13 |
| rust-analyzer separate target dir | Stops the editor and `cargo build` blocking each other, at the cost of disk | Off by default (claim 30) |

## Editor and diagnostics

- rust-analyzer shipped trait-error diagnostics in May 2026 (`raw/recency/2026-11-16-ra-changelog-326.md`).
- rust-analyzer maintainers consider an LLM interface out of scope (claim 33); a request to run it as a shared daemon is open (`raw/skeptic/2026-11-16-rust-analyzer-22765-daemonize.md`).
- An RFC proposes letting crates hint that they need optimization in dev builds (`raw/recency/2026-11-16-rfc-3924-min-opt-level.md`).

## Not yet researched

The panel's claims were weighted toward build speed. Error-message quality, debugger experience, and macro and proc-macro opacity have no fetched sources in this wiki yet.

Related: [Compiler, backends and linkers](compiler-backends-linkers.md), [AI-agent loop](ai-agent-loop.md).

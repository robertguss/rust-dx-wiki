---
updated: 2026-11-16
sources:
  - raw/skeptic/2026-11-16-report.md
  - raw/manual/2026-11-16-goal-397.md
  - raw/manual/2026-11-16-fast-builds-roadmap.md
---

# Failures and stalls

Projects in this space that died, stalled or lost their edge, and why. Collected by the Skeptic seat on 2026-11-16 (`raw/skeptic/2026-11-16-report.md`).

| What | What happened | Why |
| --- | --- | --- |
| [Production-ready Cranelift goal](https://github.com/rust-lang/goals/issues/397) (2025H2) | Closed with no work done | "We did not receive the funding we needed to work on this goal"; also "the amount of time spent in codegen for realistic changes to real code bases was smaller than expected" |
| [Fleet](https://github.com/suptejas/fleet) | "The blazing fast build tool for Rust", 2,424 stars; last code commit 2023-04-13, no releases | Not stated; issues unanswered since 2023 |
| [cargo-watch](https://github.com/watchexec/cargo-watch) | Archived | Maintainer stopped and points to Bacon |
| [Cargo build-dir layout v2](https://github.com/rust-lang/cargo/pull/17187) | Stabilized, reverted a day later in July 2026, then shipped in 1.100.0 | "We felt it would be safer to revert so that are not on a shot clock to fix the issues." |
| [Cargo per-user artifact cache](https://github.com/rust-lang/cargo/issues/5931) | Open since 2018; restarted as the 2026 cross-workspace cache goal | Hard design: cache poisoning, garbage collection, platform differences |
| [Cargo `target/` garbage collection](https://github.com/rust-lang/cargo/issues/13136) | Open since 2023; PR open | Not stated |
| Wild's speed lead over mold | Mold's August 2026 benchmarks put Wild behind | Mold 2.42 got faster |
| [MCP inside rust-analyzer](https://github.com/rust-lang/rust-analyzer/issues/20340) | Request closed the day it was filed | Maintainers see it as out of scope |
| [cargo-remote](https://github.com/sgeisler/cargo-remote) | No push since 2024-06-12 | Not stated |
| Relink Don't Rebuild funding | Marked red at $70,000 in the roadmap's funding table | Meaning of the marker not checked; it reads as unfunded |
| Crate slicing 2026 goal | "Not accepted" | Not stated (`raw/recency/2026-11-16-goals-2026-crate-slicing.md`) |

## Patterns

- Money, not ideas, is the limit upstream: three roadmap items are marked red in the funding table (`raw/manual/2026-11-16-fast-builds-roadmap.md`).
- A build-speed gain that looks large in one phase shrinks end to end. Cranelift's 20% on code generation became 5% to 12% on real incremental builds.
- Cargo features in this area take years and can be reverted after stabilizing, so a tool that depends on Cargo's internal layout carries that risk.
- A "blazing fast build tool" that wraps existing tricks (Fleet) did not last; the 2026 entrants that got traction (kache, mbx) ship their own cache.

Related: [Compiler, backends and linkers](compiler-backends-linkers.md), [Cargo, caching and build infrastructure](cargo-caching-build-infra.md).

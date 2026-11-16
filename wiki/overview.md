---
updated: 2026-11-16
sources:
  - raw/primary/2026-11-16-report.md
  - raw/skeptic/2026-11-16-report.md
  - raw/recency/2026-11-16-report.md
  - raw/manual/2026-11-16-fast-builds-roadmap.md
---

# Overview

The current synthesis. Goal: find something worth building that speeds up Rust compile times or improves Rust developer experience without changing the language.

## Where things stand on 2026-11-16

The problem is real and measured. Slow incremental rebuilds are the top compile-time complaint, and about 45% of surveyed people who left Rust named compile times as a reason ([claims 1 to 3](claims.md)).

The Rust project is working on it through the 2026 Fast Builds roadmap, which says plainly that "we're past the point of easy wins" (`raw/manual/2026-11-16-fast-builds-roadmap.md`). Nothing transformative is on stable yet:

- On stable: `rust-lld` on one Linux target, `build.build-dir`, the new build-dir layout, steady single-digit compiler speedups.
- On nightly only: Cranelift, the parallel front end, relink-don't-rebuild, TPDE (and that one needs a self-built compiler).
- Expected gains are modest so far. Cranelift gives 5% to 12% on real incremental builds, not the 20% often quoted.
- Several of the highest-impact items are short of funding.

See [Compiler, backends and linkers](topics/compiler-backends-linkers.md).

Outside the compiler, 2026 was the year of the cross-worktree cache. kache and mbx both launched and gained traction, a crop of small agent-focused tools followed, and Cargo is building its own cache. See [AI-agent loop](topics/ai-agent-loop.md) and [Cargo, caching and build infrastructure](topics/cargo-caching-build-infra.md).

## What the panel corrected

- "The agent build loop is empty ground" was wrong. It is the most active area found.
- "Cranelift is about 20% faster" overstated the end-to-end gain, and its production-ready goal died unfunded.
- "Wild beats mold" is no longer safe to say; mold was rewritten in Rust (3.0.0) and got faster.
- "No TPDE backend for Rust" went stale three days before this research: `-Z llvm-tpde` merged on 2026-11-13.

## Where the gaps appear to be

These are leads for brainstorming, not verified gaps. Each is an absence in what was fetched.

1. **Shared rust-analyzer for many agents and worktrees.** One 15-star project; upstream issue open; maintainers decline LLM-facing work.
2. **Machine-wide build scheduling.** Many concurrent Cargo runs oversubscribe CPU and memory. mbx has a shared job budget; the roadmap lists "Better build parallelization" as "Future" with no 2026 owner.
3. **Deduplicated verification.** Several agents run the same tests and lints on the same tree. Only Sluice (2 stars) addresses it.
4. **Build diagnosis.** The profiling tools exist but are separate and manual. Nothing fetched takes a workspace and says "your build is slow because of X; here is the fix".
5. **Agent-loop measurement.** Nothing fetched measures where an agent's time and tokens go in a Rust edit-check loop.
6. **Unfunded upstream work.** Relink-don't-rebuild ($70,000), polymorphization and target-directory size are marked red in the roadmap's funding table. Crate slicing has a claimed 1.4x to 30x upside and no accepted goal.
7. **Hot-patching beyond Dioxus.** subsecond is framework-neutral in principle but needs the Dioxus CLI as runner.

## Not yet covered

- Commercial build services (Depot, WarpBuild and others) were only skimmed.
- Error messages, debugging and macro opacity have no sources yet.
- No usage data beyond GitHub stars for any tool.
- Nothing here was installed or benchmarked; every number is the source's own.

See [Failures and stalls](topics/failures-and-stalls.md) for what has already been tried and dropped.

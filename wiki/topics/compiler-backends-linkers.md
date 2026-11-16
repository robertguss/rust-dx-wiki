---
updated: 2026-11-16
sources:
  - raw/manual/2026-11-16-fast-builds-roadmap.md
  - raw/manual/2026-11-16-cranelift-2026-goal.md
  - raw/manual/2026-11-16-tpde-internals.md
  - raw/manual/2026-11-16-wild-readme.md
  - raw/manual/2026-11-16-wild-vs-mold.md
  - raw/manual/2026-11-16-mold-v3-release.md
  - raw/manual/2026-11-16-nnethercote-sept-2026.md
  - raw/recency/2026-11-16-report.md
---

# Compiler, backends and linkers

The Rust project's own map of this area is the 2026 [Fast Builds roadmap](https://goals.rust-lang.org/2026/roadmap-fast-builds.html). Its first design axiom: "No one thing. Particularly for batch compilation, we're past the point of easy wins."

## State of each lever

| Lever | Status on 2026-11-16 | Measured gain | Source |
| --- | --- | --- | --- |
| `rust-lld` default linker | Stable since 1.90 on `x86_64-unknown-linux-gnu` only | not fetched | [claim 4](../claims.md) |
| Parallel front end | Nightly only; 2 threads became the nightly default on 2026-11-13; stabilization plan accepted | not fetched | claim 8 |
| Cranelift backend | Nightly only. The "production-ready" goal closed unfunded; the 2026 goal targets a 2x speedup inside the backend and is funded at $65,000 | 10 to 15% per crate on the rustc benchmark suite; 5% to 12% on incremental Zed builds | claims 5 to 7 |
| TPDE mode (`-Z llvm-tpde`) | Merged 2026-11-13. Needs a locally built compiler, Linux only, falls back to LLVM | 10 to 20x on code generation alone; 3 to 4% wall time on ripgrep in the PR | claims 15, 16; `raw/recency/2026-11-16-rust-pr-164108-llvm-tpde.md` |
| Relink, don't rebuild | Nightly as `-Z public-api-hash`; stabilization prep in 2027; marked red in the funding table at $70,000 | roadmap says "Massive speedup of rebuilds in large multi-crate projects" | claim 12 |
| `-Z hint-mostly-unused` | Unstable | not fetched | claim 13 |
| `-Z cache-proc-macros` | Unstable; derive macros only; no purity check | not fetched | claim 14 |
| Incremental Systems Rethought | Accepted 2026 goal: share incremental work between `check`, `build` and `test` | none yet | `raw/recency/2026-11-16-goals-2026-incremental-rethought.md` |
| Polymorphic code generation | Accepted 2026 experiment; marked red in the funding table | none yet | `raw/recency/2026-11-16-goals-2026-polymorphization.md` |
| Crate slicing | "Future" on the roadmap; the 2026 goal proposal was not accepted. `cargo-slicer` is an external proof of concept | roadmap: "anywhere from 1.4x to 30x" in experiments | `raw/recency/2026-11-16-goals-2026-crate-slicing.md` |
| Steady compiler optimization | Ongoing | "The mean wall-time reduction was 4.57%" over two months to 2026-09-28 | `raw/manual/2026-11-16-nnethercote-sept-2026.md` |
| New `debug` profile | Stable in 1.99, "preparation for transitioning the `dev` profile away from debugging" | none yet | `raw/recency/2026-11-16-rust-releases-md.md` |

## Linkers

- mold 3.0.0 (2026-10-05) is a rewrite: "we have rewritten mold from C++ to Rust, and this is the first release of the Rust version" (`raw/manual/2026-11-16-mold-v3-release.md`).
- Wild 0.11.0 (2026-10-24) supports Linux and WebAssembly. Incremental linking, Mach-O and Windows are on its "looking ahead" list (`raw/manual/2026-11-16-wild-readme.md`).
- Which is faster is [contested](../claims.md): each project's benchmarks favour itself, and the result flips with filesystem and flags (`raw/manual/2026-11-16-wild-vs-mold.md`).
- Wild is on the Fast Builds roadmap as "Incremental, efficient linking with Wild", "2026 and beyond".

## Reading this as a builder

- The deep wins here are compiler-team work with named owners and, in several cases, missing money: relink-don't-rebuild, polymorphization and target-directory size are all marked red in the roadmap's funding table.
- The roadmap lists "Better build parallelization" (Cargo and rustc coordination) and "Crate slicing" as "Future", with no owner in 2026.
- Tools for finding out why a build is slow exist but are separate and manual: `cargo build --timings`, `-Z self-profile` with measureme, `cargo-llvm-lines`, `cargo-bloat` (`raw/primary/2026-11-16-report.md`). `cargo-wizard` applies presets but does not diagnose. Cargo 1.100 added a built-in `cargo::unused_dependencies` lint (`raw/manual/2026-11-16-rust-1-100-0.md`).

Related: [Cargo, caching and build infrastructure](cargo-caching-build-infra.md), [Failures and stalls](failures-and-stalls.md).

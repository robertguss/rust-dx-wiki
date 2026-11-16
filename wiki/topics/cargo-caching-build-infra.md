---
updated: 2026-11-16
sources:
  - raw/primary/2026-11-16-report.md
  - raw/skeptic/2026-11-16-report.md
  - raw/recency/2026-11-16-report.md
  - raw/manual/2026-11-16-rust-1-100-0.md
  - raw/manual/2026-11-16-depot-rust-ci-guide.md
  - raw/manual/searches.jsonl
---

# Cargo, caching and build infrastructure

## What Cargo does and does not do today

- It locks the whole build directory per build; fine-grained locking is unstable and has an open deadlock bug (claims 17, 18 in the [ledger](../claims.md)).
- `build.build-dir` is stable since 1.91 and the new per-build-step layout since 1.100.0, after one stabilize-then-revert in July 2026 (claim 19; `raw/skeptic/2026-11-16-cargo-pr-17187-revert-build-dir-layout-v2.md`).
- No cross-workspace cache yet. It is a 2026 goal for nightly; the parent issue has been open since 2018 (claim 21; `raw/skeptic/2026-11-16-cargo-5931-per-user-cache.md`).
- No prebuilt library dependencies (claim 22).
- It cleans its global download cache but not `target/`; a PR is open (claim 25).
- Since 1.99: "incremental compilation is now disabled by default when running in CI" (`raw/recency/2026-11-16-rust-releases-md.md`).
- Target-directory size reduction is a 2026 goal with a nightly experiment announced 2026-08-18 (`raw/primary/2026-11-16-target-reduction.md`).
- Cargo plumbing commands, machine-oriented interfaces for external tools, are a 2026 goal that says it "needs contributors" (`raw/primary/2026-11-16-cargo-plumbing.md`).

## Caches

| Tool | Scope | Notes |
| --- | --- | --- |
| [sccache](https://github.com/mozilla/sccache) | Local and remote compiler cache; the one the Cargo Book names | 7,934 stars. Cannot cache incremental crates (claim 23). 0.19.0 added `SCCACHE_BASEDIRS` and `SCCACHE_ALLOW_INCREMENTAL`. |
| [kache](https://github.com/kunobi-ninja/kache) | Content-addressed cache across worktrees and CI | 1,468 stars, created 2026-02-15 |
| [mbx](https://github.com/jdx/mr-boxington) | Cargo wrapper with shared store, cleanup and job budget | 773 stars, created 2026-08-20 |
| [Swatinem/rust-cache](https://github.com/Swatinem/rust-cache) | GitHub Actions cache | In 164,864 workflow files (claim 26) |
| [cargo-chef](https://github.com/LukeMathWalker/cargo-chef) | Docker layer caching of dependencies | Active |
| [cargo-hakari](https://crates.io/crates/cargo-hakari) | Workspace-hack crates to avoid feature-unification rebuilds | unverified; not fetched by the panel |

## Remote caching and execution

- Bazel with rules_rust and Buck2 do remote caching and execution; Cargo does not (claim 24). [NativeLink](https://github.com/TraceMachina/nativelink) is an open-source server for them (1,644 stars). [rules_rs](https://github.com/hermeticbuild/rules_rs) is a newer Bazel rule set (116 stars).
- [cargo-remote](https://github.com/sgeisler/cargo-remote) (214 stars) has not been pushed since 2024-06-12.

## Commercial services

Skimmed in one search, not checked by the panel; treat as unverified leads (`raw/manual/searches.jsonl`).

- [Depot](https://depot.dev/blog/guide-to-faster-rust-builds-in-ci): hosted CI runners plus a remote cache that sccache uses as a backend (`raw/manual/2026-11-16-depot-rust-ci-guide.md`).
- [WarpBuild](https://warpbuild.com/solutions/rust-github-actions): hosted runners and cache for GitHub Actions.
- [cargo-burst](https://lib.rs/crates/cargo-burst) and [cargo-green](https://crates.io/crates/cargo-green): Cargo add-ons for remote or sandboxed builds.

Related: [AI-agent loop](ai-agent-loop.md), [Failures and stalls](failures-and-stalls.md).

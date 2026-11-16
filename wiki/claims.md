---
updated: 2026-11-16
sources:
  - raw/primary/2026-11-16-report.md
  - raw/skeptic/2026-11-16-report.md
  - raw/recency/2026-11-16-report.md
---

# Claims ledger

The claims the "build something for Rust compile times and DX" idea rests on. They were written from model recall on 2026-11-16 and then checked by a three-seat research panel the same day: Primary (GPT-6.1 Sol), Skeptic (Claude Fable 5.2), Recency (Gemini 4 Carbon). Every quote below comes from a page fetched on 2026-11-16.

Verdicts: `confirmed`, `refuted`, `outdated`, `unverified`, `contested`. A claim is `confirmed` only when at least one seat confirmed it and none refuted or outdated it. The "Seats" column shows Primary / Skeptic / Recency (C confirmed, O outdated, R refuted, U unverified).

Result: 29 confirmed, 4 outdated, 2 contested.

## Problem

| # | Claim | Verdict | Seats | Evidence |
| --- | --- | --- | --- | --- |
| 1 | The most recent annual State of Rust survey lists slow compilation among the biggest problems Rust users report. | confirmed | C/C/C | "resource usage (slow compile times and storage usage) is still up there" ([2025 State of Rust results](https://blog.rust-lang.org/2026/03/02/2025-State-Of-Rust-Survey-results), 2026-03-02; `raw/primary/2026-11-16-state-survey.md`) |
| 2 | The 2025 Compiler Performance Survey found slow incremental rebuilds after a small change are the biggest compile-time complaint. | confirmed | C/C/C | "Waiting too long for an incremental rebuild after making a small source code change was by far the most common complaint" ([survey results](https://blog.rust-lang.org/2025/09/10/rust-compiler-performance-survey-2025-results), 2025-09-10; `raw/primary/2026-11-16-compiler-survey.md`) |
| 3 | The 2025 Compiler Performance Survey found slow compile times are a reason some developers stopped using Rust. | confirmed | C/C/C | "Around 45% respondents who answered that they are no longer using Rust said that at least one of the reasons why they stopped were long compile times." (same page) |

## Compiler, backends, linkers

| # | Claim | Verdict | Seats | Evidence |
| --- | --- | --- | --- | --- |
| 4 | On stable Rust, `rust-lld` is the default linker for `x86_64-unknown-linux-gnu`. | confirmed | C/C/C | "target will now use the LLD linker for linking Rust crates by default" ([Rust 1.90.0](https://blog.rust-lang.org/2025/09/18/Rust-1.90.0/), 2025-09-18; `raw/primary/2026-11-16-lld-release.md`). Other Linux targets still use the system linker. |
| 5 | The Cranelift codegen backend is available only on nightly Rust. | confirmed | C/C/C | "Requires using nightly Rust and an unstable Cargo feature" ([Cargo build performance guide](https://doc.rust-lang.org/cargo/guide/build-performance.html); `raw/primary/2026-11-16-build-performance.md`) |
| 6 | The Rust project has a current goal to make the Cranelift backend production-ready. | outdated | O/O/O | The 2025H2 goal closed unfunded: "We did not receive the funding we needed to work on this goal, so no progress has been made." ([goals#397](https://github.com/rust-lang/goals/issues/397), 2025-12-01; `raw/manual/2026-11-16-goal-397.md`). Its 2026 replacement: "We're targeting a 2x speedup inside the `rustc_codegen_cranelift` backend." ([2026 goal](https://goals.rust-lang.org/2026/improve-cg_clif-performance.html); `raw/manual/2026-11-16-cranelift-2026-goal.md`) |
| 7 | The Cranelift backend makes debug-build code generation roughly 20% faster than LLVM on the Rust project's benchmarks. | outdated | C/O/R | The 20% was code generation only, on three large projects, in the closed 2025H2 goal. The current figures: "the average speedup around 10-15% for a single crate compilation in the rustc benchmark suite" and, for incremental builds of Zed, "with `-Cdebug-info=line-tables-only`, cranelift is 12% faster than LLVM" ([2026 goal](https://goals.rust-lang.org/2026/improve-cg_clif-performance.html); `raw/manual/2026-11-16-cranelift-2026-goal.md`) |
| 8 | The parallel front end (`-Z threads`) is nightly-only and not enabled by default on stable. | confirmed | C/C/C | "Requires using nightly Rust and an unstable Rust feature" ([Cargo build performance guide](https://doc.rust-lang.org/cargo/guide/build-performance.html)). Going stale: [rust#162848](https://github.com/rust-lang/rust/pull/162848) "Use 2 parallel frontend threads by default on the nightly and dev channel" merged 2026-11-13 (checked with `gh`). |
| 9 | The Wild linker is actively maintained and benchmarks faster than mold on Linux. | contested | C/O/C | Maintained: release 0.11.0 on 2026-10-24. Speed depends on whose benchmark. Wild's own 0.11.0 charts put mold 3.0.0 behind (`raw/primary/2026-11-16-wild-chart.md`, `raw/recency/2026-11-16-wild-chrome-crel-svg.md`). Wild's author on mold's numbers: "These benchmarks show Wild being substantially slower than Mold" and "Mold has recently gotten considerably faster" ([Lattimore](https://davidlattimore.github.io/posts/2026/09/18/benchmarking-wild-vs-mold.html), 2026-09-18; `raw/manual/2026-11-16-wild-vs-mold.md`). |
| 10 | Wild has not shipped incremental linking. | confirmed | C/C/C | "The plan is to eventually make it incremental, however that isn't yet implemented." ([Wild README](https://github.com/wild-linker/wild); `raw/manual/2026-11-16-wild-readme.md`) |
| 11 | Wild supports only Linux, not macOS or Windows. | outdated | R/O/O | The README's supported list now includes "WebAssembly (wasm32)", and lists "Mach-O support" and "Windows support" under things it is "looking ahead to" (`raw/manual/2026-11-16-wild-readme.md`). |
| 12 | "Relink, don't rebuild" has not shipped in stable Rust. | confirmed | C/C/C | "Relink Don't Rebuild - Prepare for stabilization \| 2027" ([Fast Builds roadmap](https://goals.rust-lang.org/2026/roadmap-fast-builds.html); `raw/manual/2026-11-16-fast-builds-roadmap.md`). It exists on nightly as `-Z public-api-hash` (`raw/skeptic/2026-11-16-rust-158844-rdr-tracking.md`). |
| 13 | rustc has an unstable `-Zhint-mostly-unused` option that defers code generation for unused dependency items. | confirmed | C/C/C | "this option makes the compiler defer as much code generation as possible from functions in the crate, until later crates invoke those functions" ([unstable book](https://doc.rust-lang.org/unstable-book/compiler-flags/hint-mostly-unused.html); `raw/primary/2026-11-16-hint-unused.md`) |
| 14 | rustc has an unstable option that caches proc-macro expansion across incremental builds. | confirmed | C/C/C | "This option instructs `rustc` to cache (derive) proc-macro invocations using the incremental system." ([unstable book](https://doc.rust-lang.org/unstable-book/compiler-flags/cache-proc-macros.html); `raw/primary/2026-11-16-proc-cache.md`). Derive macros only; no purity check. |
| 15 | TPDE compiles LLVM IR about 10 to 20 times faster than LLVM at `-O0`. | confirmed | C/C/C | "Typically, compile times are 10–20x faster than the LLVM -O0 back-end with similar execution time" ([TPDE docs](https://docs.tpde.org/tpde-llvm-main.html); `raw/primary/2026-11-16-tpde-doc.md`). That is code generation, not whole Rust builds. |
| 16 | No TPDE-based rustc backend is usable for general Rust projects today. | outdated | O/C/C | "`rustc` has an experimental TPDE-LLVM backend option which can be used to improve compile times for debug builds. [...] `rustc` supports falling back to regular LLVM codegen if TPDE fails." ([rustc dev guide](https://rustc-dev-guide.rust-lang.org/tpde/internals.html); `raw/manual/2026-11-16-tpde-internals.md`). [rust#164108](https://github.com/rust-lang/rust/pull/164108) "Add unstable `-Zllvm-tpde` flag" merged 2026-11-13. It still needs a locally built compiler: `bootstrap.example.toml` has `#llvm.tpde = false` (checked with `gh`). Linux only. |

## Cargo, caching, build infrastructure

| # | Claim | Verdict | Seats | Evidence |
| --- | --- | --- | --- | --- |
| 17 | Cargo takes an exclusive lock on the build directory, so two cargo commands on the same target directory block each other. | confirmed | C/C/C | "Right now whenever a build happens we lock the entirety of the `target` directory for the whole build" ([cargo#4282](https://github.com/rust-lang/cargo/issues/4282); `raw/primary/2026-11-16-locking-issue.md`) |
| 18 | Finer-grained build-directory locking in Cargo is in progress and not yet stable. | confirmed | C/C/C | "Use fine grain locking instead of locking the entire build cache." ([Cargo unstable reference](https://doc.rust-lang.org/nightly/cargo/reference/unstable.html); `raw/primary/2026-11-16-cargo-unstable.md`). Open deadlock bug: `raw/recency/2026-11-16-cargo-issue-17508-locking.md`. |
| 19 | Cargo stabilized `build.build-dir`. | confirmed | C/C/C | "was stabilized in the 1.91 release" (same page). The new build-dir layout followed in 1.100.0 (`raw/manual/2026-11-16-rust-1-100-0.md`) after one revert (`raw/skeptic/2026-11-16-cargo-pr-17187-revert-build-dir-layout-v2.md`). |
| 20 | Under default settings, separate git worktrees of one project do not share compiled dependency artifacts. | confirmed | C/C/C | "These artifacts are local to the current workspace. This is not ideal as it requires Cargo to rebuild build units when we could simply reuse the artifacts" ([2026 cache goal](https://goals.rust-lang.org/2026/cargo-cross-workspace-cache.html); `raw/primary/2026-11-16-cross-cache.md`) |
| 21 | Cargo has no stable built-in cache that shares compiled dependencies across workspaces. | confirmed | C/C/C | "In 2026, we will design and implement this cache in Cargo, making it available on nightly for users to begin experimenting with." (same page). Not yet on nightly as of the 2026-11-14 update (`raw/skeptic/2026-11-16-goals-626-cargo-cross-workspace-cache.md`). |
| 22 | Cargo has no supported way to download prebuilt binary artifacts for crates.io library dependencies. | confirmed | U/C/C | Rests on absence: "Support for pre-built dependencies" is still open and labelled `S-needs-design` ([cargo#1139](https://github.com/rust-lang/cargo/issues/1139), opened 2015, updated 2026-04-06; `raw/skeptic/2026-11-16-cargo-1139-prebuilt-deps.md`). |
| 23 | sccache cannot cache Rust crates compiled with incremental compilation enabled. | confirmed | C/C/C | "Incrementally compiled crates cannot be cached." ([sccache README](https://github.com/mozilla/sccache); `raw/primary/2026-11-16-sccache.md`). Newer caches (kache, mbx) advertise handling incremental state. |
| 24 | Bazel and Buck2 support remote caching and remote execution of Rust builds, which Cargo does not do natively. | confirmed | C/C/C | "Bazel uses an open-source gRPC protocol to allow for remote execution and remote caching." ([Bazel](https://bazel.build/remote/rbe); `raw/primary/2026-11-16-bazel-remote.md`) and "Buck2 can use services that expose Bazel's remote execution API" ([Buck2](https://buck2.build/docs/users/remote_execution); `raw/primary/2026-11-16-buck-remote.md`) |
| 25 | Cargo garbage-collects its global download cache but does not automatically clean `target/` directories. | confirmed | C/C/C | "Support for tracking build artifacts is not yet implemented, and tracked in cargo#13136." ([Cargo config reference](https://doc.rust-lang.org/cargo/reference/config.html); `raw/primary/2026-11-16-cargo-config.md`). An open PR is working on it (`raw/skeptic/2026-11-16-cargo-13136-gc-target.md`). |
| 26 | `Swatinem/rust-cache` is the most widely used GitHub Actions cache for Rust builds. | confirmed | U/C/C | GitHub code search of workflow files: "Swatinem/rust-cache total_count=164864" against "mozilla-actions/sccache-action total_count=5744" (`raw/skeptic/2026-11-16-github-code-search-rust-cache-actions.md`). Hand-rolled `actions/cache` setups are not counted. |

## Inner loop and editor

| # | Claim | Verdict | Seats | Evidence |
| --- | --- | --- | --- | --- |
| 27 | Dioxus's `subsecond` provides hot-patching of running Rust code and is usable outside Dioxus apps. | confirmed | C/C/C | "Subsecond is a hot-reloading library for Rust. It makes it easy to add Rust hot-reloading to your existing Rust project" ([README](https://github.com/DioxusLabs/dioxus/blob/main/packages/subsecond/README.md); `raw/primary/2026-11-16-subsecond.md`). It still needs a runner such as the Dioxus CLI and is called experimental (`raw/skeptic/2026-11-16-docs-rs-subsecond.md`). |
| 28 | `cargo-watch` is no longer developed and its maintainer points users to Bacon. | confirmed | C/C/C | "Cargo Watch is on life support: it will not receive further updates" and "Use [Bacon]." ([README](https://github.com/watchexec/cargo-watch); `raw/primary/2026-11-16-cargo-watch.md`) |
| 29 | `cargo-nextest` is actively maintained and reports test runs up to 3 times faster than `cargo test`. | confirmed | C/C/C | "Up to 3x as fast as cargo test" ([nexte.st](https://nexte.st/); `raw/primary/2026-11-16-nextest.md`). Latest changelog entry 2026-11-02. The figure is test execution, not test compilation. |
| 30 | By default rust-analyzer's check-on-save shares the workspace target directory and can block a concurrent `cargo build`. | confirmed | C/C/C | "More than 35% users said that they consider the IDE and Cargo blocking one another to be a big problem." ([survey results](https://blog.rust-lang.org/2025/09/10/rust-compiler-performance-survey-2025-results), 2025-09-10) |
| 31 | `cargo-wizard` applies preset profiles that configure a faster linker, Cranelift, and the parallel front end. | confirmed | C/C/C | "`fast-compile` - minimizes compilation times [...] In nightly mode, it also enables the Cranelift codegen backend and the parallel frontend" ([README](https://github.com/Kobzol/cargo-wizard); `raw/primary/2026-11-16-wizard.md`) |
| 32 | Bevy recommends dynamic linking as a workaround to speed up incremental builds. | confirmed | C/C/C | "as dynamic library, preventing it from having to be statically linked each time you rebuild your project" ([Bevy setup](https://bevy.org/learn/quick-start/getting-started/setup/); `raw/primary/2026-11-16-bevy-setup.md`) |

## AI-agent loop

| # | Claim | Verdict | Seats | Evidence |
| --- | --- | --- | --- | --- |
| 33 | No official MCP server ships with rust-analyzer or Cargo. | confirmed | U/C/C | Rests on a May 2025 maintainer statement plus absence: "I don't think it's the job of rust-analyzer to implement an interface for LLMs" ([discussion 19608](https://github.com/rust-lang/rust-analyzer/discussions/19608), 2025-05-05; `raw/skeptic/2026-11-16-rust-analyzer-discussion-19608-mcp.md`) |
| 34 | Third-party tools expose Cargo or rust-analyzer to AI coding agents over MCP. | confirmed | C/C/C | "This is a Model Context Protocol (MCP) server that provides integration with rust-analyzer" ([zeenix/rust-analyzer-mcp](https://github.com/zeenix/rust-analyzer-mcp); `raw/primary/2026-11-16-ra-mcp.md`) |
| 35 | No widely adopted tool is built specifically to speed up the Rust build loop for parallel AI coding agents. | contested | U/O/C | Turns on "widely adopted" and "specifically". The ground is occupied: kache "restores matching compiler outputs across worktrees and CI runs" (1,468 stars; `raw/manual/2026-11-16-kache-readme.md`); mbx offers "Parallel builds with a shared budget." (773 stars; `raw/skeptic/2026-11-16-mr-boxington-readme.md`); Ferry "builds each commit once, then gives every agent its own fork of that warm build" (2 stars; `raw/recency/2026-11-16-ferry-rs-librs.md`). See [AI-agent loop](topics/ai-agent-loop.md). |

## Still weak

- 22 and 33 are negatives backed by absence, not by a page that states them. A Cargo team or rust-analyzer team statement dated 2026 would settle them.
- 9 needs an independent linker benchmark on one machine, both linkers at current versions, on ext4 and tmpfs.
- 35 needs usage data (downloads or installs) for kache, mbx and Worktrunk; star counts are the only adoption signal fetched.
- Commercial build-acceleration services (Depot, WarpBuild, cargo-burst, cargo-green) were only skimmed in one search and are not covered by any claim. See `raw/manual/searches.jsonl`.

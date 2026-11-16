---
updated: 2026-11-16
sources: []
---

# Claims ledger

Claims the "build something for Rust compile times and DX" idea rests on. They were written from model recall on 2026-11-16 and are unverified until a research panel row settles them.

Verdicts: `confirmed`, `refuted`, `outdated`, `unverified`, `contested`.

## Problem

1. The most recent annual State of Rust survey lists slow compilation among the biggest problems Rust users report.
2. The Rust project's 2025 Compiler Performance Survey found that slow incremental rebuilds after a small change are the biggest compile-time complaint.
3. The 2025 Compiler Performance Survey found that slow compile times are a reason some developers stopped using Rust.

## Compiler, backends, linkers

4. On stable Rust, `rust-lld` is the default linker for `x86_64-unknown-linux-gnu`.
5. The Cranelift codegen backend is available only on nightly Rust, not stable.
6. The Rust project has a current project goal to make the Cranelift backend production-ready.
7. The Cranelift backend makes debug-build code generation roughly 20% faster than LLVM on the Rust project's benchmarks.
8. The parallel compiler front end (`-Z threads`) is nightly-only and not enabled by default on stable.
9. The Wild linker is actively maintained and benchmarks faster than mold on Linux.
10. Wild has not shipped incremental linking.
11. Wild supports only Linux, not macOS or Windows.
12. "Relink, don't rebuild" (skipping recompilation of dependents when a crate's public interface is unchanged) has not shipped in stable Rust.
13. rustc has an unstable `-Zhint-mostly-unused` option that defers code generation for dependency items that go unused.
14. rustc has an unstable option that caches proc-macro expansion across incremental builds.
15. TPDE, a compiler back-end framework from TU Munich, compiles LLVM IR about 10 to 20 times faster than LLVM at `-O0`.
16. No TPDE-based rustc backend is usable for general Rust projects today.

## Cargo, caching, build infrastructure

17. Cargo takes an exclusive lock on the build directory, so two cargo commands on the same target directory block each other.
18. The Rust project has work in progress on finer-grained build-directory locking in Cargo that is not yet stable.
19. Cargo stabilized `build.build-dir`, which separates intermediate build artifacts from final outputs.
20. Under default Cargo settings, separate git worktrees of the same project do not share compiled dependency artifacts.
21. Cargo has no stable built-in cache that shares compiled dependency artifacts across workspaces on one machine.
22. Cargo has no supported way to download prebuilt binary artifacts for crates.io library dependencies.
23. sccache cannot cache Rust crates compiled with incremental compilation enabled.
24. Bazel (rules_rust) and Buck2 support remote caching and remote execution of Rust builds, which Cargo does not do natively.
25. Cargo automatically garbage-collects its global download cache but does not automatically clean `target/` directories.
26. `Swatinem/rust-cache` is the most widely used GitHub Actions cache for Rust builds.

## Inner loop and editor

27. Dioxus's `subsecond` provides hot-patching of running Rust code and is usable outside Dioxus apps.
28. `cargo-watch` is no longer actively developed and its maintainer points users to Bacon.
29. `cargo-nextest` is actively maintained and reports test runs up to 3 times faster than `cargo test`.
30. By default rust-analyzer's check-on-save shares the workspace target directory and can block a concurrent `cargo build`.
31. `cargo-wizard` applies preset profiles that configure a faster linker, the Cranelift backend, and the parallel front end.
32. Bevy recommends dynamic linking of the engine as a workaround to speed up incremental builds.

## AI-agent loop

33. No official MCP server ships with rust-analyzer or Cargo.
34. Third-party tools exist that expose Cargo or rust-analyzer to AI coding agents over MCP.
35. No widely adopted tool is built specifically to speed up the Rust build loop for parallel AI coding agents.

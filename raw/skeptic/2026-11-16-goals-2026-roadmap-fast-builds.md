https://goals.rust-lang.org/2026/roadmap-fast-builds.html
2026-11-16

title: Fast Builds - Rust Project Goals
published_date: None
final_url: https://goals.rust-lang.org/2026/roadmap-fast-builds.html

# Fast Builds

| Metadata |
| --- |
| Short title | Fast Builds |
| What and why | Make Rust compilation fast — both from-scratch builds and incremental rebuilds during development |
| Contact | Nurzhan Saken |
| Task owners | bjorn3, Noah Lev, Jynn Nelson, Nicholas Nethercote, Vadim Petrochenkov, Matyas Susits, @wg-parallel-rustc, @ywxt |

## Summary

Minimize the time it takes to build Rust projects, whether from scratch (CI, fresh checkouts, branch switches) or incrementally during the edit-test-debug loop.

## Motivation

### The status quo

Compilation time is consistently one of the top pain points cited by Rust developers. It manifests in two distinct but related scenarios:

Clean builds — CI pipelines often take 30+ minutes for medium-sized projects, discouraging frequent commits and slowing iteration cycles. Developers switching branches or starting on a fresh checkout face similar delays that break their flow.

Incremental rebuilds — As projects grow, the time to see errors in the IDE starts to lag, going from “near instantaneous” to having a noticeable delay. This becomes worse when debugging tests, since developers must also wait for the test build to complete and execute.

The Rust compiler has made progress on compilation performance over the years, with many hotspots addressed and optimizations implemented. However, there are still architectural limitations that prevent the compiler from fully utilizing modern hardware. The frontend remains largely single-threaded despite CI machines having 16+ cores. For debug builds, we spend time in LLVM optimization passes that provide little benefit for unoptimized code. And the incremental system, while helpful, misses opportunities to skip unnecessary work.

### Design axioms

* No one thing. Particularly for batch compilation, we’re past the point of easy wins. Improving build times means doing many small improvements that add up.
* End-to-end, not just the compiler. From the user’s perspective, time spent linking or waiting for Cargo coordination is still time spent waiting. We should consider the big picture, not limit our focus to the compiler proper.
* Scenario matters. Different workflows have different bottlenecks. By focusing on particular scenarios — like incremental rebuilds during development — we can find specialized wins (like RDR) that dramatically improve that case.

### What we are shooting for

Clean builds: You switch branches or start a fresh checkout. The build completes quickly enough that you can grab coffee and come back to a ready development environment, not wait through a lunch break.

Incremental rebuilds: You are debugging a test or doing a refactoring. You edit the file. As you are editing, IDE feedback is instant. You click to rerun the test. The result is immediate.

### How we get there

| Goal | Timespan | What and why |
| --- | --- | --- |
| Add an experimental TPDE compilation option | 2026 | Significant speedup of debug builds |
| Compiler performance optimizations | 2026-2027 | Make  ``` rustc ```  faster through sustained, incremental, profile-driven optimization. |
| Improve  ``` rustc_codegen_cranelift ```  performance | 2026 | This goal aims to improve the rust development experience through faster incremental code generation with  ``` rustc_codegen_cranelift ```  . |
| Incremental Systems Rethought | 2026 | Design, propose, and implement a redesign of the incremental system to allow for shared common bases between different Rustc invocations with different arguments (i.e. |
| Polymorphic code generation experiment | 2026 | Implement experimental support in the Rust compiler for polymorphic code generation. |
| Promoting Parallel Front End | 2026 | Continue with stabilization and performance improvements to the parallel front-end, continuing from the 2025h2 goal. |
| Relink Don’t Rebuild - Land in nightly, with limitations | 2026 | Massive speedup of rebuilds in large multi-crate projects |
| Relink Don’t Rebuild - Prepare for stabilization | 2027 | Massive speedup of rebuilds in large multi-crate projects |
| Target directory size reduction | 2026 | Reduce the size of temporary compilation artifacts so developers need less disk space and the compiler spends less time on disk I/O |
| Incremental, efficient linking with Wild | 2026 and beyond | Integrate support for Wild, an innovative, Rust-based linker focused on performance and incremental link times |
| Better build parallelization | Future | Improve Cargo’s ability to coordinate parallel compilation across and within crates |
| Crate slicing | Future | Don’t compile the entire crate, just the parts you need |

Alternative backends for debug builds. The biggest opportunity for clean builds comes from using faster backends for unoptimized code. LLVM is optimized for heavyweight optimization but not ideal for debug builds where compilation speed matters more than runtime performance. Cranelift (cg\_clif) is already functional and provides speedups for debug builds. TPDE is a newer backend framework that compiles 10-20x faster than LLVM -O0 with similar code quality, showing even more promise.

Parallel rustc frontend. Currently, rustc processes each crate single-threaded even when compiling multiple crates in parallel. Enabling intra-crate parallelism lets the compiler utilize all available cores, especially important for large crates that become bottlenecks in the build graph.

Relink-Don’t-Rebuild (RDR). Most users are building a workspace with multiple crates. Changes in a root crate can force downstream rebuilds that are typically unnecessary. The goal of Relink-Don’t-Rebuild is to detect when changes are purely internal and skip the recompilation step, instead just invoking the linker.

Incremental, efficient linking with Wild. The Wild linker is an innovative new project that can help RDR be more effective by optimizing the linking step itself.

End-to-end Incremental Compilation. The current incremental system covers HIR and later phases but misses earlier work like name resolution. Extending incremental compilation to cover more phases and improving dependency tracking precision reduces unnecessary recompilation.

Shared artifacts across compilation modes. The

```
cargo check
```

command is a useful way to get compilation errors (it also powers rust-analyzer’s error reporting), but all the work that it does has to be redone when you later run

```
cargo build
```

or

```
cargo test
```

. The result is that people whose workflows include checking for errors, running lints, and running tests often wind up doing the same work over and over for each workflow.

Compiler performance optimizations. Profiling shows that compilation time is dominated by phases like trait resolution and type checking. Targeted optimizations to these bottlenecks can provide improvements across all build types without requiring architectural changes.

Better build parallelization. Better coordination between Cargo and rustc can enable more aggressive parallelization and reduce coordination overhead, especially important for large workspaces with complex dependency graphs.

Crate slicing. The Rust compiler currently builds the entirety of your dependencies before it starts on your crate, even when you yourself only need a small part of that code. Experiments suggest that compiling just the subset of dependencies that are actually used can improve build times anywhere from 1.4x to 30x, but doing this optimization well will require rearchitecting the compiler.

## Funding

| Goal | Cost | Funding contact | Sponsor(s) |
| --- | --- | --- | --- |
| 🟡 | Add an experimental TPDE compilation option | TBD | Funding team |
| 🟡 | Compiler performance optimizations | Ask | Hexcat | 🙏 Google, OpenAI, Devolutions, Fulfil |
| ✅ | Improve  ``` rustc_codegen_cranelift ```  performance | $65,000 | Tweede golf | 🙏 OpenAI, AWS |
| 🟡 | Incremental Systems Rethought | TBD | Funding team | 🙏 AWS |
| 🟥 | Polymorphic code generation experiment | TBD | Funding team |
| 🟥 | Relink Don’t Rebuild | $70,000 | Funding team |
| 🟥 | Target directory size reduction | TBD | Jynn Nelson |

## Frequently asked questions

### What about optimized/release builds?

These improvements primarily target debug builds where alternative backends provide the biggest wins. Optimized builds spend most time in LLVM optimization passes, which are harder to accelerate. However, frontend improvements and better parallelization will still provide meaningful speedups for release builds.

### Will this help rust-analyzer?

Many of these improvements will directly benefit rust-analyzer, especially frontend parallelization and smarter incremental compilation. The overall reduction in compiler work will improve IDE responsiveness.

### How much faster will builds get?

Alternative backends can provide significant improvements for debug builds, with additional gains from parallelization on multi-core machines. The exact speedup depends on the codebase characteristics and available hardware, but the goal is to make builds fast enough that they don’t interrupt development workflows.

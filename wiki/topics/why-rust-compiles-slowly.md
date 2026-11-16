---
updated: 2026-11-16
sources:
  - raw/manual/2026-11-16-kobzol-what-takes-so-long.md
  - raw/manual/2026-11-16-pingcap-compilation-model.md
  - raw/manual/2026-11-16-matklad-fast-rust-builds.md
  - raw/manual/2026-11-16-kobzol-why-not-faster.md
  - raw/manual/2026-11-16-fast-builds-roadmap.md
  - raw/primary/2026-11-16-compiler-survey.md
  - raw/manual/2026-11-16-goal-397.md
---

# Why Rust compiles slowly

There is no single cause. The time goes to three stages, and which one dominates changes with the project and with what you are doing.

## The three stages

From Jakub Beránek's breakdown ([What part of Rust compilation is the bottleneck?](https://kobzol.github.io/rust/rustc/2024/03/15/rustc-what-takes-so-long.html), 2024-03-15; `raw/manual/2026-11-16-kobzol-what-takes-so-long.md`):

- "Frontend: lexing, parsing, macro expansion, type checking, trait solving, borrow checking, MIR optimization, metadata generation, etc."
- "Backend: code generation (currently using LLVM)."
- "Linker: linking of the final artifact".

Which stage dominates, from the same post:

| Scenario | Dominant stage | Quote |
| --- | --- | --- |
| Clean debug build of a binary (ripgrep) | Backend | "most of the time is spent waiting on LLVM" although "the frontend in this case runs on a single thread, while the backend part is parallelized by up to 16 threads" |
| Incremental debug rebuild of a binary | Linker | "the linker suddenly becomes a much larger bottleneck, since it is essentially the only non-incremental part of the compilation now" |
| Incremental release rebuild | Backend | "The backend now again takes a much large ratio" |
| Library crates (about 90 measured) | Frontend | "for libraries the frontend takes a much larger fraction of the whole compilation time" |

His conclusion: "the answer to the question 'what is the bottleneck' is 'it depends'".

## Root causes

### 1. Language design chose run-time speed over compile-time speed

"One of those fundamental tradeoffs is run-time performance vs. compile-time performance, and the Rust team nearly always (if not always) chose run-time over compile-time." ([The Rust Compilation Model Calamity](https://www.pingcap.com/blog/rust-compilation-model-calamity/), Brian Anderson, 2020; `raw/manual/2026-11-16-pingcap-compilation-model.md`). The same post lists the features that cost compile time:

- **Monomorphization.** "Rust translates each generic instantiation into its own machine code, creating code bloat and increasing compile time." It also repeats across crates: "it will get compiled twice, because monomorphization happens per crate" (matklad, [Fast Rust Builds](https://matklad.github.io/2021/09/04/fast-rust-builds.html), 2021-09-04; `raw/manual/2026-11-16-matklad-fast-rust-builds.md`).
- **Macros.** They "expand to often surprising amounts of hidden code". Procedural macros must themselves be compiled first, and a derive can make a whole subtree "wait for `syn` to compile" (matklad).
- **Build scripts.** "Their unknown side-effects and unknown inputs and outputs limit assumptions tools can make about them, which e.g. limits caching opportunities."
- **Borrowing.** "Its sophisticated pointer analysis spends compile-time to make run-time safe."

These are language-level. They are out of scope to change, but how a project uses them is not.

### 2. The compiler's architecture

Also from the pingcap list:

- **LLVM.** "LLVM produces good machine code, but runs relatively slowly."
- **Too much IR.** "Rust is well-known for generating a large quantity of LLVM IR and letting LLVM optimize it away. This is exacerbated by duplication from monomorphization."
- **Code generation per crate.** "rustc generates machine code each time it compiles a crate, but it doesn't need to".
- **Single-threaded front end.** Still true on stable in 2026: "The frontend remains largely single-threaded despite CI machines having 16+ cores" ([Fast Builds roadmap](https://goals.rust-lang.org/2026/roadmap-fast-builds.html); `raw/manual/2026-11-16-fast-builds-roadmap.md`).
- **Cargo and rustc are separate.** "both cargo and rustc having imperfect and redundant information about the overall compilation pipeline".
- **The crate is the unit of compilation.** A crate compiles as a whole before anything that depends on it starts: "The Rust compiler currently builds the entirety of your dependencies before it starts on your crate, even when you yourself only need a small part of that code" (roadmap).

### 3. Rebuilds redo work that did not need redoing

This is the layer developers feel most. From the [2025 Compiler Performance Survey](https://blog.rust-lang.org/2025/09/10/rust-compiler-performance-survey-2025-results) (`raw/primary/2026-11-16-compiler-survey.md`), the three bottlenecks behind slow incremental rebuilds:

- **Workspace cascades.** "If you modify a crate in a workspace that has several dependent crates and perform a rebuild, all those dependent crates will currently have to be recompiled."
- **Linking from scratch.** "unlike the rest of the compilation process, linking is always performed 'from scratch'".
- **Gaps in incremental compilation.** "there are some parts of the compilation process that are not incremental yet or that are not cached in an optimal way. For example, expansion of derive proc macros is not currently cached".

Further redundant work:

- **Debug information.** The default dev profile "generates full debug information (debuginfo) both for workspace crates and also all dependencies", which "makes compilation and linking slower"; the survey cites "a possible improvement of 2-30% in cycle counts" from reducing it.
- **Check, build and test do not share work.** "all the work that it does has to be redone when you later run `cargo build` or `cargo test`" (roadmap).
- **Locks and duplicated target directories.** See claims 17, 20 and 30 in the [ledger](../claims.md).

## Why it has not been fixed

- "No one thing. Particularly for batch compilation, we're past the point of easy wins. Improving build times means doing many small improvements that add up." (roadmap)
- Removing one stage's cost helps less than expected. On Cranelift: "the amount of time spent in codegen for realistic changes to real code bases was smaller than expected" (`raw/manual/2026-11-16-goal-397.md`).
- Compiler performance competes with other priorities and with maintainability of a large codebase ([Why doesn't Rust care more about compiler performance?](https://kobzol.github.io/rust/rustc/2025/06/09/why-doesnt-rust-care-more-about-compiler-performance.html), 2025-06-09; `raw/manual/2026-11-16-kobzol-why-not-faster.md`).

## Which causes a tool outside the compiler can touch

| Cause | Reachable without changing rustc? | How |
| --- | --- | --- |
| Monomorphization bloat | Partly | Find the worst generic instantiations and restructure them |
| Proc macros and build scripts | Partly | Find heavy ones; avoid feature unification that pulls them in |
| Workspace cascades | Partly | Reshape the crate graph; the real fix is relink-don't-rebuild in rustc |
| Linking from scratch | Yes | Faster linker, less debug info, dynamic linking in dev |
| Debug information | Yes | Profile settings |
| Check, build, test not sharing | No | Needs the incremental redesign in rustc |
| Single-threaded front end | No, on stable | Nightly flag only |
| LLVM speed | No, on stable | Cranelift and TPDE are nightly |
| Repeated work across worktrees and CI | Yes | Caches (kache, mbx, sccache) |
| Lock contention | Yes | Separate target directories, scheduling |

The 2024 post that measured the stages also names a missing tool: "It would be cool if Cargo would be able to show you some summary of the bottlenecks that slow down the compilation of your crate(s), and guide you towards approaches that could reduce them".

Related: [Compiler, backends and linkers](compiler-backends-linkers.md), [Inner loop and editor](inner-loop-editor.md).

# Index

## Synthesis

- [Overview](wiki/overview.md): where Rust build speed and DX stand, what the panel corrected, and where the gaps appear to be.
- [Claims ledger](wiki/claims.md): 35 numbered claims with verdicts and quoted evidence (29 confirmed, 4 outdated, 2 contested).

## Topics

- [Why Rust compiles slowly](wiki/topics/why-rust-compiles-slowly.md): the three stages, the root causes in three layers, and which ones a tool outside the compiler can reach.
- [Compiler, backends and linkers](wiki/topics/compiler-backends-linkers.md): status and measured gain of each compiler-side lever, plus mold and Wild.
- [Cargo, caching and build infrastructure](wiki/topics/cargo-caching-build-infra.md): what Cargo does and lacks, caches, remote execution, commercial services.
- [Inner loop and editor](wiki/topics/inner-loop-editor.md): survey pain points, watch and test tools, hot-patching, rust-analyzer.
- [AI-agent loop](wiki/topics/ai-agent-loop.md): parallel agents in worktrees, who already serves them, what looks less crowded.
- [Failures and stalls](wiki/topics/failures-and-stalls.md): what was tried and dropped, and the patterns behind it.

## Experiments

- [Build-diagnosis kill test](experiments/build-diagnosis-kill-test/RESULTS.md): five real projects, five configurations; verdict is don't build the diagnosis tool, apply the preset.

## Raw sources

- `raw/primary/`, `raw/skeptic/`, `raw/recency/`: each panel seat's fetched pages, `searches.jsonl`, and `2026-11-16-report.md`.
- `raw/manual/`: pages re-fetched to check disputed quotes.

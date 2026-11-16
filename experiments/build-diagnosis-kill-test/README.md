# Build-diagnosis kill test

Question: is an automated "why is my Rust build slow, and fix it" tool worth building?

Written on 2026-11-16 before any measurement was taken.

## What would make the tool worth building

A generic preset already exists: `cargo-wizard`'s `fast-compile` profile turns off debug info and switches to a faster linker. A diagnosis tool only earns its place if it finds wins beyond that preset.

- **Build it** if project-specific fixes, applied on top of the preset, cut the median incremental rebuild time by 20% or more on at least 3 of the 5 projects.
- **Don't build it** if they do not. If the preset alone gives 20% or more, the lesson is "apply the preset", which needs no new tool.
- **Unclear** if the only large remaining cost is structural (rebuild cascades through the workspace) and cannot be fixed without rewriting the project's crate layout. That would point to advice, not automation.

## Projects

Latest release of each, shallow-cloned. Each uses the Rust toolchain its own repository pins.

| Project | Why | Binary package | Leaf edit | Deep edit |
| --- | --- | --- | --- | --- |
| nushell | Large CLI workspace, 46 crates | `nu` | `src/main.rs` | `crates/nu-protocol/src/lib.rs` |
| atuin | Async app stack (tokio, sqlx, axum) | `atuin` | `crates/atuin/src/main.rs` | `crates/atuin-common/src/lib.rs` |
| meilisearch | Large server | `meilisearch` | `crates/meilisearch/src/main.rs` | `crates/milli/src/lib.rs` |
| helix | Editor | `helix-term` | `helix-term/src/main.rs` | `helix-core/src/lib.rs` |
| ripgrep | Small control | `ripgrep` | `crates/core/main.rs` | `crates/matcher/src/lib.rs` |

## Measurements

For each project and configuration, on a fresh target directory:

1. One clean `cargo build` of the binary package (dev profile).
2. Three rebuilds after appending a dead private function to the leaf file. The median is the leaf rebuild time.
3. Three rebuilds after appending a dead private function to the deep file. The median is the deep rebuild time.
4. One more leaf rebuild with `-Z time-passes` to split the binary crate's time into compile and link.

Dependencies are fetched before timing. Builds run one at a time on an otherwise idle 8-core, 31 GB x86_64 Linux VM.

## Configurations

| Name | Change from the repository as shipped | Kind |
| --- | --- | --- |
| `baseline` | none | |
| `no-debug` | `profile.dev.debug=false` | preset |
| `preset` | `no-debug` plus the mold 3.0.0 linker | preset |
| `preset+macro-opt` | `preset` plus `profile.dev.build-override.opt-level=3` | project-specific candidate |
| `deps-no-debug` | debug info off for dependencies only | project-specific candidate |

Further project-specific fixes are chosen after reading the baseline timings and are listed in `RESULTS.md` with the evidence that suggested them.

## Not tested

Nightly-only options (Cranelift, parallel front end, TPDE), macOS and Windows, `cargo check`, test builds, and release builds.

## Files

- `run.py`: the harness. `python3 run.py <workdir> [project ...]`. It skips measurements already in `results.jsonl`.
- `results.jsonl`: one line per project and configuration.
- `logs/`: `-Z time-passes` output and Cargo timing reports.
- `RESULTS.md`: the verdict.

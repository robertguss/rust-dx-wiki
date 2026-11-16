# Results

Run on 2026-11-16. Raw numbers are in `results.jsonl`; every figure below is computed from it.

## Verdict: don't build the diagnosis tool

Measured against the criteria written in `README.md` before the run:

- The generic preset alone (debug info off plus the mold linker) cut leaf rebuild time by 20% or more on 4 of 5 projects. That is the "apply the preset" outcome.
- Project-specific fixes on top of the preset reached 20% on 2 of 5 projects for leaf rebuilds and 0 of 5 for deep rebuilds. The bar was 3 of 5.
- What remains after the preset is mostly rebuild cascades through the workspace, which no configuration change touched.

## Rebuild after a leaf edit (median of 3, seconds)

| Project | As shipped | Preset | Gain | Preset + optimized macros | Further gain |
| --- | --- | --- | --- | --- | --- |
| ripgrep | 0.62 | 0.46 | 26% | 0.47 | -2% |
| helix | 3.70 | 2.34 | 37% | 2.53 | -8% |
| atuin | 7.49 | 5.43 | 28% | 3.92 | 28% |
| nushell | 3.53 | 1.58 | 55% | 1.72 | -9% |
| meilisearch | 9.41 | 7.84 | 17% | 6.25 | 20% |

## Rebuild after a deep edit (median of 3, seconds)

| Project | Crates recompiled | As shipped | Preset | Gain | Preset + optimized macros | Further gain |
| --- | --- | --- | --- | --- | --- | --- |
| ripgrep | 6 | 1.07 | 0.80 | 25% | 0.88 | -10% |
| helix | 7 | 5.95 | 4.58 | 23% | 4.66 | -2% |
| atuin | 12 | 21.62 | 20.57 | 5% | 16.50 | 20% (19.8) |
| nushell | 24 | 13.38 | 10.44 | 22% | 10.44 | 0% |
| meilisearch | 6 | 17.57 | 16.57 | 6% | 13.67 | 17% |

## Clean build (one run, seconds) and disk

| Project | As shipped | Preset | Preset + optimized macros | `target/` as shipped | `target/` with preset |
| --- | --- | --- | --- | --- | --- |
| ripgrep | 8.3 | 7.0 | 8.0 | 0.5 GB | 0.3 GB |
| helix | 60.6 | 38.0 | 77.1 | 5.4 GB | 2.4 GB |
| atuin | 222.8 | 181.8 | 273.0 | 10.8 GB | 5.1 GB |
| nushell | 120.3 | 101.5 | 167.2 | 12.2 GB | 5.9 GB |
| meilisearch | 166.3 | 157.0 | 234.8 | 15.4 GB | 8.0 GB |

## What the numbers say

- **None of the five projects ships the preset.** All build with full debug info and the default linker, and all but meilisearch gain 26% to 55% on leaf rebuilds from two settings.
- **The preset roughly halves `target/`.** That bears on the disk pain of many worktrees.
- **Optimizing build scripts and proc macros (`build-override.opt-level=3`) is a real project-specific win, but a narrow one.** It helped atuin and meilisearch by about 20% to 28% and did nothing for the other three. It costs 14% to 103% on a clean build. Why those two projects benefit was not investigated.
- **Deep edits are dominated by the cascade.** In atuin, editing `atuin-common` recompiles 12 crates, and the binary crate alone takes 4 to 7 seconds of the rebuild (`logs/atuin-*-deep-timing.html`). The preset moves that by 5%.
- **Debug info off for dependencies only** keeps a debugger usable for your own code and gave 10% to 18% on leaf rebuilds for helix, atuin and nushell; it was slower on ripgrep and meilisearch.
- **Presets are not uniformly safe.** Turning debug info off made meilisearch 8% slower on leaf rebuilds, consistently across three runs. The cause was not investigated.

## Limits

- Three runs per rebuild measurement and one per clean build, on one 8-core x86_64 Linux VM. Differences under about 10% are within run-to-run spread (see the per-run times in `results.jsonl`).
- All five projects were built with Rust 1.97.1. The environment sets `RUSTUP_TOOLCHAIN`, which overrides each repository's pinned toolchain.
- The baseline linker is already `rust-lld`, the default on this target since Rust 1.90. On macOS or older toolchains the linker gain would differ.
- Only configuration changes were tested. No project was restructured, so the upside of fixing cascades by reshaping the crate graph is unmeasured.
- Nightly options (Cranelift, parallel front end, relink-don't-rebuild) were not tested.
- One kind of edit: appending an unused private function.

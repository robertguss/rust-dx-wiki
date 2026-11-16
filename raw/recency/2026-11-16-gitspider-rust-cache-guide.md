https://gitspider.com/guides/github-actions-cache-cargo-rust
2026-11-16

← All guides

# Caching cargo builds in GitHub Actions: use rust-cache, not actions/cache

Rust pays more for a missing cache than any other ecosystem: an uncached CI run re-downloads the crates.io index and recompiles every dependency from source, and "every dependency" on a real project is minutes of pure compute per run. The standard fix is one line, and it is not `actions/cache`.

## The one line: Swatinem/rust-cache

```
- uses: dtolnay/rust-toolchain@stable
- uses: Swatinem/rust-cache@v2
```

`Swatinem/rust-cache` is the de-facto cargo cache. It knows what plain `actions/cache` doesn't: cache the registry index, the downloaded crates, *and* the compiled dependencies in `target/`, keyed on `Cargo.lock` + toolchain + job, while pruning your own crate's artifacts (which change every commit and would bloat the cache to no benefit). clap runs it on effectively every job in its CI workflow: test, build, MSRV, lint, docs.

## Why not plain actions/cache?

You can hand-roll it, and the naive version backfires: cache all of `target/` with a lockfile key and the cache grows by your own incremental artifacts every run until saves start timing out, while a single dependency bump invalidates everything. rust-cache's selective pruning + stable keys is precisely the part you don't want to maintain yourself.

## The honest counterexample

serde runs its entire CI with no cargo cache at all, and that is *reasonable for serde*: a foundational crate with a tiny dependency tree, where a cold build is cheap and cache correctness across its many toolchain jobs isn't worth the surface. (Its CI is disciplined in a different way: `timeout-minutes: 45` on every job.) The lesson is the ratio, not the ritual: the deeper your dependency tree, the more a cache pays; an app with 400 transitive crates is not serde.

## Pair it with a concurrency group

Long compiles make superseded runs expensive: push twice and the stale run grinds through a full rebuild anyway unless you cancel it. Rust repos feel the concurrency guide more than anyone. See how popular Rust repos run CI →

## Common questions

**Should I use actions/cache or Swatinem/rust-cache?** rust-cache. It prunes `target/` and keys on the right inputs; a hand-rolled `actions/cache` for Rust usually caches too much (a bloated `target/` that's slower to restore than to rebuild) or misses on every lockfile change.

**Why is my Rust GitHub Actions build so slow?** Almost always a cold or missing cache. Without one, cargo recompiles every dependency from source on every run, the single most expensive thing in most Rust CI. One line of rust-cache fixes it.

**Does rust-cache cache the compiled target directory?** Yes, selectively: the registry, git dependencies, and a pruned `target/`, deliberately skipping your own crate's artifacts that change every commit and would bloat the cache to no benefit.

These hide across however many workflow files you have, which is exactly why nobody sits down and fixes them. Point GitSpider at your repo and it flags which patterns apply, with the fix for each.

No signup. Public repos only. ~30 seconds.

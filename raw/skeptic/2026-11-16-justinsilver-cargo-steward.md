https://www.justinsilver.com/technology/programming/cargo-steward/
2026-11-16

title: Cargo Steward: Rust builds, AI agents and disk space | Justin Silver
published_date: 2026-11-08T18:52:36.352Z
final_url: https://www.justinsilver.com/technology/programming/cargo-steward/

Programming

# Rust builds kept filling my disk, so I built Cargo Steward

I kept running out of disk space while doing Rust development with AI agents. More agents meant more git worktrees, and each worktree came with another set of build artifacts. I'd free some space, get back to work, and end up doing the same thing again.

I wanted that to stop being part of my day. That became Cargo Steward, a small Rust tool that started with cleaning up build output. Once I was looking at what all those builds were doing, I kept finding ways to make the workflow faster too.

## Where the space was going

Some of the growth was a Rust debug-object leak. On Rust 1.88 through 1.100, incremental rebuilds on macOS, or with

```
split-debuginfo = "unpacked"
```

, can leave old

```
*.rcgu.o
```

and

```
*.rcgu.dwo
```

files behind. The new compile writes another generation, while the old files keep taking up space. Listing a directory full of them also makes the compiler do more work before it can get started.

There was ordinary accumulation as well: old incremental sessions, dependencies copied into every worktree, and build directories left behind after the worktree itself was gone. Deleting an entire target directory gets rid of all of that, but it also throws away the dependencies I want the next build to reuse.

Cargo Steward runs as Cargo's

```
rustc-wrapper
```

. It remembers which debug objects were there before an incremental compile and removes the replaced ones after rustc succeeds. It keeps an existing wrapper, such as sccache, behind it. Cargo 1.101 addresses the object leak in its own builds; I also wanted cleanup for projects pinned to older toolchains and for everything else that accumulates around a build.

## What that looks like on disk

The cleanup log from my development machine gives a sense of the scale. On November 8, one pass reported a 25.4 GiB increase in free space on my Scratch volume. Later passes reported 17.8 GiB and 20.5 GiB. The chart shows all six logged passes from that morning, including the smaller ones.

Free-space increases reported during six cleanup passes on my machine.

These are changes in filesystem free space during each pass, rather than a sum of file sizes. That distinction matters on APFS: two cloned files can each look large while sharing the same blocks. Builds and other disk activity can also affect the free-space measurement.

Cleanup runs in the background after builds. It starts with things that cost little or nothing to rebuild, then works through idle caches, unused build units and abandoned build directories. When a disk gets low, it considers how recently a directory was used, how much unshared space it costs, and how long its builds took. I wanted it to keep the expensive builds around when it could.

## Giving a new worktree a warm start

Freeing space solved one problem, but starting each agent in a new worktree still meant compiling the same dependencies again. I added

```
cargo steward seed
```

so a worktree can start from a copy-on-write clone of a build the repository already has.

It prefers the main checkout's build when that build is available. If the main one is busy, it looks for a recent build from another worktree. A git hook can seed new worktrees when they are created, and the optional Cargo proxy can do it on their first build.

The two directories remain independent. Changing a file in one doesn't change the other. Dependencies that Cargo finds fresh can be reused; crates inside the repository normally rebuild once because creating the worktree gives their source files new timestamps. This needs a filesystem with cloning support and both build directories on the same volume, such as APFS, btrfs, reflink-enabled XFS or bcachefs.

## Getting builds out of each other's way

Several agents can each start Cargo as though they have the machine to themselves. I added a machine-wide

```
max-compiles
```

setting to limit rustc processes across builds. The Cargo proxy has a separate

```
max-builds
```

setting for limiting whole Cargo builds. Those are controls you can tune for your machine, rather than asking every agent to remember how many jobs it should use.

The proxy can also route each worktree's target directory and temporary files to a Scratch volume. On my Mac, that keeps disposable build output away from Time Machine's local snapshots and Spotlight indexing. The worktrees themselves stay on the backed-up volume.

Actual output from cargo steward shim explain on this checkout, typeset for readability. It shows Scratch routing; no whole-build limit is set in this example.

That led to a few more useful pieces: deduplicating identical build files as filesystem clones, trimming a CI cache to what its job used, and a

```
doctor
```

command that checks the wrapper chain, toolchain pins, cache settings and build-volume setup. There's also a skill for Claude Code and Codex, so agents know how to preview a cleanup and retire a worktree's build output.

## Keeping the builds I still need

A cleanup tool runs close to things I don't want it to break. Cargo Steward takes Cargo's locks before removing build output, skips directories a build is using, and protects programs still running from them. Incremental sessions are removed whole. A build directory can also be pinned when it needs to survive between runs.

The commands let me inspect the plan first.

```
cargo steward gc
```

is a preview;

```
cargo steward gc --apply
```

performs the cleanup.

```
cargo steward status --sizes
```

shows both the usual size and the unshared size, which is much more useful when builds have been cloned.

## Use it in GitHub Actions

For CI, I published Cargo Steward as a GitHub Marketplace Action. The Action trims cached build output to what the job used. With Swatinem/rust-cache, put start after the cache restore and before anything builds, then put trim at the end of the job. rust-cache saves its cache in a post step, so trimming runs before that save.

For example, this workflow installs Cargo Steward 0.1.0 if needed, runs the tests, and gives the build units trim can remove a 6 GiB budget:

```
```
name: Rust CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - uses: 0xdoublesharp/[email protected]
        with:
          mode: start
          version: 0.1.0
      - run: cargo test --locked
      - uses: 0xdoublesharp/[email protected]
        with:
          mode: trim
          budget: 6GiB
```
```

Leave trim as the final ordinary step with its normal success condition. A failed build has only used part of its cache, so forcing trim to run with always() could remove dependencies a successful job would need. Pick a budget for your project; the 6 GiB here is an example, and final outputs, documentation and busy profiles are outside that budget.

The Library guide covers workspace subdirectories, custom build directories and the options for keeping workspace crates.

## Try it

Cargo Steward is open source, MIT licensed, and available on crates.io. With Rust 1.89 or newer:

```
```
cargo install --locked cargo-steward
cargo steward setup
cargo steward skill install
cargo steward doctor
```
```

There are also prebuilt macOS and Linux binaries for Apple Silicon, Intel Macs, ARM64 Linux and x86-64 Linux. The Cargo Steward Library page has the setup guide, everyday commands and configuration examples.

It started because I was tired of making room for another Rust build. I ended up with something that also helps the next agent get to work with dependencies already built and a machine that isn't trying to run every compile at once. If that sounds like your setup, try it or open an issue.

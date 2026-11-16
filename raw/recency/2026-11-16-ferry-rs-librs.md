https://lib.rs/crates/ferry-rs
2026-11-16

### 4 releases

Uses new Rust 2024

|  |  |
| --- | --- |
| 0.1.3 | Oct 29, 2026 |
| 0.1.2 | Oct 27, 2026 |
| 0.1.1 | Oct 24, 2026 |
| 0.1.0 | Oct 24, 2026 |

#365 in Build Utils

705KB
  
17K
SLoC

# Ferry

### Blazingly fast Rust worktrees for AI agents.

Every agent starts from one warm Cargo build.  
No cold compiles, no crossed builds.

Install · Try it · How fast · How it works · Docs

## Why

Running several coding agents on one Rust repository means one git worktree
per agent, and every new worktree's first

```
cargo build
```

starts cold. Pointing
them all at one

```
CARGO_TARGET_DIR
```

instead makes builds queue on Cargo's lock,
and it is silently wrong: an agent can build, rebuild 0 crates, and run
another agent's code. Ferry's tests reproduce that with plain cargo in 60 of
60 runs (

```
tests/contamination.rs
```

).

Ferry builds each commit once, then gives every agent its own fork of that warm build.

## Install

```
```
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/patwrall/ferry/releases/latest/download/ferry-rs-installer.sh | sh
```
```

A prebuilt binary of about 1 MB for Linux (x86-64, ARM64) and macOS. Or:

```
```
brew install patwrall/tap/ferry
cargo install ferry-rs --locked
```
```

On Ubuntu 24.04 and later, run

```
ferry setup apparmor
```

once (it shows each step
and asks before its one

```
sudo
```

call).

## Try it

In any Rust repository:

```
```
ferry base                    # build one warm base for HEAD, once per commit
ferry spawn a1                # worktree + branch ferry/a1 + forked warm target, in under a second
ferry run a1 -- cargo test    # warm from the first build
```
```

Spawn as many agents as you like; each builds in its own fork. Run your agent
inside one with

```
ferry run a1 -- claude
```

, or let Claude Code create Ferry
agents for

```
--worktree
```

sessions and subagents through its hooks
(example).

```
ferry doctor
```

says what your
machine supports.

## How fast

* A new agent's first build: 0.2 to 0.5 s where a new worktree takes 71 to 92 s. That's 170× to 430× faster on rust-analyzer, polars and uv (ruff: 3.2 s against 132 s, 41×).
* Its first edit: 6× to 36× faster than in a new worktree:

| A new agent's first edit | Build units | New  ``` git worktree ``` | kache | Ferry |
| --- | --- | --- | --- | --- |
| ruff | 505 | 142 s | 40.3 s | 10.0 s | 14× |
| uv | 624 | 79.5 s | 40.6 s | 9.0 s | 8.8× |
| rust-analyzer | 281 | 74.0 s | 26.0 s | 7.7 s | 9.6× |
| polars | 212 | 71.0 s | 9.6 s | 2.0 s | 36× |
| ripgrep | 44 | 7.1 s | 2.9 s | 1.1 s | 6.3× |

* Refreshing the base after a commit: 3 to 14 s on the large workspaces, seeded from the previous base, against 71 to 163 s cold.
* Later edits aren't faster. Once an agent has built, an edit takes about as long as in any warm checkout. Ferry's gain is in starting agents.

Medians on a 6-core Ryzen 3600X with btrfs and rustc 1.99 (polars: its pinned nightly), Ferry 0.1.2 (ripgrep: an earlier build). Every scenario and step: benchmarks.

## How it works

```
ferry base
```

builds one commit's workspace once and never touches it again.

```
ferry spawn
```

gives each agent a copy-on-write clone of that target dir
(btrfs, XFS, APFS), an overlayfs layer, or a copy, and stamps the files that
are provably identical to the base so Cargo sees them as fresh. On Linux every
build runs in a private mount namespace where all agents' worktrees and target
dirs appear at the same two paths, so rustc's incremental state stays valid
and an agent's first edit compiles incrementally.
More.

## Good to know

* Linux gets the full speed-up. It needs unprivileged user namespaces, which most distributions allow. On macOS agents reuse every unchanged crate, but an edited crate recompiles from scratch.
* It is not a security sandbox. It isolates build state; agents still run as you, with your files and network.
* Local only. Ferry shares builds between agents on one machine, not across machines.
* It's young. Tell us when an agent's build differs from a cold one: issues.

All the details: platforms and limitations.

## Learn more

* Getting started: a full walkthrough
* Agent integrations: Claude Code, Codex, anything else
* Configuration and CLI reference
* FAQ: how it compares with sccache, kache and plain worktrees
* Troubleshooting
* Architecture: the invariants and how the code keeps them

## Contributing

See

```
CONTRIBUTING.md
```

. Security issues:

```
SECURITY.md
```

.

## License

MIT or Apache-2.0, at your option (

```
LICENSE-MIT
```

,

```
LICENSE-APACHE
```

). Unless you explicitly state otherwise,
any contribution you submit for inclusion is dual licensed as above, without
any additional terms or conditions.

#### Dependencies

~3.5–8.5MB
  
~185K SLoC

https://docs.rs/ferry-rs/latest/ferry/
2026-11-16

# Crate ferry

Search

Settings

Help

Source

Expand description

Ferry gives every parallel AI coding agent its own git worktree with an
instantly forked, already-warm Cargo build.

The binary (`ferry`) is the supported interface; this library exists so the
CLI and the integration tests share one implementation. Its API is not
stable.

## Re-exports§

**`pub use error::Error;`****`pub use error::Result;`**

## Modules§

**agent**:   Spawning, running, listing and removing agents.
**base**:   Building, listing and collecting immutable warm bases.
**cli**:   Command-line interface. Errors are `anyhow` here and typed below.
**config**:   `ferry.toml` schema and resolution.
**context**:   The repository, configuration and store a command operates on.
**doctor**:   `ferry doctor`: what this machine supports, what Ferry will do, and how to
    fix what is missing.
**error****fork**:   Forking a base’s target dir into an agent’s private build state.
**freshness**:   Making a fresh checkout’s unchanged files look as old as the base they
    fork from, without ever hiding a real change from Cargo.
**fsutil**:   Small filesystem helpers shared across modules.
**git**:   Git operations, by shelling out to the `git` binary.
**hook**:   Agent-tool hook handlers (`ferry hook <event>`).
**lock**:   Advisory `flock(2)` locks on files in the store.
**platform**:   Detecting what the running system can do: filesystem type, reflinks,
    unprivileged user namespaces, overlayfs inside them, and the knobs that
    restrict them (Ubuntu’s `AppArmor` userns restriction, Debian’s sysctl).
**prune**:   Pruning a seeded base’s target dir to the units its own warm build used.
**remap**:   Experimental: path-independent rustc incremental state for builds that run
    without the namespace sandbox (macOS, or Linux without user namespaces).
**sandbox**:   Running commands in an agent’s (or base’s) build context.
**setup**:   `ferry setup apparmor`: on Ubuntu 24.04 and later, installs ferry to a
    root-owned path and loads the `AppArmor` profile that lets it create user
    namespaces, through one `sudo` call the user confirms.
**shim**:   The `cargo` shim.
**store**:   On-disk layout of a repository’s Ferry store.
**toolchain**:   The Rust toolchain that will build a worktree.
**watch**:   `ferry base --watch`: builds a base whenever a revision moves.

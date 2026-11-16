https://users.rust-lang.org/t/announcements-cargo-worktree-fix-build-isolation-in-git-worktrees/139192
2026-11-16

title: Announcements cargo-worktree- fix build isolation in git worktrees
published_date: 2026-03-26T16:47:57+00:00
final_url: https://users.rust-lang.org/t/announcements-cargo-worktree-fix-build-isolation-in-git-worktrees/139192

## Problem

When developing Rust projects using Git Worktree + Agent, the default target path causes Cargo's build cache (target/ + .cargo-lock) to be globally mutually exclusive.\*\*

* e.g

  Multiple worktrees/multiple agents in the same workspace/create

  simultaneously building with Cargo\*\*

  will cause contention for:\*\*

  > ```
  > target/ directory**
  > cargo/.package-cache/registry cache
  >
  > file lock (target/.cargo-lock)
  > ```

## Solution

We encapsulated Cargo-Worktree, allowing each worktree to have its own independent target path.

https://crates.io/crates/cargo-worktree/1.0.0

## Demo

Welcome to use it!

system
Closed
2

This topic was automatically closed 90 days after the last reply. We invite you to open a new topic if you have further questions or comments.

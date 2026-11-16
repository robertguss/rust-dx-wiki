https://github.com/rust-lang/cargo/issues/17508
2026-11-16

# `-Zfine-grain-locking`: concurrent builds deadlock when both compile the same units #17508

New issue

New issue

Open

## Description

benedikt-bartscher

opened on Sep 24, 2026

### Problem

Two concurrent `cargo check`s of the same workspace with `-Zfine-grain-locking` often deadlock from a clean state. Both processes stop using CPU, and each waits on a build unit lock the other holds. We first hit it with two cross builds that used separate `--target-dir`s and one shared `build.build-dir`.

### Steps

```
#!/usr/bin/env bash
set -u
dir=$(mktemp -d) && cd "$dir"
printf '[workspace]\nmembers = ["app", "dep*"]\nresolver = "3"\n' > Cargo.toml
for i in $(seq 1 16); do
  mkdir -p dep$i/src
  printf '[package]\nname = "dep%s"\nversion = "0.1.0"\nedition = "2024"\n' $i > dep$i/Cargo.toml
  for k in $(seq 1 400); do echo "pub fn f$k(x: u64) -> u64 { (0..$((k % 40 + 1))).fold(x, |a, b| a.wrapping_mul(31).rotate_left(b) ^ $k) }"; done > dep$i/src/lib.rs
done
mkdir -p app/src
{ printf '[package]\nname = "app"\nversion = "0.1.0"\nedition = "2024"\n\n[dependencies]\n'
  for i in $(seq 1 16); do echo "dep$i = { path = \"../dep$i\" }"; done; } > app/Cargo.toml
echo 'fn main() { println!("{}", dep1::f1(1) ^ dep8::f1(8)); }' > app/src/main.rs

for attempt in $(seq 1 8); do
  rm -rf target
  timeout 60 cargo +nightly -Zfine-grain-locking check -p app >/dev/null 2>&1 & a=$!
  timeout 60 cargo +nightly -Zfine-grain-locking check -p app >/dev/null 2>&1 & b=$!
  wait $a; ra=$?; wait $b; rb=$?
  echo "attempt $attempt: exit $ra / $rb"  # 124 = hung until the timeout
done
```

7 of 8 attempts hang here. Without `-Zfine-grain-locking`, none do.

`/proc/locks` during a hang, from a run with 8 dependency crates:

```
debug/build/dep1/6634f7d28328c938/.lock: held shared by B, exclusive wanted by A
debug/build/dep2/0df4cbf1d5349301/.lock: held shared by A, exclusive wanted by B
debug/build/dep3/70818309f13b4c2a/.lock: held shared by A, exclusive wanted by B
debug/build/dep4/403e3d501cf46364/.lock: held shared by B, exclusive wanted by A
...
```

### Cause

Both processes find all units dirty. `compile` wraps each dirty job in a blocking exclusive lock, then downgrades to a shared lock that it keeps for the rest of the build. A builds `dep2` while B builds `dep1`. Each then keeps a shared lock on its own unit and waits for an exclusive lock on the other's.

The failures in #16657's Windows CI may have been this. The known issue in #4282 about a shared dirty unit blocking is a permanent deadlock once there are two such units.

### Version

```
cargo 1.100.0-nightly (98a09e7e7 2026-09-21)
Linux x86_64
```

## Activity

1. ### ranger-ross commented on Sep 24, 2026

   ranger-ross

   on Sep 24, 2026

   Member

   Thanks for reporting, and yeah the fine grain locking design is currently not sound.

   I have stepped back from that work to focus on the build-dir layout stabilization (which is required for fine grain locking) and work towards cross workspace caching.  
   I'd like to come back and properly re-design the fine grain locking support once those are further along. (also some of the assumptions about the locking design may be invalidated by the rustc incremental redesign which another reason I've punted on this project)

   Reacted by benedikt-bartscher
2. maan2003

   added a commit that references this issue on Nov 8, 2026

Sign up for free **to join this conversation on GitHub.** Already have an account? Sign in to comment

## Metadata

## Metadata

### Assignees

No one assigned

### Labels

No labels

No labels

### Type

No type

### Projects

No projects

### Milestone

No milestone

### Relationships

None yet

### Development

No branches or pull requests

## Issue actions

https://tamedtornado.com/guides/rust-builds-ai-coding-agents
2026-11-16

title: How to Speed Up Rust Builds for AI Coding Agents — Tamed Tornado
published_date: 2026-08-04
final_url: https://tamedtornado.com/guides/rust-builds-ai-coding-agents

Suppose you start five coding agents on the same Rust project.

Each agent gets its own Git worktree. That is good: the agents cannot overwrite one another's files. Each agent then runs the normal checks:

```
```
cargo check --all-targets
cargo clippy --all-targets -- -D warnings
cargo test
```
```

That is also good. An agent should not claim that its work is finished without running the real project checks.

Then the host falls over.

All five worktrees are clean, so Cargo starts compiling the same dependencies five times. A large link begins in several worktrees at once. CPU use jumps, memory disappears, and agents spend more time waiting for builds than editing code.

This is the problem that led to

```
cargo-reapi
```

.

## The first attempt: limit Cargo jobs

The obvious first step is to reduce Cargo's job count:

```
```
cargo build -j 1
```
```

This limits one Cargo process. It does not limit the machine.

If five agents each run Cargo with one build job, the host can still run five expensive compiler or linker processes at once. You have made each build slower without stopping the duplicate work.

Serializing the agents fixes the resource problem, but defeats the reason for running several agents. We wanted five agents to keep working while the machine compiled each unique Rust action only once.

## The second attempt: share the target directory

The next idea is to point every worktree at the same

```
target/
```

directory.

This can look effective in a quick test. One worktree compiles a dependency, and another worktree finds the artifact. But

```
target/
```

is not a read-only cache. Cargo writes fingerprints, build-script output, incremental state, locks, binaries, and other working files there.

Now five independent jobs are changing the same directory. Cleanup in one job can affect another. Cancelled jobs leave shared state behind. It becomes harder to tell which branch produced a file.

The safer setup is:

* one target directory per worktree;
* one shared cache for reusable build output.

The worktrees stay isolated. The expensive work does not have to be repeated.

The difference is covered in more detail in Should Multiple Rust Worktrees Share a Cargo Target Directory?.

## Put the cache underneath Cargo

cargo-reapi does not replace Cargo. It runs Cargo and watches the compiler commands Cargo starts.

Install it, choose a cache directory that every build can reach, and run an ordinary Cargo command through it:

```
```
cargo install cargo-reapi --locked

cargo reapi \
  --backend cache \
  --cache-dir /shared/cargo-reapi-cache \
  -- check --all-targets
```
```

Cargo still decides which crates need to build. Cargo still handles features, profiles, build scripts, and proc macros. cargo-reapi decides whether a compiler action has already been completed with the same inputs.

If it has, the output is restored into the current worktree's target directory. If it has not, the compiler runs and the result is saved for the next worktree.

## What happens when an agent starts

There are three useful cases.

### Case 1: the agent has not changed anything yet

An agent usually begins from the same commit as the other agents. It may run the full quality gate before editing.

If another worktree has already completed that exact gate, cargo-reapi can restore the complete target state. Cargo does not need to start.

Think of this as a saved result for one exact command on one exact project state. It is not a random copy of somebody else's

```
target/
```

directory. The cache entry is tied to the source, Cargo options, toolchain, platform, and other inputs that can change the result.

### Case 2: the agent changes one crate

Once the agent edits a file, the exact saved gate no longer matches. Cargo runs and plans the build as usual.

That does not mean a full rebuild. cargo-reapi can still restore the compiler actions that did not change. The edited crate and the crates that depend on it rebuild. Unrelated crates come from the shared cache.

This is important. A cache that works only when the entire repository is unchanged is not very useful for active development.

### Case 3: several agents miss the same action together

Imagine five fresh builds reaching

```
bevy_pbr
```

at the same time.

Without coordination, all five run the same compiler command. cargo-reapi lets one process do the work. The other four wait for that result and then restore it.

We observed exactly this during production use: one compiler process ran and four callers reused its output. All five Cargo jobs continued successfully.

This also helps on the first cold run. The cache does not have to be warm before it reduces duplicate work.

## Stop builds from exhausting the host

Removing duplicate work solves only part of the problem. Different agents can still compile different crates at the same time.

cargo-reapi therefore has one shared resource limit for real compiler and linker work. You configure how much CPU and memory the host may spend. Cache hits do not consume that allowance. Five identical misses count as one piece of work because only one compiler runs.

The Cargo jobs themselves remain concurrent. We are limiting expensive work, not forcing whole quality gates into a single-file queue.

That distinction matters when ten agents are active. Most of them may be reading cached output while only a few are actually compiling.

## What this looked like on Moria

We tested the system on Moria, a real Rust and Bevy project. Each clean worktree ran formatting, checks, Clippy, and tests.

On the production Linux host, one cold quality gate took about 52 minutes. After the cache was populated, five clean worktrees ran the full gate together in about 25 seconds.

| Run | Time | Peak build memory |
| --- | --- | --- |
| One cold gate | 3,125.608s | 6.37 GB |
| Five warm gates together | 24.695s | 879 MB |

An operating-system observer saw no compiler or linker processes during the five warm gates. This was not just Cargo saying that everything was fresh.

The public test suite also changes source files, compiler flags, features, build inputs, and cached data on purpose. A fast cache that returns the wrong binary is worse than no cache.

## Production use found real bugs

The first agent runs did not produce a perfect hit rate. They found several mistakes in the integration.

The agent platform was passing its own scheduling variables into Cargo. Build scripts can read environment variables, so cargo-reapi treated different values as different builds. The fix was to stop leaking private scheduler settings into the project process.

In another case, the target directory was mounted at one path inside a container while the cache settings referred to a host path. cargo-reapi refused to cache those actions because the paths did not agree.

A Bevy dependency also tried to run

```
c++
```

through Debian's

```
/etc/alternatives
```

. The strict build sandbox could not see that path, so the build failed. We added the required read-only path and a test that compiles and links real C++ code from

```
build.rs
```

.

These failures were inconvenient, but safe. They caused a miss or a visible error. They did not return stale build output.

## A simple rollout

Do not switch every agent at once.

Start with one project and one host:

1. Give every worktree its own target directory.
2. Put the cargo-reapi cache on fast storage shared by those worktrees.
3. Run

   ```
   cargo reapi doctor
   ```

   before admitting the host.
4. Run the normal quality gate through the cache backend.
5. Inspect the JSON action log to see hits, misses, and actions that could not be cached.
6. Start two clean worktrees together and confirm that identical misses run once.
7. Increase the agent count only after memory and disk use are understood.

The repository includes cache statistics and garbage-collection commands for long-running hosts.

## Where it fits today

The tested path is a shared local cache on macOS with APFS and Linux with XFS. It is a good fit when several worktrees or containers build on the same compatible host.

cargo-reapi also contains an adapter for the standard Remote Execution API, but that adapter has not yet been validated against a live production REAPI service. Windows and many less common native build setups are also outside the tested range.

For CI rather than agents, read Rust Build Caching for Parallel CI. For a general worktree setup, read How to Share Rust Build Work Across Git Worktrees.

The source, test suite, benchmarks, and full Moria case study are in the cargo-reapi repository.

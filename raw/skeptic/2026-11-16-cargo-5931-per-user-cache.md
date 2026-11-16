https://github.com/rust-lang/cargo/issues/5931
2026-11-16

fetched_with: gh api repos/rust-lang/cargo/issues/5931 --jq '"title: \(.title)\nstate: \(.state)\ncreated: \(.created_at)\nupdated: \(.updated_at)\nlabels: \([.labels[].name]|join(", "))\n\n\(.body)"'; echo; echo '--- last comments ---'; gh api 'repos/rust-lang/cargo/issues/5931/comments?per_page=100' --jq '.[-8:][] | "[\(.created_at) \(.user.login)] \(.body)\n"'

title: Per-user compiled artifact cache
state: open
created: 2018-08-23T14:30:36Z
updated: 2026-10-06T06:15:00Z
labels: A-caching, S-needs-design

*[View all comments](https://triagebot.infra.rust-lang.org/gh-comments/rust-lang/cargo/issues/5931)*

MVP design: cache intermediate artifacts across projects with minimal cache poisoning
- Only immutable items (registry, git, not path)
- Idempotent builds (no build script executions + dependents, no proc macro dependents)

Roadmap:
- [x] Split out a `build-dir` to communicate out early what will be broken (#14125)
- [x] Re-organize `build-dir` into cacheable units (#15010)
- [ ] Experiments
  - [ ] More granular locking in `build-dir` to see what could apply to a shared cache (#4282)
  - [ ] GC for `build-dir` in prep for GC for shared cache (#5026)
  - [ ] Implement shared cache without gc and with coarse locking
- [ ] Polish shared cache
  - [ ] GC
  - [ ] granular locking

Parallel efforts to improve cache efficiency
- #14948
- #14903
- rust-lang/rust#143549
- rust-lang/rust#143547

Future possibilities
- Remote cache plugin system
- Means for proc-macros and build scripts to be cached
  - Pinky promise flag to be cacheable
  - Means for guarenteeing they are only accessing declared resources

Open questions
- How does this interact with `cargo clean`?
- How does this interact with pipelined builds?

---

I was wondering if anyone has contemplated somehow sharing compiled crates. If I have a number of projects on disk that often have similar dependencies, I'm spending a lot of time recompiling the same packages. (Even correcting for features, compiler flags and compilation profiles.) Would it make sense to store symlinks in `~/.cargo` or equivalent pointing to compiled artefacts?

--- last comments ---
[2026-09-02T14:48:29Z ssokolow] > `relatime` and `lazytime` exist on Linux. Windows can delay atime updates for up to one hour, like `lazytime`. MacOS seems to default to something like `relatime` (see `strictatime` in the mount options).

Like nazar-pc, I also run my drives with `noatime`. Currently, it's common wisdom that the only thing which will break is optional functions of local mail clients like `mutt`, so I'd recommend not depending on it.

(To be honest, if Cargo's caching started depending on it, I'd probably start looking for a way to hack around that rather than turning any form of atime updating back on... maybe pin an old Cargo until the AI bubble pops and RAM prices come down enough, install a few more gigs, and then put my `target` dirs on a RAM drive.)

[2026-09-02T14:52:46Z nazar-pc] As I mentioned earlier, you can update access time of a file explicitly even on filesystem mounted with `noatime` if it is really necessary. So no need to search for alternatives, just something to keep in mind and be deliberate with.

[2026-09-07T16:58:02Z ranger-ross] I did some [experimenting](https://github.com/ranger-ross/cargo/pull/32) with using content addressable store to back the build cache. I got it working and results were mixed. On the benchmarks I ran, we only saved 0.5GB out of 30GB.
This is kind of expected as the build-cache is being to quiet conservative to start with.


I had a discussion @epage and he had the idea to extend CAS storage to include files in the `build-dir` as well.
The idea is that we would could always deduplicate artifact files even if we cannot safely cache them at a build unit level. 
This CAS cache would not benefit build times since we would not be able to check it for build units before building.

The thought process is that we could build the CAS storage and start getting disk space reduction benefits for most files in `build-dir` while keeping the scope small enough that we'd be able to stabilize it in a reasonable period of time.
Then we could build the build cache on top of the CAS storage.

This would probably benefit the git worktree workflows that are becoming increasing popular quiet a bit.

[2026-09-10T16:59:09Z ranger-ross] I did some more experimenting on the CAS design. 
I rewrote [my prototype](https://github.com/ranger-ross/cargo/pull/33) from scratch making some strategic design changes after learning from the first prototype. (notably we do not to to read directly from the cache, instead I hardlink into `build-dir` accepting that it makes cache GC more complicated but greatly simplifies the build process)
Also I handwrote this prototype compared to previous ones, and thus it only clocks in at ~225 lines changed, which is much smaller than previous attempts.

What the build units the cache considers safe to share is very conservative ([logic](https://github.com/ranger-ross/cargo/pull/33/changes#diff-5ff136e7febc28afc808732c6475f3211d3cf56da996fd3e9e23e07ce8508c0fR321-R348)), so I was not expecting to see huge wins.

I did 2 benchmarks on this:

## Benchmark 1: The gauntlet 
 
I cloned ~20 OSS rust projects and ran `cargo build` on them and compared the disk usage and wallclock time

<details><summary>List</summary>

* alacritty
* atuin
* bat
* bottom
* delta
* dust
* eza
* fd
* helix
* hyperfine
* just
* nextest
* ripgrep
* starship
* tauri
* tokei
* typst
* zellij
* zoxide

</details> 

Results:

- cargo 1.98.0
    - target 31G
    - build-cache 0 (does not exist on stable)
    - 12m 59s for all builds
- With CAS cache -- clean build
    - build-cache+target 31G
    - build-cache 2.9G
    - 12m 18s for all builds
- With CAS cache -- warm build (warm build-cache, clean `target` dir)
    - 11m 30s
- cache stats (after the bench was done)
    - 486 crates, 1,394 cache entries
    - distribution: (entries per crate, can have multiple entries if version, RUSTFLAGS, etc are different)
        - 1: 247 (247 crates only had 1 cache entry)
        - 2: 84
        - 3: 40
        - 4: 17
        - 5: 26
        - …
        - 19: 2 (log, bitflags)
        - 22: 1 (hashbrown)

## Benchmark 2: Git worktrees workflow

I wanted to all test the git worktree flow, by using a single project but having 5 copies (git worktrees) of it with their own `target` dirs but shared build-cache. My benchmark I used Alacrity, as it was a medium sized project.
I built the worktrees one at a time and measured disk usage and wall clock.

Results: 

- cargo 1.98.0 (797e8a9bc 2026-08-05)
    - 2m 53s — avg 35s
    - 5.8GB across all targets dirs
- CAS cache (clean cache on first build.)
    - 2m 38s — avg 31s
    - build-cache 238MB
    - build-cache+all target dirs 4.9GB

---

So to recap, for general sharing of dependencies across multiple projects, I believe there are 2 issues:
1. The cache build unit eligibility is too strict (knew that going in, can be improved over time)
2. It appears that there are quiet a lot of misses due to crate versions not being aligned or other build configuration. I didn't look to deeply, but this is not terribly surprising. Unsure if there is much we can do about this since its just how the crates ecosystem is.
  * It might be worth considering automatically disabling the build-cache if a workspace is setting `RUSTFLAGS` (or other) and require them to explictly opt-in this workspace to avoid bloating the cache with entries that will never be used by other workspaces. (granted, if we go with #17453 then we might as well add the entry because the files we be stored in the cache regardless)




[2026-09-10T18:10:14Z epage] Is the CAS only used for build reuse or did you expand the rules for it for de-duplication?

Have you tried a run without the restricted rules for build reuse to see the potential with improved build scripts and proc macros?

[2026-09-11T01:31:44Z ranger-ross] The above benchmarks are only with build unit caching, no build-dir deduplication. 

I haven't tested with more aggressive caching yet either. 

I want to try doing both of these later this week or next. 
I am optimistic we can greatly reduce disk space if implemented correctly

[2026-09-11T15:49:31Z ranger-ross] Ran a couple of more experiments:

Rerunning the same "gauntlet" benchmark above

- With CAS and caching enabled for all non-local crates w/ Clean cache
    - build-cache+targets 31G
    - build-cache 11G
    - 6m 46s for all builds
- With CAS and caching enabled for all non-local crates w/ Warm cache (clean target dirs)
    - 3m 27s

So this is a pretty nice result I'd say. With a clean cache, we cut the time to run the gauntlet nearly in half since the cache fills up and progressively gets more hits towards the end.

Also reran my worktree scenario benchmark:

- With CAS and caching enabled for all non-local crates w/ clean cache
    - 42s
    - build-cache 596MB
    - build-cache+all target dirs 3.5GB

(Note: I noticed that the repo (Alacritty) I was using seems to not have deterministc output of its binary, so the final binary was being duplicated and was ~155MB)

For the `build-dir` deduplication I am still trying to impl a PoC to test that. 



[2026-10-06T06:14:59Z ranger-ross] Late follow up here, but I've continued to go down the content addressible storage route.
I've been focusing on implementing #17453 as a first step, but after a few attempts in #17512 I decided to take a step back instead of designing each piece in isolation. 

I spent some time putting together a [design document](https://hackmd.io/9GQ0pYr_TSONt7fqQTJs3w) with a proposed design. 
Feedback on it is welcome. There is also a Zulip thread with discussion about the design [#t-cargo > Cargo remote cache / deduplication design @ 💬](https://rust-lang.zulipchat.com/#narrow/channel/246057-t-cargo/topic/Cargo.20remote.20cache.20.2F.20deduplication.20design/near/629227898)




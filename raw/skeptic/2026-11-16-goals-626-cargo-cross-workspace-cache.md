https://github.com/rust-lang/goals/issues/626
2026-11-16

fetched_with: gh api repos/rust-lang/goals/issues/626 --jq '"title: \(.title)\nstate: \(.state)\ncreated: \(.created_at)\nupdated: \(.updated_at)\nlabels: \([.labels[].name]|join(", "))\n\n\(.body)"'; echo; echo '--- last comments ---'; gh api 'repos/rust-lang/goals/issues/626/comments?per_page=100' --jq '.[-8:][] | "[\(.created_at) \(.user.login)] \(.body)\n"'

title: Cargo cross workspace cache
state: open
created: 2026-05-05T13:29:34Z
updated: 2026-11-14T15:56:13Z
labels: T-cargo, C-tracking-issue


| Metadata         | |
| --------         | --- |
| Contact          | @ranger-ross |
| Team(s)          | [cargo](https://github.com/rust-lang/cargo) (@epage) |
| Goal document    | [2026/cargo-cross-workspace-cache](https://goals.rust-lang.org/2026/cargo-cross-workspace-cache.html) |
| Funding contact  | [Jess Izen](https://book.jessizen.com) |

## Summary

Work towards a build cache that is shared across workspaces to build times and reduce disk usage.

---

This issue is intended for status updates only.

For general questions or comments, please contact a goal owner or post in the [Zulip topic](https://rust-lang.zulipchat.com/#narrow/channel/435869-goals/topic/Cargo.20cross.20workspace.20cache.20.28goals.23626.29).


--- last comments ---
[2026-05-05T13:41:09Z tomassedovic] This issue is intended for status updates only.

For general questions or comments, please contact the owner(s) directly.

[2026-05-28T12:31:47Z ranger-ross] ## Update May 28, 2026

The last week for me was spent at Rust Week and the all hands. 
There was a lot of good discussion about the possibilities for how the cache may work and usecases.

We are continuing the effort to stabilize the new `build-dir` layout in Cargo as that is a requirement for the cross workspace cache.
The stabilization PR (https://github.com/rust-lang/cargo/pull/16807) has been posted and FCPed, and it is just waiting on the rust-lang/rust PR (https://github.com/rust-lang/rust/pull/155439) to be merged to add support for the new layout to the compiler. I've been working through the issues and I believe we are quiet close to merging, just need to fix the remaining CI failures.


[2026-07-28T12:57:18Z ranger-ross] ## Update July 28, 2026

The new `build-dir` layout stabilization was merged in https://github.com/rust-lang/cargo/pull/16807 but later rolled back in https://github.com/rust-lang/cargo/pull/17187 due to build failures discovered in some projects on nightly.

The build failure stemmed from increased arguments (primary `-L`) being passed to rustc from Cargo hitting OS limits. Also a similar failure mode where the dylib search path (`LD_LIBRARY_PATH` on Linux and `PATH` on Windows) would get too long and hit OS limits.
We then merged a series of fixes https://github.com/rust-lang/cargo/pull/17191, https://github.com/rust-lang/cargo/pull/17236, https://github.com/rust-lang/cargo/pull/17168 to reduce the paths being passes to rustc and added to the search.

In addition to the fixes in Cargo, we also added arg file support to sccache in https://github.com/mozilla/sccache/pull/2782 which is a work around for OS command length limits that is already supported in Cargo+rustc.
With the increase in likelihood of a project getting large enough to need an arg file this was a preemptive optimize to minimize breakage on stabilization.  

With the fixes above, we are feeling better about the new layout and plan to enable it by default on nightly. (https://github.com/rust-lang/cargo/pull/17258)
Instead of stabilizing the new layout immediately, we are opting to enable it on nightly by default to gather feedback and find the places we can improve before committing to stabilization.

If all goes well, you should see the new build-dir layout on nightly in the near future


[2026-09-04T09:57:52Z ranger-ross] ## Update Sept 4, 2026

The new `build-dir` layout was restabilized in https://github.com/rust-lang/cargo/pull/17354 and is expected to release in 1.100.0.
There were also some more optimizations made to reduce the amount of args passed to rustc when the new layout is enabled (https://github.com/rust-lang/cargo/pull/17410) 
At this point, the `build-dir` layout has been enabled on nightly for a few weeks and there hasn't been any new issues reported so I have claimed victory on this!

With the layout stablized, I've shifted my attention back to actually implementing the cache. Until the old layout code is removed (which we will do like 1 release after the new layout lands) I have been working on prototyping the cache design. I have a few MVP implementation and design discussions are happening in https://github.com/rust-lang/cargo/issues/5931.

I expect this prototyping loop to continue for another month while we iterate on cache design.
My goal is to get something into nightly in October. :) 

[2026-09-21T11:52:08Z ranger-ross] ## Update Sept 21, 2026

I have continue experimenting with different cache design over the last 2 weeks.
Most of the discussion has happened in https://github.com/rust-lang/cargo/issues/5931

Currently the design that seems most promising to me is having a shared content addressable storage (CAS) location for the cache, with a cache "entry" that has "pointers" into that  CAS storage. (see https://github.com/rust-lang/cargo/issues/5931#issuecomment-5498506395)

I built a prototype and ran some benchmarks that do show some promising results (https://github.com/rust-lang/cargo/issues/5931#issuecomment-5622385527, https://github.com/rust-lang/cargo/issues/5931#issuecomment-5637021096)

During this discussion, the idea of using the CAS for deduplication of artifacts between multiple workspace `build-dir` directories.
Built units output artifacts would be able to be deduplicated regardless of if we can safely cache the build unit. (e.g. its a non-deterministic build script)
Currently, we are considering pursuing this as a step stone towards the build cache.
It's notable to point out that the deduplication across multiple Git worktree's of the same workspace (which has become popular in AI workflows) gets a large reduction in disk space from my testing.
CAS deduplication feature is being tracked in https://github.com/rust-lang/cargo/issues/17453

Over the month, I'll continue building on the existing prototypes and refining the design.
I am still hopeful to get _something_ on nightly in October.


[2026-10-01T15:49:22Z ranger-ross] ## Update Oct 1, 2026

Over the last 2 weeks, I've continued to experiment with CAS deduplication. (going forward's I'll refer to it as blob storage)
Implementing the blob storage and deduplication itself is not that difficult.
The tricky part is adding garbage collection in a cross platform + performant way.

Shared blob storage is going to fill up and is unaffected by `cargo clean`, it actually makes `cargo clean` much less effective on it's own since deleting a file from `target` does not actually recoever the disk space.
This makes having garbage collection for blob storage really important for being able to land this feature.

Initially, I tried leveraging the existing Cargo garbage collection infrastructure which uses sqlite.
I had performance concerns about sqlite on large workspaces, but to my surprise it was not too bad.
But the cost of hashing all of the outputs so that we can make blobs as used was huge and not feasible.

Another approach I tried was using a `<original-file-name>.timestamp` file that is hardlinked into each workspace, that serves as a "pointer" that can be updated by setting it's `mtime`. This approach does not require hashing files which helps performance quiet a bit, but there are concerns that this not going to work well (or at all) for extending blob storage to work remotely.

I am currently exploring other approaches for how we can make blob storage garbage collection work.
If you are interested in helping with the design please get in contact with me!

The discussion about the blob storage GC implementation is primarily happening in https://github.com/rust-lang/cargo/pull/17512 


[2026-10-14T07:08:45Z ranger-ross] ## Update Oct 14, 2026

Over the last 2 weeks, I've continued to iterate on the blob storage and cache design.
Last week, I decided to take a step back from the blob storage PR and created a [design document](https://hackmd.io/9GQ0pYr_TSONt7fqQTJs3w?view) for the larger feature instead of trying to design pieces in isolation.
This document is a living document and is actively being updated as the design changes.
As questions have been answered, more questions have been opened and I am still working through them.

I feel I've made some meaningful progress exploring the design space and I am getting closer to a cache design that could be feasible in accomplishing our goals.

One of the many things to solve is how we handle (reduce/remove) absolute paths from the rustc output so that things are more cachable.
https://github.com/rust-lang/cargo/pull/17573 was a first step, but there still a lot of work to be done here.

Design discussions are happening in [#t-cargo > Cargo remote cache / deduplication design](https://rust-lang.zulipchat.com/#narrow/channel/246057-t-cargo/topic/Cargo.20remote.20cache.20.2F.20deduplication.20design/with/629227898)

(Feedback is welcome! Hackmd comments, in the Zulip thread, or on the github issue https://github.com/rust-lang/cargo/issues/5931)

[2026-11-14T15:56:13Z ranger-ross] ## Update Nov 15, 2026

Over the last month, I've continued to work towards getting cross workspace deduplication into nightly.
I've been working through some of the smaller issues, notably:

### Cache poisoning 

Cargo makes use of hardlinking to reduce disk space and improve performance by avoiding large file copies.
For blob storage, we plan to use reflinks (copy on write) when the filesystem support them.
However, from the research I have done, reflinks platform support is unfortunately quiet bad making it really hard to require them.

We decided that using hardlinks and the risk of cache poisoning is worth it if we can support more platforms.
However we want to mitigate this as much as possible. 

https://github.com/rust-lang/cargo/pull/17675 changes Cargo to remove the entire build unit's output directory before building to mitigate this risk.
We feel this is reasonable mitigation and we can experiment with more integrity checking while on nightly.

### Handling mtime sharing across workspaces

As mentioned above we will continue to use hardlinks into a shared storage directory. 
This means that file metadata is shared including `mtime`s (which Cargo uses for rebuild detection) across all workspaces using the deduplicated file.
This makes it possible to get into scenarios where a file is deduplicated with an older mtime causing a permanent rebuild state.

To avoid this, we decided to change Cargo's logic to use a dedicated timestamp file that is not shared across workspaces and no longer rely on the mtime's of output artifacts directly.

See: https://github.com/rust-lang/cargo/pull/17718 and https://github.com/rust-lang/cargo/pull/17732

## Implementing deduplication

While working on the issues above, I was also updating the [cross workspace deduplication PR](https://github.com/rust-lang/cargo/pull/17573) to align with the direction in the [design doc](https://hackmd.io/9GQ0pYr_TSONt7fqQTJs3w).
I rewrote this PR nearly from the ground up and it is now functional and getting close to being reviewable.
I need to add a few more unit tests and do some more benchmarking. 
I am hoping to get this PR into the review pipeline later this week and on to nightly later this month.



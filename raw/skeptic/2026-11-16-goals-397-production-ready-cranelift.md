https://github.com/rust-lang/goals/issues/397
2026-11-16

fetched_with: gh api repos/rust-lang/goals/issues/397 --jq '"title: \(.title)\nstate: \(.state)\ncreated: \(.created_at)\nupdated: \(.updated_at)\nlabels: \([.labels[].name]|join(", "))\n\n\(.body)"'; echo; echo '--- last comments ---'; gh api 'repos/rust-lang/goals/issues/397/comments?per_page=100' --jq '.[-8:][] | "[\(.created_at) \(.user.login)] \(.body)\n"'

title: Production-ready cranelift backend
state: closed
created: 2025-09-16T18:42:50Z
updated: 2026-05-11T10:16:03Z
labels: T-compiler, C-tracking-issue, Flagship Goal, T-wg-compiler-performance, ex-2025h2


| Metadata         | |
| --------         | --- |
| Point of contact | @folkertdev |
| Team(s)          | [compiler](http://github.com/rust-lang/compiler-team), [wg-compiler-performance](https://github.com/rust-lang/rustc-perf) |
| Goal document    | [2025h2/production-ready-cranelift](https://rust-lang.github.io/rust-project-goals/2025h2/production-ready-cranelift.html) |

## Summary

This project aims to get the rust cranelift codegen backend to a production-ready state. Specifically, with this work completed, we'd be confident to recommend it as the default for local development, e.g. with `cargo test` or `cargo run`.

## Tasks and status

* [ ] Acquire funding ()
* [ ] Standard reviews ([compiler](http://github.com/rust-lang/compiler-team) ![Team][])
* [ ] Dedicated reviewer ([compiler](http://github.com/rust-lang/compiler-team) ![Team][])
* [ ] Deploy to production ([wg-compiler-performance](https://github.com/rust-lang/rustc-perf) ![Team][])
* [ ] Do the work (@bjorn3, @folkertdev)

[Team]: https://img.shields.io/badge/Team%20ask-red


--- last comments ---
[2025-09-16T18:44:05Z nikomatsakis] This issue is intended for status updates only.

For general questions or comments, please contact the owner(s) directly.

[2025-12-01T16:43:03Z folkertdev] We did not receive the funding we needed to work on this goal, so no progress has been made.

Overall I think the improvements we felt comfortable promising are on the low side. Overall the amount of time spent in codegen for realistic changes to real code bases was smaller than expected, meaning that the improvements that cranelift can deliver for the end-user experience are smaller. 

We still believe larger gains can be made with more effort, but did not feel confident in promising hard numbers.

So for now, let's close this.



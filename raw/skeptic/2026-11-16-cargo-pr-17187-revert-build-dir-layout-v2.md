https://github.com/rust-lang/cargo/pull/17187
2026-11-16

fetched_with: gh pr view 17187 -R rust-lang/cargo --json title,state,mergedAt,body --jq '"title: \(.title)\nstate: \(.state)\nmerged: \(.mergedAt)\n\n\(.body)"'

title: Revert "feat: Stablize build-dir layout v2"
state: MERGED
merged: 2026-07-07T16:27:15Z


### What does this PR try to resolve?

This PR reverts the final stabilization commit (668039de97e189dbe3ca0a9b1085089c394cd636) in https://github.com/rust-lang/cargo/pull/16807.

At today's Cargo meeting, we discussed the recent bug reports (notably #17183) from the new `build-dir` landing on nightly. 
We felt it would be safer to revert so that are not on a shot clock to fix the issues.


### How to test and review this PR?

no response

r? @epage 



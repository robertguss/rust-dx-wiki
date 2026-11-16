https://github.com/rust-lang/rust/issues/158844
2026-11-16

fetched_with: gh api repos/rust-lang/rust/issues/158844 --jq '"title: \(.title)\nstate: \(.state)\ncreated: \(.created_at)\nupdated: \(.updated_at)\nlabels: \([.labels[].name]|join(", "))\n\n\(.body)"'; echo; echo '--- last comments ---'; gh api 'repos/rust-lang/rust/issues/158844/comments?per_page=100' --jq '.[-8:][] | "[\(.created_at) \(.user.login)] \(.body)\n"'

title: Tracking Issue for Relink Don't Rebuild
state: open
created: 2026-07-06T08:09:08Z
updated: 2026-09-16T13:08:16Z
labels: C-tracking-issue


<!--
NOTE: For library features, please use the "Library Tracking Issue" template instead.

Thank you for creating a tracking issue! 📜 Tracking issues are for tracking a
feature from implementation to stabilisation. Make sure to include the relevant
RFC for the feature if it has one. Otherwise provide a short summary of the
feature and link any relevant PRs or issues, and remove any sections that are
not relevant to the feature.

Remember to add team labels to the tracking issue.
For a language team feature, this would e.g., be `T-lang`.
Such a feature should also be labeled with e.g., `F-my_feature`.
This label is used to associate issues (e.g., bugs and design questions) to the feature.
-->

This is a tracking issue for the MCP ["Relink Don't Rebuild"](https://github.com/rust-lang/compiler-team/issues/790).
The unstable option for this issue is `public_api_hash`

## About tracking issues

Tracking issues are used to record the overall progress of implementation.
They are also used as hubs connecting to other relevant issues, e.g., bugs or open design questions.
A tracking issue is however *not* meant for large scale discussion, questions, or bug reports about a feature.
Instead, open a dedicated issue for the specific matter and add the relevant feature gate label.
Discussion comments will get marked as off-topic or deleted.
Repeated discussions on the tracking issue may lead to the tracking issue getting locked.

There is a dedicated [zulip channel](https://rust-lang.zulipchat.com/#narrow/channel/604410-t-compiler.2Frelink-dont-rebuild) for discussions related to Relink Don't Rebuild

## Steps
<!--
Include each step required to complete the feature. Typically this is a PR
implementing a feature, followed by a PR that stabilises the feature. However
for larger features an implementation could be broken up into multiple PRs.
-->

### Implement the MCP
There is currently a [large open PR](https://github.com/rust-lang/rust/pull/156940) providing an initial working implementation of RDR. This should be split into smaller ones:
 - [ ] add option to stable hash spans as if they had no parents 
 - [ ] add missing StableHash derives/impls for structs encoded in the metadata
 - [ ] :star2: implement public api hash as the stable hash of (almost) all encoded data
 - [ ] add rustc test attribute for testing public api hashing in incremental tests
 - [ ] :star: move public hash to the crate header, handle public and private hashes in the resolver
 - [ ] encode defindex as DefPathHash in the metadata when public api hashing is enabled
 - [ ] use SyntaxContext instead of raw u32 in HygieneEncodeContext::encode
 - [ ] :star2: add the metadata reachability graph
 - [ ] :star: remove LocalExpnId::ROOT -> CRATE_DEF_ID edge from the reachability graph
 - [ ] :star: include trait impls in the reachability graph
 - [ ] remove stripped cfg items when public api hashing is enabled
 - [ ] remove traits when public api hashing is enabled
 - [ ] remove private module children when public api hashing is enabled
 - [ ] disable upstream monomorphizations when public api hashing is enabled
 - [ ] add VisibilityDefId
 - [ ] add is_exportable query
 - [ ] move exported_generic_symbols and exported_non_generic_symbols behind the private hash. Move parts used before linking into tables
 - [ ] sanity checks: allow access to private hash in metadata compiled without public_api_hash and in sessions requiring a linking step
 - [ ] add tests, -Zls=public_hash

Ones marked with :star2: are large PR-s, needing more reviewer effort. :star: are middle sized or need understanding of RDR to review. Ones without markers are small and should be easy to review without much knowledge of the feature.

#### Features not yet implemented, but should be done before stabilization
 - [ ] Cargo intergration
 - [ ] Implement a safe mechanism for accessing private data of dependencies. In general, when compiling a crate, accessing private data of dependencies is unsound. Since recompiling a dependency might not trigger a recompile for the current crate. An important exception is when the current crate's compilation fails. When the compilation fails, rustc should be allowed to access private data of dependencies to produce better error messages. The resolver makes use of this to produce visibility errors or tell the user that some item is behind a feature flag. The current implementation simply removes these from the metadata when RDR is enabled.
 - [ ] readd removed private items (except module children)
 - [ ] refactor resolver to use public module children for name resolution, private for error reporting. This might need a large refactor. The resolver currently doesn't care whether something is public/private during name resolution. Visibility check is done after name resolution is finished.
 - [ ] readd removed private module children
 - [ ] optimize the hashing of public items
 - [ ] optimize hashing of spans. Some spans are used for diagnostics, there we need the hash of the source they cover, while some spans are only used as line info for debug info generation.
 - [ ] make hashing of public items incremental cache friendly. For a non-incremental build, the overhead of public api hashing is ~3% (double check this). For an incremental rebuild where nothing changes this currently sits at ~25%. 
 - [ ] remove `impl PublicTrait for PrivateStruct` trait impls from the public hash, where `PublicTrait` and `PrivateStruct` are defined in the local crate

Trait impls in a public api hash are partially done. Its current state:

| Trait visibility | Struct visibility | Should be in the public hash | Currently in the public hash |
|------------------|-------------------|------------------------------|------------------------------|
| Private          | Private           | No                           | No                           |
| Private          | Public            | No                           | No                           |
| Public           | Private           | No                           | Yes                          |
| Public           | Public            | Yes                          | Yes                          |

 - [ ] review the hashing of the remaining metadata fields. The current set of supported fields work for the frequently changing parts of most crates, but the metadata fields left without attention should be checked and documented
   - [ ] header
   - [ ] required_panic_strategy
   - [ ] panic_in_drop_strategy
   - [ ] dylib_dependency_formats
   - [ ] lib_features
   - [ ] stability_implications
   - [ ] diagnostic_items
   - [ ] native_libraries
   - [ ] foreign_modules
   - [ ] incoherent_impls
   - [ ] debugger_visualizers
   - [ ] stable_order_of_exportable_impls
   - [ ] target_modifiers
   - [ ] denied_partial_mitigations
   - [ ] compiler_builtins
   - [ ] needs_allocator
   - [ ] needs_panic_runtime
   - [ ] no_builtins
   - [ ] panic_runtime
   - [ ] profiler_runtime
   - [ ] symbol_mangling_version
   - [ ] specialization_enabled_in
   - [ ] public_api_hash_opt_enabled
  
- [ ] Adjust documentation ([see instructions on rustc-dev-guide][doc-guide])
  - [ ] what the feature can and can't fix. Strengths and weaknesses
  - [ ] how to structure a crate in a way that causes the least amount of change in the public api hash
  - [ ] add clippy lints helping to ensure the above

- [ ] Stabilization PR ([see instructions on rustc-dev-guide][stabilization-guide])
- [ ] Raise awareness of the feature. Rust is still known for its slow compile times. It will still be far from optimal, but RDR is a significant improvement for large projects, which could help start shifting that narrative.

[stabilization-guide]: https://rustc-dev-guide.rust-lang.org/stabilization_guide.html#stabilization-pr
[doc-guide]: https://rustc-dev-guide.rust-lang.org/stabilization_guide.html#documentation-prs

### Unresolved Questions
<!--
Include any open questions that need to be answered before the feature can be
stabilised. It is useful to link related discussions and conculsions as they
develop.
-->

#### Span sensitivity
Spans are part of the public api. Which has the unfortuante consequence that changing the span of public items (a simple operation like editing the body of a function moves the end of its span, editing its doc comment also moves it) will cause rebuild in dependants. Errors and warnings produced by dependants rely heavily on spans, and debug info also uses it (a bit differently, debug info only needs the line numbers, while diagnostics produced also read and emit the source code covered by the spans).

Span insensitivity would enable other public api hash optimizations which don't make sense without it:
- ignore reordering of repr(rust) enum variants, union or struct fields
- ignore adding private fields to a struct (with the usual caveats)
- ignore doc comment changes

There are multiple avenues for exploration:

 - add an option which simply ignores diagnostic spans for public api hashing. Combined with disabling debug info generation this could effectively make public api hashing span insensitive. This could be a major win for `cargo check`, which does not generate debug info.
 - add some kind of fast path which just reemits diagnostics and debug info.

#### v0 symbol mangling changes
Current v0 symbol mangling disambiguator does not work well with RDR. It uses a per crate global index based on the number of symbols in the crate. The symbol disambiguator part should be reworked to make them compatible. Currently, v0 symbol mangling panics when public api hashing is enabled in any dependency. 
### Implementation history

<!--
Include a list of all the PRs that were involved in implementing the feature.
-->



--- last comments ---


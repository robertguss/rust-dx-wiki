https://github.com/rust-lang/rust-analyzer/issues/22765
2026-11-16

fetched_with: gh api repos/rust-lang/rust-analyzer/issues/22765 --jq '"title: \(.title)\nstate: \(.state)\ncreated: \(.created_at)\nupdated: \(.updated_at)\nlabels: \([.labels[].name]|join(", "))\n\n\(.body)"'; echo; echo '--- last comments ---'; gh api 'repos/rust-lang/rust-analyzer/issues/22765/comments?per_page=100' --jq '.[-8:][] | "[\(.created_at) \(.user.login)] \(.body)\n"'

title: Daemonize rust-analyzer / Share it between clients
state: open
created: 2026-07-11T11:28:00Z
updated: 2026-08-24T08:12:38Z
labels: C-feature

With the rise of agents and folks doing more concurrent work on projects than ever, as well as agent harnesses adding more LSP support it becomes pretty common for folks to have a bunch of rust-analyzer instances running, which in turn will have a bunch of proc-macro servers running (if one configures r-a to use multiple its even worse).

In my opinion, rust-analyzer would benefit quite a bit from us daemonizing it per toolchain, that is we'd only spin up a proxy per client that then talks to the actual server process, allowing us to deduplicate a decent chunk of state as well as reducing the amount of concurrent system resources. An interesting outcome of this would be sharing of cross client workspace dependency analysis results as well as VFS content, especially when it comes to the standard libraries. Additionally, as we will likely add an MCP server to r-a soon after all we could then expose that MCP interface without having to spin up yet another r-a instance that just loads what is already loaded by the LSP client as well.

Naturally not all is well though, there is a specific issue with the LSP and its open/close documents invariants (what we call `MemDocs` internally). That is when a client "opens" a file, it becomes authorative of the files content. That means, multiple clients could own a file in this manner, with daemonizing this we now have the issue of deciding who is actually authorative of the file as we can only consider one of them as the current state of the file. In practice, this should not really become an issue I think especially if we consider crates-io and std source files as immutable (in which case we should discard the memdoc concept entirely imo).


Note there is precedent for this already, https://codeberg.org/p2502/lspmux

--- last comments ---
[2026-07-11T18:40:13Z ChayimFriedman2] Given that like you stated yourself there are already external solutions for that, and furthermore they work for any LSP server, why should this live in r-a?

[2026-08-24T08:12:38Z zetaloop] I've been building something close to this: [zetaloop/analyzed](https://github.com/zetaloop/analyzed).

It runs all analysis in one daemon process with a separate connection per client. Sessions with a compatible toolchain and Cargo configuration share one analysis backend. They can open different workspace roots, and their crate graphs merge so shared dependencies are analyzed once. A generic mux can't do that; it only multiplexes connections.

On-disk file contents are shared through a common VFS. Unsaved edits live in session-local overlays, so each client stays authoritative only for its own open buffers. Proc-macro client pools are shared across sessions too.



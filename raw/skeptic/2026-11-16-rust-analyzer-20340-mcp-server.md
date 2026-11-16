https://github.com/rust-lang/rust-analyzer/issues/20340
2026-11-16

fetched_with: gh api repos/rust-lang/rust-analyzer/issues/20340 --jq '"title: \(.title)\nstate: \(.state)\ncreated: \(.created_at)\nupdated: \(.updated_at)\nlabels: \([.labels[].name]|join(", "))\n\n\(.body)"'; echo; echo '--- last comments ---'; gh api 'repos/rust-lang/rust-analyzer/issues/20340/comments?per_page=100' --jq '.[-8:][] | "[\(.created_at) \(.user.login)] \(.body)\n"'

title: Could rust-analyzer provide a mcp server?
state: closed
created: 2025-07-30T06:26:00Z
updated: 2025-07-30T06:27:52Z
labels: C-feature

Just like [gopls](https://go.dev/gopls/features/mcp)

--- last comments ---
[2025-07-30T06:27:52Z lnicola] https://github.com/rust-lang/rust-analyzer/discussions/19608



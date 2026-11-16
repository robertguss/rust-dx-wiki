https://github.com/rust-lang/rust-analyzer/discussions/19608
2026-11-16

fetched_with: gh api graphql -f query='{repository(owner:"rust-lang",name:"rust-analyzer"){discussion(number:19608){title createdAt updatedAt closed body comments(last:12){nodes{createdAt author{login} body}}}}}' --jq '.data.repository.discussion | "title: \(.title)\ncreated: \(.createdAt)\nupdated: \(.updatedAt)\nclosed: \(.closed)\n\n\(.body)\n\n--- comments ---\n" + ([.comments.nodes[] | "[\(.createdAt) \(.author.login)] \(.body)"] | join("\n\n"))'

title: Model Context Protocol (MCP) Binary for rust-analyzer
created: 2025-04-16T14:47:50Z
updated: 2025-05-06T18:22:58Z
closed: false

## Overview

With the growing adoption of the Model Context Protocol (MCP) as a standard for enabling AI assistants to interact with codebases and development tools, integrating MCP support into rust-analyzer could enhance its capabilities. This integration would allow rust-analyzer to serve as a backend for AI-driven code assistance tools, facilitating tasks like symbol resolution, diagnostics, and code navigation.
## Motivation

MCP provides a structured protocol for AI assistants to communicate with various tools and services. By implementing an MCP-compatible binary, rust-analyzer can expose its rich language analysis features to AI models, enabling more intelligent code assistance. This integration aligns with the trend of enhancing developer tools with AI capabilities.
## Potential Benefits

* Enhanced AI Integration: Facilitates the development of AI-powered tools that can provide intelligent code assistance for Rust projects.

* Improved Developer Experience: Enables features like natural language code queries, automated refactoring suggestions, and context-aware code generation.

--- comments ---
[2025-05-05T21:31:23Z ChayimFriedman2] I don't think it's the job of rust-analyzer to implement an interface for LLMs, nor I see other language servers doing that. We also expose an API (the `ra_ap_X` crates), so anyone feeling it's important can do it themselves.

[2025-05-06T18:22:58Z lnicola] Why not a generic MCP server [for LSP](https://github.com/isaacphi/mcp-language-server)?


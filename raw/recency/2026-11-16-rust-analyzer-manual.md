https://rust-analyzer.github.io/manual.html
2026-11-16

# rust-analyzer

rust-analyzer is a language server that provides IDE functionality for
writing Rust programs. You can use it with any editor that supports
the Language Server
Protocol (VS
Code, Vim, Emacs, Zed, etc).

rust-analyzer features include go-to-definition, find-all-references,
refactorings and code completion. rust-analyzer also supports
integrated formatting (with rustfmt) and integrated diagnostics (with
rustc and clippy).

Internally, rust-analyzer is structured as a set of libraries for
analyzing Rust code. See
Architecture
for more details.

To improve this document, send a pull request:
https://github.com/rust-lang/rust-analyzer

The manual is written in markdown and includes
some extra files which are generated from the source code. Run
`cargo test` and `cargo xtask codegen` to create these.

If you have questions about using rust-analyzer, please ask them in the
“IDEs and Editors” topic of Rust
users forum.

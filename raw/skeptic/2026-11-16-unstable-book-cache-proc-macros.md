https://doc.rust-lang.org/unstable-book/compiler-flags/cache-proc-macros.html
2026-11-16

title: cache_proc_macros - The Rust Unstable Book
published_date: None
final_url: https://doc.rust-lang.org/unstable-book/compiler-flags/cache-proc-macros.html

## `cache-proc-macros`

The tracking issue for this feature is: #151364

---

This option instructs `rustc` to cache (derive) proc-macro invocations using the incremental system. Note that the compiler does not currently check whether the proc-macro is actually “cacheable” or not. If you use this flag when compiling a crate that uses non-pure proc-macros, it can result in stale expansions being compiled.

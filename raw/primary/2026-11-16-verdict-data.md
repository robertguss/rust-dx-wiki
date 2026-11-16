local:primary-evidence-assembly
Fetched: 2026-11-16
[
  [
    1,
    "confirmed",
    [
      [
        "state-survey",
        "When asked about which non-trivial problems people encounter, little changes overall compared to 2024: resource usage (slow compile times and storage usage) is still up there. The debugging story slipped from 2nd to 4th place (~2pp). We just started a survey to learn more about it!",
        "2026-03-02"
      ]
    ]
  ],
  [
    2,
    "confirmed",
    [
      [
        "compiler-survey",
        "Waiting too long for an incremental rebuild after making a small source code change was by far the most common complaint in the open answers that we received, and it was also the most common problem that respondents said they struggle with. Based on our respondents' answers, this comes down to three main bottlenecks:",
        "2025-09-10"
      ]
    ]
  ],
  [
    3,
    "confirmed",
    [
      [
        "compiler-survey",
        "Around 45% respondents who answered that they are no longer using Rust said that at least one of the reasons why they stopped were long compile times.",
        "2025-09-10"
      ]
    ]
  ],
  [
    4,
    "confirmed",
    [
      [
        "lld-release",
        "LLD is now the default linker on",
        "2025-09-18"
      ],
      [
        "lld-release",
        "target will now use the LLD linker for linking Rust crates by default.",
        "2025-09-18"
      ]
    ]
  ],
  [
    5,
    "confirmed",
    [
      [
        "build-performance",
        "❌ Requires using nightly Rust and an unstable Cargo feature",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    6,
    "outdated",
    [
      [
        "cranelift-2026",
        "This goal aims to improve the rust development experience through faster incremental code generation with `rustc_codegen_cranelift`. We’re targeting a 2x speedup inside the `rustc_codegen_cranelift` backend.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    7,
    "confirmed",
    [
      [
        "old-cranelift",
        "In our measurements on larger projects (e.g. Zed, Tauri, hickory-dns), we currently see roughly a 20% reduction of code generation time, translating to around 5% speedup of total compilation time for clean builds.",
        "2025H2 goal; day not stated"
      ]
    ]
  ],
  [
    8,
    "confirmed",
    [
      [
        "build-performance",
        "❌ Requires using nightly Rust and an unstable Rust feature",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    9,
    "confirmed",
    [
      [
        "wild-bench",
        "The benchmarks are just running the\nlinker, not the compiler.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    10,
    "confirmed",
    [
      [
        "wild",
        "The plan is to eventually make it incremental, however that isn't yet implemented.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    11,
    "refuted",
    [
      [
        "wild",
        "* WebAssembly (wasm32)",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    12,
    "confirmed",
    [
      [
        "fast-builds",
        "| Relink Don’t Rebuild - Prepare for stabilization | 2027 | Massive speedup of rebuilds in large multi-crate projects |",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    13,
    "confirmed",
    [
      [
        "hint-unused",
        "Currently, this option makes the compiler defer as much code generation as\npossible from functions in the crate, until later crates invoke those\nfunctions. Functions that never get invoked will never have code generated for\nthem.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    14,
    "confirmed",
    [
      [
        "proc-cache",
        "This option instructs `rustc` to cache (derive) proc-macro invocations using the incremental system. Note that the compiler does not currently check whether the proc-macro is actually “cacheable” or not. If you use this flag when compiling a crate that uses non-pure proc-macros, it can result in stale expansions being compiled.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    15,
    "confirmed",
    [
      [
        "tpde-doc",
        "Typically, compile times are 10–20x faster than the LLVM -O0 back-end with similar execution time, code size is ~10-30% larger for -O0 IR and similar for -O1 IR.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    16,
    "outdated",
    [
      [
        "tpde-internals",
        "`rustc` has an experimental TPDE-LLVM backend option which can be used to improve compile times for debug builds. TPDE is currently missing the “long tail” of features supported by LLVM, but `rustc` supports falling back to regular LLVM codegen if TPDE fails.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    17,
    "confirmed",
    [
      [
        "locking-issue",
        "Right now whenever a build happens we lock the entirety of the `target` directory for the whole build, but it may be possible for us to have a more granular locking strategy which allows multiple instances of Cargo to proceed in parallel instead of serializing them.",
        "Issue updated 2026-07-06"
      ]
    ]
  ],
  [
    18,
    "confirmed",
    [
      [
        "cargo-unstable",
        "Use fine grain locking instead of locking the entire build cache.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    19,
    "confirmed",
    [
      [
        "cargo-unstable",
        "was stabilized in the 1.91 release.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    20,
    "confirmed",
    [
      [
        "cross-cache",
        "These artifacts are local to the current workspace. This is not ideal as it requires Cargo to rebuild build units when we could simply reuse the artifacts that have previously been built for other workspaces.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    21,
    "confirmed",
    [
      [
        "cross-cache",
        "In 2026, we will design and implement this cache in Cargo, making it available on nightly for users to begin experimenting with. (tracked in rust-lang/cargo#5931)",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    22,
    "unverified",
    [
      [
        "prebuilt-issue",
        "Cargo assumes this is a location to source code, which it will then proceed to build.",
        "Issue updated 2026-04-06; original body historical"
      ]
    ]
  ],
  [
    23,
    "confirmed",
    [
      [
        "sccache",
        "Incrementally compiled crates cannot be cached.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    24,
    "confirmed",
    [
      [
        "bazel-remote",
        "Bazel uses an open-source\ngRPC protocol\nto allow for remote execution and remote caching.",
        "Not stated (living page; fetched 2026-11-16)"
      ],
      [
        "buck-remote",
        "Buck2 can use services that expose\nBazel's remote execution API in\norder to run actions remotely.",
        "Not stated (living docs)"
      ]
    ]
  ],
  [
    25,
    "confirmed",
    [
      [
        "cargo-config",
        "Support for tracking build artifacts is not yet implemented, and tracked in cargo#13136.",
        "Not stated (living page; fetched 2026-11-16)"
      ],
      [
        "cargo-config",
        "Periodically, Cargo will delete files that have not been used for some period of time.",
        "Not stated (living docs)"
      ]
    ]
  ],
  [
    26,
    "unverified",
    [
      [
        "rust-cache",
        "A GitHub Action that implements smart caching for rust/cargo projects with",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    27,
    "confirmed",
    [
      [
        "subsecond",
        "Subsecond is a hot-reloading library for Rust. It makes it easy to add Rust hot-reloading to your\nexisting Rust project with minimal integration overhead.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    28,
    "confirmed",
    [
      [
        "cargo-watch",
        "Cargo Watch is on life support: it will not receive further updates, but does remain available.",
        "Not stated (living page; fetched 2026-11-16)"
      ],
      [
        "cargo-watch",
        "Use [Bacon].",
        "Not stated (README)"
      ]
    ]
  ],
  [
    29,
    "confirmed",
    [
      [
        "nextest",
        "**Up to 3x as fast as cargo test**",
        "Not stated (living page; fetched 2026-11-16)"
      ],
      [
        "nextest-changelog",
        "## 0.9.151 - 2026-11-02¶",
        "2026-11-02 latest changelog entry"
      ]
    ]
  ],
  [
    30,
    "confirmed",
    [
      [
        "compiler-survey",
        "More than 35% users said that they consider the IDE and Cargo blocking one another to be a big problem. There is an existing workaround for this, where you can configure Rust Analyzer to use a different target directory than Cargo, at the cost of increased disk space usage.",
        "2025-09-10"
      ],
      [
        "ra-config",
        "Optional path to a rust-analyzer specific target directory.\nThis prevents rust-analyzer’s",
        "Not stated (living docs)"
      ]
    ]
  ],
  [
    31,
    "confirmed",
    [
      [
        "wizard",
        "- `fast-compile` - minimizes compilation times\n    - Disables debuginfo generation and uses a faster linker.\n    - In nightly mode, it also enables\n      the [Cranelift codegen backend](https://nnethercote.github.io/perf-book/build-configuration.html#cranelift-codegen-back-end)\n      and\n      the [parallel frontend](https://nnethercote.github.io/perf-book/build-configuration.html#experimental-parallel-front-end).\n- `fast-runtime` - maximizes runtime performance\n    - Enables [LTO](https://doc.rust-lang.org/cargo/reference/profiles.html#lto) and other settings designed to maximize\n      runtime performance.\n- `min-size` - minimizes binary size\n    - Similar to `fast-runtime`, but uses optimization flags designed for small binary size.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    32,
    "confirmed",
    [
      [
        "bevy-setup",
        "as dynamic library, preventing it from having to be statically linked each time you rebuild your project.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    33,
    "unverified",
    [
      [
        "cargo-ra",
        "rust-analyzer is a language server that provides IDE functionality for writing Rust programs.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    34,
    "confirmed",
    [
      [
        "ra-mcp",
        "This is a Model Context Protocol (MCP) server that provides integration with rust-analyzer, allowing\nAI assistants to analyze Rust code, get hover information, find definitions, references, and more.",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ],
  [
    35,
    "unverified",
    [
      [
        "cargo-steward",
        "**Fast, bounded Cargo builds for people and AI agents working across many\ngit worktrees.**",
        "Not stated (living page; fetched 2026-11-16)"
      ]
    ]
  ]
]

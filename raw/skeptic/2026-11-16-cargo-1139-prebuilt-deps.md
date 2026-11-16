https://github.com/rust-lang/cargo/issues/1139
2026-11-16

fetched_with: gh api repos/rust-lang/cargo/issues/1139 --jq '"title: \(.title)\nstate: \(.state)\ncreated: \(.created_at)\nupdated: \(.updated_at)\nlabels: \([.labels[].name]|join(", "))\n\n\(.body)"'; echo; echo '--- last comments ---'; gh api 'repos/rust-lang/cargo/issues/1139/comments?per_page=100' --jq '.[-8:][] | "[\(.created_at) \(.user.login)] \(.body)\n"'

title: Support for pre-built dependencies
state: open
created: 2015-01-09T12:45:30Z
updated: 2026-04-06T08:45:33Z
labels: A-caching, S-needs-design

*[View all comments](https://triagebot.infra.rust-lang.org/gh-comments/rust-lang/cargo/issues/1139)*

Currently you can add dependencies using `path` or `git`. Cargo assumes this is a location to source code, which it will then proceed to build.

My use-case stems from integrating Cargo into a private build and dependency management system. I need to be able to tell Cargo to only worry about building the current package. That is, I will tell it where the other already-built libraries are.

Consider two projects: `a` (lib) and `b` (bin) such that `b` depends on `a`:

``` toml
[package]

name = "b"
version = "0.0.1"
authors = ["me <plain@old.me>"]

[dependencies.a]

path = "/tmp/rust-crates/a"
```

A clean build will output something like:

```
> cargo build -v                                                                                                                                                                                                                                               master untracked
   Compiling a v0.0.1 (file:///private/tmp/rust-crates/b)
     Running `rustc /tmp/rust-crates/a/src/lib.rs --crate-name a --crate-type lib -g -C metadata=10d34ebdfa7a5b84 -C extra-filename=-10d34ebdfa7a5b84 --out-dir /private/tmp/rust-crates/b/target/deps --emit=dep-info,link -L dependency=/private/tmp/rust-crates/b/target/deps -L dependency=/private/tmp/rust-crates/b/target/deps`
/tmp/rust-crates/a/src/lib.rs:1:1: 3:2 warning: function is never used: `it_works`, #[warn(dead_code)] on by default
/tmp/rust-crates/a/src/lib.rs:1 fn it_works() {
/tmp/rust-crates/a/src/lib.rs:2     println!("a works");
/tmp/rust-crates/a/src/lib.rs:3 }
   Compiling b v0.0.1 (file:///private/tmp/rust-crates/b)
     Running `rustc /private/tmp/rust-crates/b/src/lib.rs --crate-name b --crate-type lib -g -C metadata=429959f67e51bc23 -C extra-filename=-429959f67e51bc23 --out-dir /private/tmp/rust-crates/b/target --emit=dep-info,link -L dependency=/private/tmp/rust-crates/b/target -L dependency=/private/tmp/rust-crates/b/target/deps --extern a=/private/tmp/rust-crates/b/target/deps/liba-10d34ebdfa7a5b84.rlib`
/private/tmp/rust-crates/b/src/lib.rs:1:1: 3:2 warning: function is never used: `it_works`, #[warn(dead_code)] on by default
/private/tmp/rust-crates/b/src/lib.rs:1 fn it_works() {
/private/tmp/rust-crates/b/src/lib.rs:2     println!("b works");
/private/tmp/rust-crates/b/src/lib.rs:3 }
```

Importantly:

```
--extern a=/private/tmp/rust-crates/b/target/deps/liba-10d34ebdfa7a5b84.rlib
```

Would it make sense to expose a `extern` option (in `dependencies.a`) for low level customization? 

``` toml
[dependencies.a]

extern = "/private/tmp/rust-crates/b/target/deps/liba-10d34ebdfa7a5b84.rlib"
```

This can be worked around by using a build script along the lines of:

``` rust
use std::io::fs;

fn main() {
    let from = Path::new("/tmp/rust-crates/a/target/liba-b2092cdbfc1953bd.rlib");
    let to = Path::new("/tmp/rust-crates/b/blah/liba-b2092cdbfc1953bd.rlib");
    fs::copy(&from, &to).unwrap();
    println!("cargo:rustc-flags=-L /tmp/rust-crates/b/blah");
}
```

But it is not ideal to have to do this with every project.


--- last comments ---
[2023-09-26T13:52:46Z bjorn3] How does that work with different programs that need mutually exclusive features of a crate? Or what about a program that needs a crate with the `std` feature enabled and another one which doesn't want to use libstd? While cargo features are supposed to be additive, many crates don't follow this advice. In some case they even disable features using a cargo feature by following the rationale that it is a feature to allow compiling for more targets even though it is an negative feature as it causes compile errors for crates that need those things.

[2023-09-26T16:18:54Z navi-desu] >How does that work with different programs that need mutually exclusive features of a crate?

as far as i know, it conflicts, but

> While cargo features are supposed to be additive, many crates don't follow this advice.
if the common behaviour is to have features work in additive ways, the packager could make an exception for a specific binary that doesn't follow that. would be the simplest solution

if there's enough binary programs for this to be quite common, i'd have to poke and see. probably drop the idea of pre-compiling rlibs, sticking to installing only the source, since i can't see a better solution yet (still a improvement over the current way gentoo packages rust apps imo, but sad). precompiling libs for each package is the same as just installing the source, but with extra steps, so that's eh.

it's either get packages to share precompiled rlibs, or install the sources and let packages build them

[2023-09-26T17:52:05Z dreamcat4] it sounds analagous to re-inventing the wheel with respect to flatpaks, which are built ontop of versioned dependancies. such that multiple versions are installed, several duplicate clones of same libraries. and ostree to point to some git-esq btree structure or whatever it is.

i am not saying re-invent the wheel, but maybe there are already similar solutions out there that could be considered, evaluated, adapted to then fit the rust / cargo infrastructure?

[2023-11-16T21:48:42Z epage] One problem I've had with pre-compiled package is "pre-compiled for what?"
- Target platform
- Dependency tree versions (and how they get unified or not with yours)
- Feature flags

#5931 takes the opposite approach.  Instead of trying to have a fixed set of the above that is pre-compiled, it is reactive and caches it on-demand.  Of course, plugins could then be extended to upload common sets.

In thinking of this, I thought of a good analogy for a way forward for pre-compiled.

We have the build-std project to make `std` act more like a regular package.  What if we allowed doing the opposite and allowed a workspace-of-packages to act like std.
- It'd have its own lockfile
- There is one fixed set of features (e.g. `lib.required-features`)
- You are responsible for dealing with target platform

To put this in C++ terms, a crate lib would be like a headers only library while this new concept would be like creating a proper SO/DLL.  It would be designed for it and the types / systems would be unique.

I will say that #5931 will likely involve a lot less design work and would be a faster path to *something*.

[2025-02-13T09:41:20Z marcbrevoort-cyberhive] > You can't guarantee that a pre-built Rust library will work unless it's built with the exact same SHA of the compiler.

Would be really nice if this limitation could be overcome somehow. 



[2025-02-22T23:31:50Z IGN-Styly] > > You can't guarantee that a pre-built Rust library will work unless it's built with the exact same SHA of the compiler.
> 
> Would be really nice if this limitation could be overcome somehow.

I am currently working in a project and have ran into this issue, as building in diffirent dirs is yielding different typeids.

[2026-04-06T08:09:30Z pbower] Hi - on this issue, my understanding is that there is currently no real-way to work with pre-built dependencies, which means that one must release their source code in full.  Is this correct?

Here's what I've found so far:

**cdylib + C ABI (.so + .h):** Works, stable across compiler versions, but you can't pass Futures or Streams across the boundary. Consumers lose native async integration. Fine for C/C++ consumers, not for Rust ones.

**Pre-compiled .rlib:**

- Consumers get native Rust types, async works, but it's pinned to a specific rustc version (no stable ABI).
- Cargo has no native support for rlib dependencies (this issue), so you end up using --extern via .cargo/config.toml which is a hack.
- rust-analyzer doesn't pick up crates declared this way, so no hover docs.

**Standalone types crate + rlib:**

- Define the public types and doc comments in a source crate, ship the rlib separately for the actual implementations.
- Consumer gets IDE support from the types crate. But the types in the source crate and the types in the rlib are different types to rustc, so they're incompatible. And orphan rules prevent adding impls across crate boundaries.

**Private registry (ship source):** Everything works perfectly - async, IDE, docs. But you're handing over the source. Watermarking + legal terms are the protection, not technical measures.

Is this understanding correct? If so, would it be possible to raise the priority on this issue? The concern I have is that, in 2026, releasing source code is heavily weighted towards being trained into AI models or replicated by larger competitors, particularly when there is genuine IP/ smarts involved, making it more difficult for regular folk to compete.

Happy to play a part and contribute.

Thanks

[2026-04-06T08:45:33Z bjorn3] > cdylib + C ABI (.so + .h): Works, stable across compiler versions, but you can't pass Futures or Streams across the boundary. Consumers lose native async integration. Fine for C/C++ consumers, not for Rust ones.

You can make a stable ABI copy of the `Future` trait and `Waker` type and then on both sides of the ABI convert the version in the standard library to this stable ABI version and back.

> Pre-compiled .rlib:

Aside from the downsides you mentioned, this still leaks a fair amount of private details of your crates. It leaks the full source paths of every included file as well as exact locations of newlines within those files and for each definition the line and column they were defined. It leaks all private declarations (modules, types, function names, signatures, ...) In addition for many functions it includes MIR which should not be terribly hard to reverse back to the original logic. If you are on nightly you can use `rustc -Zls=all /path/to/rlib` to get a small subset of the things that are leaked.



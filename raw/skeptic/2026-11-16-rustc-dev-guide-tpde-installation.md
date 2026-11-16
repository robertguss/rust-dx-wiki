https://rustc-dev-guide.rust-lang.org/tpde/installation.html
2026-11-16

title: Installation - Rust Compiler Development Guide
published_date: None
final_url: https://rustc-dev-guide.rust-lang.org/tpde/installation.html

# Installation

TPDE is not currently distributed through `rustup`, and needs to be built locally. The TPDE backend is Linux-only.

## Build instructions

Follow the instructions at How to build and run the compiler to clone the `rust-lang/rust` repository and set up a basic bootstrap configuration with the `compiler` profile.

You will also need to enable `llvm.tpde = true` in `bootstrap.toml`, and, due to present limitations with the way LLVM is built, disable CI LLVM downloads with `llvm.download-ci-llvm = false`.

Afterwards, linking the toolchain with rustup will allow you to use it through cargo:

```
rustup toolchain link stage1 build/host/stage1
# in other crate
RUSTFLAGS="-Zllvm-tpde" cargo +stage1 build
```

You can then run the compiler test suite:

```
./x test --stage 1 tests/ui --compiletest-rustc-args="-Zllvm-tpde" # or -Zllvm-tpde=only
./x test --stage 1 tests/run-make --compiletest-rustc-args="-Zllvm-tpde" # or -Zllvm-tpde=only
```

## Build instruction for TPDE itself

Following the Rust build instructions above will build the TPDE library used by the Rust compiler.
However, if working directly on TPDE, the TPDE docs have instructions on how to build TPDE and run its test suite, which is not exercised by bootstrap.

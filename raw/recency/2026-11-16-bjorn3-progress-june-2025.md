https://bjorn3.github.io/2025/06/30/progress-report-june-2025.html
2026-11-16

# Progress report on rustc\_codegen\_cranelift (June 2025)

There has been a fair bit of progress since the last progress report! There have been 476 commits since the last progress report.

You can find a precompiled version of cg\_clif at https://github.com/rust-lang/rustc\_codegen\_cranelift/releases/tag/dev or in the rustc-codegen-cranelift-preview rustup component if you want to try it out.

# Achievements in the past 7 months

#### Unwinding

Cranelift has finally implemented support for cleanup during stack unwinding on Linux.

A little bit of history: As part of my bachelor thesis I finished a little under a year ago, I implemented support for unwinding in Cranelift. This was mostly working, however when I revisited the code after finishing writing of my thesis to get it upstreamed, I discovered that there were some cases where the register allocator would insert moves after a call instruction that can unwind and then expect these moves to be executed before jumping to any of the successors of the call instruction. This however can’t happen when unwinding as unwinding directly jumps from the unwinding call to the exception handler block. I tried a bit to fix this, but got stuck on limitations in Cranelift’s register allocator. In addition I got busy with my day job. Fast forward to about two months ago, when Chris Fallin (the main author of major parts of Cranelift) started implementing support for exception handling in Cranelift, fixing the limitations of the register allocator that I got stuck on in the process. The overall design is similar to my proposal, though the details of the Cranelift IR extensions are more elegant than what I previously came up with. I was able to rebase the cg\_clif changes from my thesis on top of the newly landed Cranelift changes with minor effort after a couple of small fixes on the Cranelift side. Thanks a lot for working on unwinding support for Cranelift, Chris!

A walkthrough of how unwinding is actually implemented in cg\_clif can be found at https://tweedegolf.nl/en/blog/157/exception-handling-in-rustc-codegen-cranelift.

Unwinding support in cg\_clif will remain disabled by default for now pending investigation of some build performance issues. In addition it currently doesn’t work on Windows and macOS. On macOS there are some minor differences around the exact encoding of the unwinding tables that haven’t been implemented yet. On Windows adding support will be a fair bit more complicated however. Windows uses the funclets based SEH rather than the landingpads based itanium unwinding (

```
.eh_frame
```

) for unwinding. Cranelift only supports landingpads.

* issue wasmtime#1677: Support cleanup during unwinding
* bytecodealliance/rfcs#36: Implementing the exception handling proposal in Wasmtime
* issue #1567: Support unwinding on panics
* wasmtime#10485: Cranelift: remove block params on critical-edge blocks. (thanks @cfallin!)
* wasmtime#10502: Cranelift: remove return-value instructions after calls at callsites. (thanks @cfallin!)
* wasmtime#10510: Cranelift: initial try\_call / try\_call\_indirect (exception) support. (thanks @cfallin!)
* wasmtime#10593: Some fixes for try\_call
* wasmtime#10609: Cranelift: move exception-handler metadata into callsites. (by me and @cfallin)
* wasmtime#10702: Avoid clobbering all float registers in the presence of try\_call on arm64
* wasmtime#10709: Cranelift: fix invalid regalloc constraints on try-call with empty handler list. (thanks @cfallin!)
* ab514c9: Pass UnwindAction to a couple of functions
* 9495eb5: Pass Module to UnwindContext
* #1575: Preparations for exception handling support
* #1584: Experimental exception handling support on Linux

#### ARM

CI now builds and tests on native arm64 Linux systems rather than testing a subset of the tests in QEMU. Inline asm on arm64 can now use vector registers. And the half and bytecount crates are now fixed on arm64.

* #1557: Test and dist for arm64 linux on CI
* #1564: Fix usage of vector registers in inline asm on arm64
* #1566: Fix the half and bytecount crates on arm64

#### f16/f128 support

@beetrees contributed support for the unstable f16 and f128 types.

* wasmtime#8860: Initial f16 and f128 support (thanks @beetrees!)
* wasmtime#9045: Add initial f16 and f128 support to the x64 backend (thanks @beetrees!)
* wasmtime#9076: Add initial f16 and f128 support to the aarch64 backend (thanks @beetrees!)
* wasmtime#10652: Add inital support for f16 without Zfh and f128 to the riscv64 backend (thanks @beetrees!)
* wasmtime#10691: Add initial f16 and f128 support to the s390x backend (thanks @beetrees!)
* #1574: Add f16/f128 support (thanks @beetrees!)

#### Sharing code between codegen backends

I’ve made two PR’s to rustc to share more code between codegen backends. This reduces the maintenance burden of both cg\_clif and rustc. In the future I would like to migrate the entire inline asm handling of cg\_clif to cg\_ssa to be used as fallback for codegen backends that don’t natively support inline asm.

* rust#132820: Add a default implementation for CodegenBackend::link
* rust#134232: Share the naked asm impl between cg\_ssa and cg\_clif
* rust#141769: Move metadata object generation for dylibs to the linker code

#### SIMD

Some new vendor intrinsics were implemented.

* b004312: Implement arm64 vaddlvq\_u8 and vld1q\_u8\_x4 vendor intrinsics
* 1afce7c: Implement simd\_insert\_dyn and simd\_extract\_dyn intrinsics
* 49bfa1a: Fix simd\_insert\_dyn and simd\_extract\_dyn intrinsics with non-pointer sized indices

#### ABI

ABI handling for 128bit integers libcalls has been improved. In addition the abi-cafe version we test against has been updated to 1.0. Thanks to a bunch of new features it has, we no longer need to patch it’s source code, making it easier to do future updates.

* #1546: Fix the ABI for libcalls
* #1582: Update to abi-cafe 1.0
* b7cfe2f: Use the new –debug flag of abi-cafe

# Challenges

#### SIMD

While

```
core::simd
```

is fully supported through emulation using scalar operations, many platform specific vendor intrinsics in

```
core::arch
```

are not supported. This has been improving though with the most important x86\_64 and arm64 vendor intrinsics implemented.

If your program uses any unsupported vendor intrinsics you will get a compile time warning and if it actually gets reached, the program will abort with an error message indicating which intrinsic is unimplemented. Please open an issue if this happens.

* issue #171: std::arch SIMD intrinsics

#### ABI

There are still several remaining ABI compatibility issues with LLVM. On arm64 Linux there is a minor incompatibility with the C ABI, but the Rust ABI works just fine. On arm64 macOS there are several ABI incompatibilities that affect the Rust ABI too, so mixing cg\_clif and cg\_llvm there isn’t recommended yet. And on x86\_64 Windows there is also an incompatibility around return values involving i128. I’m slowly working on fixing these.

* issue #1525: Tracking issue for abi-cafe failures

# Contributing

Contributions are always appreciated. Feel free to take a look at good first issues and ping me (@bjorn3) for help on either the relevant github issue or preferably on the rust lang zulip if you get stuck.

https://github.com/rust-lang/rust/releases
2026-11-16

fetched_with: gh api 'repos/rust-lang/rust/releases?per_page=6' --jq '.[]|"=== \(.tag_name) published \(.published_at[:10])\n\(.body)\n"'

=== 1.100.0 published 2026-11-12
<a id="1.100.0-Language"></a>

## Language

- [Stabilize never type](https://github.com/rust-lang/rust/pull/155499)
- [Lint against repeated `#[repr(..)]` attributes](https://github.com/rust-lang/rust/pull/157036)
- [Stabilize `extern "custom"`](https://github.com/rust-lang/rust/pull/158504)
- [Extend `dropping_references`, `dropping_copy_types` and `undropped_manually_drops` lints to `drop_in_place`](https://github.com/rust-lang/rust/pull/160229)
- [`unfulfilled_lint_expectations` no longer fires on `#[expect(dead_code)]` inside code that is covered by a dead parent's diagnostic](https://github.com/rust-lang/rust/pull/161005)
- [Turn the error for `repr(align)` fields in a `repr(packed)` type into a deny-by-default lint `aligned_fields_in_packed`](https://github.com/rust-lang/rust/pull/162160)
- [volatile: allow accesses to non-AM memory to trap](https://github.com/rust-lang/rust/pull/160564/)

<a id="1.100.0-Compiler"></a>

## Compiler

- [Stabilize `-Cprofile-sample-use`](https://github.com/rust-lang/rust/pull/155942)
- [Enable next solver by default in orphanck](https://github.com/rust-lang/rust/pull/160668)

<a id="1.100.0-Platform-Support"></a>

## Platform Support

- [`i686-pc-windows-gnu` is now a tier 2 without host tools target](https://github.com/rust-lang/rust/pull/161681)
- [Promote `wasm32-wasip3` to Tier 2](https://github.com/rust-lang/rust/pull/161940)
- [Add new Tier 3 target `powerpc64-sony-ps3`](https://github.com/rust-lang/rust/pull/162072)

Refer to Rust's [platform support page](https://doc.rust-lang.org/rustc/platform-support.html) for more information on Rust's tiered platform support.

<a id="1.100.0-Libraries"></a>

## Libraries

- [Stabilize custom allocators](https://github.com/rust-lang/rust/pull/156882)
- [Map `ENOTSUP` to `ErrorKind::Unsupported`](https://github.com/rust-lang/rust/pull/158580)
- [Fix soundness issues in `std::sys::pal::sgx::waitqueue::unsafe_list`](https://github.com/rust-lang/rust/pull/161334)

<a id="1.100.0-Stabilized-APIs"></a>

## Stabilized APIs

- [`impl PartialEq<Cow<'_, [U]>> for Vec<T, A>`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#impl-PartialEq%3CCow%3C'_,+%5BU%5D%3E%3E-for-Vec%3CT,+A%3E)
- [`impl PartialEq<Cow<'_, [U]>> for &[T]`](https://doc.rust-lang.org/stable/std/primitive.slice.html#impl-PartialEq%3CCow%3C'_,+%5BU%5D%3E%3E-for-%26%5BT%5D)
- [`impl PartialEq<Cow<'_, [U]>> for &mut [T]`](https://doc.rust-lang.org/stable/std/primitive.slice.html#impl-PartialEq%3CCow%3C'_,+%5BU%5D%3E%3E-for-%26mut+%5BT%5D)
- [`std::alloc::Allocator`](https://doc.rust-lang.org/stable/std/alloc/trait.Allocator.html)
- [`std::alloc::Global`](https://doc.rust-lang.org/stable/std/alloc/struct.Global.html)
- [`std::alloc::System`](https://doc.rust-lang.org/stable/std/alloc/struct.System.html)
- [`impl Allocator for Global`](https://doc.rust-lang.org/stable/std/alloc/trait.Allocator.html#impl-Allocator-for-Global)
- [`impl Allocator for System`](https://doc.rust-lang.org/stable/std/alloc/trait.Allocator.html#impl-Allocator-for-System)
- [`impl<A: Allocator> Allocator for &A`](https://doc.rust-lang.org/stable/std/alloc/trait.Allocator.html#impl-Allocator-for-%26A)
- [`impl<T: Allocator, A: Allocator> Allocator for Box<T, A>`](https://doc.rust-lang.org/stable/std/alloc/trait.Allocator.html#impl-Allocator-for-Box%3CT,+A%3E)
- [`impl<A: Allocator> Allocator for &mut A`](https://doc.rust-lang.org/stable/std/alloc/trait.Allocator.html#impl-Allocator-for-%26mut+A)
- [`impl<T: Allocator, A: Allocator> Allocator for Arc<T, A>`](https://doc.rust-lang.org/stable/std/alloc/trait.Allocator.html#impl-Allocator-for-Arc%3CT,+A%3E)
- [`impl<T: Allocator, A: Allocator> Allocator for Rc<T, A>`](https://doc.rust-lang.org/stable/std/alloc/trait.Allocator.html#impl-Allocator-for-Rc%3CT,+A%3E)
- [`Box::new_in`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.new_in)
- [`Box::from_raw_in`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.from_raw_in)
- [`Box::from_non_null_in`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.from_non_null_in)
- [`Box::into_raw_with_allocator`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.into_raw_with_allocator)
- [`Box::into_non_null_with_allocator`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.into_non_null_with_allocator)
- [`Box::allocator`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.allocator)
- [`Vec::new_in`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#method.new_in)
- [`Vec::with_capacity_in`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#method.with_capacity_in)
- [`Vec::from_raw_parts_in`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#method.from_raw_parts_in)
- [`Vec::from_parts_in`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#method.from_parts_in)
- [`Vec::into_raw_parts_with_allocator`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#method.into_raw_parts_with_allocator)
- [`Vec::into_parts_with_allocator`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#method.into_parts_with_allocator)
- [`Vec::allocator`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#method.allocator)
- [`Child::main_thread_handle`](https://doc.rust-lang.org/stable/std/os/windows/process/trait.ChildExt.html#tymethod.main_thread_handle)
- [`impl Default for std::sync::Once`](https://doc.rust-lang.org/stable/std/sync/struct.Once.html#impl-Default-for-Once)
- [`bool::toggle`](https://doc.rust-lang.org/stable/std/primitive.bool.html#method.toggle)
- [`Box::take`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.take)
- [`Box::map`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.map)
- [`Rc::map`](https://doc.rust-lang.org/stable/std/rc/struct.Rc.html#method.map)
- [`Arc::map`](https://doc.rust-lang.org/stable/std/sync/struct.Arc.html#method.map)
- [`impl AsRef<T> for !`](https://doc.rust-lang.org/stable/std/primitive.never.html#impl-AsRef\<T\>-for-!)
- [`impl AsMut<T> for !`](https://doc.rust-lang.org/stable/std/primitive.never.html#impl-AsMut\<T\>-for-!)
- [`core::mem::DropGuard`](https://doc.rust-lang.org/stable/core/mem/struct.DropGuard.html)
- [`core::mem::conjure_zst`](https://doc.rust-lang.org/stable/core/mem/fn.conjure_zst.html)
- [`UnsafeCell::replace`](https://doc.rust-lang.org/stable/std/cell/struct.UnsafeCell.html#method.replace)
- [`UnsafeCell::as_ref_unchecked`](https://doc.rust-lang.org/stable/std/cell/struct.UnsafeCell.html#method.as_ref_unchecked)
- [`UnsafeCell::as_mut_unchecked`](https://doc.rust-lang.org/stable/std/cell/struct.UnsafeCell.html#method.as_mut_unchecked)
- [`str::trim_prefix`](https://doc.rust-lang.org/stable/std/primitive.str.html#method.trim_prefix)
- [`str::trim_suffix`](https://doc.rust-lang.org/stable/std/primitive.str.html#method.trim_suffix)
- [`[T]::trim_prefix`](https://doc.rust-lang.org/stable/std/primitive.slice.html#method.trim_prefix)
- [`[T]::trim_suffix`](https://doc.rust-lang.org/stable/std/primitive.slice.html#method.trim_suffix)
- [`Path::trim_prefix`](https://doc.rust-lang.org/stable/std/path/struct.Path.html#method.trim_prefix)
- [`Vec::from_fn`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#method.from_fn)
- [`os::windows::process::CommandExt::show_window`](https://doc.rust-lang.org/stable/std/os/windows/process/trait.CommandExt.html#tymethod.show_window)

<a id="1.100.0-Cargo"></a>

## Cargo

- Introduced Cargo's own linting system: some Cargo warnings are now emitted as lints that users can control in the `[lints.cargo]` table. This includes a new built-in unused dependency check via the `cargo::unused_dependencies` lint. [docs](https://doc.rust-lang.org/stable/cargo/reference/lints.html) [\#17298](https://github.com/rust-lang/cargo/pull/17298)
- Introduced minimum publish age configurations, also known as dependency cooldowns. When the relevant config is set, the resolver ignores versions published more recently than that, unless they are already in `Cargo.lock`. ([RFC 3923](https://rust-lang.github.io/rfcs/3923-cargo-min-publish-age.html)) [docs](https://doc.rust-lang.org/stable/cargo/reference/resolver.html#publish-age) [\#17335](https://github.com/rust-lang/cargo/pull/17335)
- cargo-install: now uses the existing lockfile in the `.crate` tarball by default. `--locked` in cargo install becomes a no-op. [\#17388](https://github.com/rust-lang/cargo/pull/17388)
- Cargo now uses a new directory layout for intermediate build artifacts. Tools that inspect the build directory may need to use [Cargo’s JSON messages](https://doc.rust-lang.org/stable/cargo/reference/external-tools.html#json-messages) to locate build artifacts instead of relying on the build directory layout. The layout is not a stable interface and is subject to change. ([build cache doc](https://doc.rust-lang.org/stable/cargo/reference/build-cache.html)) [\#17354](https://github.com/rust-lang/cargo/pull/17354)

## Rustdoc

- [Add new `invalid_markdown_table` rustdoc lint](https://github.com/rust-lang/rust/pull/159583)

<a id="1.100.0-Compatibility-Notes"></a>

## Compatibility Notes

- [Closures now more precisely capture variables used in `if let`. This may cause new errors](https://github.com/rust-lang/rust/pull/154210)
- [Check dyn-compatibility of trait objects in more places](https://github.com/rust-lang/rust/pull/154992)
- [`Infallible` is now a type alias to `!`](https://github.com/rust-lang/rust/pull/155499)
- [The never type fallback was changed to `!` on all editions](https://github.com/rust-lang/rust/pull/155499)
- [`box` patterns are no longer syntactically allowed](https://github.com/rust-lang/rust/pull/156749)
- [Report Query Cycle errors in more cases when computing the layout of enums with explicit discriminants](https://github.com/rust-lang/rust/pull/157562)
- [Always escape grapheme extenders in `str::escape_debug`](https://github.com/rust-lang/rust/pull/158303)
- [Make let-else respect `macro_rules` `expr` metavariable grouping](https://github.com/rust-lang/rust/pull/158515)
- [`Iterator::{min,max}(_by_key)` changed which `Ord` methods they use.](https://github.com/rust-lang/rust/pull/160203) This cannot change behaviour (other than being potentially faster) for types correctly following the [`Ord` rules](https://doc.rust-lang.org/std/cmp/trait.Ord.html), but may impact types with inconsistent trait implementations.
- [Emit an error when trying to enable SSE/AVX on an x86 (32bit or 64bit) softfloat target](https://github.com/rust-lang/rust/pull/160302)
- [Require windowed (and exception) for Xtensa ABI](https://github.com/rust-lang/rust/pull/160643)
- [windows-gnullvm: always link libunwind statically](https://github.com/rust-lang/rust/pull/160712)
- [From version 1.94 up to 1.100 a number of ARMv7-A hardfloat targets required the `VFPv3-D32` FPU as a minimum, as they erroneously had the `d32` feature in their baseline list of features. Breakage introduced as a result of correcting this can be fixed by passing `-Ctarget-feature=+d32` to Rust.](https://github.com/rust-lang/rust/pull/160911)
- [Change "Rust" ABI on x86 to use SSE registers if they are always-available for the current target](https://github.com/rust-lang/rust/pull/161583)
- [Make the `ambiguous_glob_imported_traits` lint fire in slightly more cases](https://github.com/rust-lang/rust/pull/161805)
- [Make `+fix-cortex-a53-835769` a default feature for `aarch64-unknown-fuchsia`](https://github.com/rust-lang/rust/pull/161886)
- [Some impls on `Box` have been generalised to arbitrary allocators, which may cause new type inference errors](https://github.com/rust-lang/rust/pull/161946)
- [The standard library now uses Unicode version 18.0.0](https://doc.rust-lang.org/stable/std/primitive.char.html#associatedconstant.UNICODE_VERSION)
- [WASI SDK version was bumped from 33 to 34](https://github.com/rust-lang/rust/pull/163809)
- [On ARM targets, `-Ctarget-feature`/`-Ctarget-cpu` values that would alter the ABI are rejected as hard errors now.](https://github.com/rust-lang/rust/pull/161280)

<a id="1.100.0-Internal-Changes"></a>

## Other

- [Test harness now allows passing `--test-threads` and `--color` multiple times, with later arguments overriding earlier ones](https://github.com/rust-lang/rust/pull/161312)


=== 1.99.1 published 2026-10-16
<a id="1.99.1"></a>

- [library: fix missing symbol `wcslen` on UEFI and embedded targets](https://github.com/rust-lang/rust/issues/163614)
- [rustc: fix miscompilation of FFI `bool` return values on x86\_64](https://github.com/rust-lang/rust/issues/163911)
- [rust-lld: add the rpath for `libLLVM` on macOS](https://github.com/rust-lang/rust/issues/163947)


=== 1.99.0 published 2026-10-01
<a id="1.99.0-Language"></a>

## Language

- [Add allow-by-default `raw_borrows_via_references` lint that checks for references that decay immediately into raw borrows](https://github.com/rust-lang/rust/pull/138230)
- [Extend `unconditional_panic` lint to function calls that panic when the chunks/windows size is zero](https://github.com/rust-lang/rust/pull/153563)
- [Stabilize C-variadic function definitions](https://github.com/rust-lang/rust/pull/155697)
- [Stabilize the ability to use `#[unsafe(naked)]` functions to define C-variadic functions (`#![feature(c_variadic_naked_functions)]`).](https://github.com/rust-lang/rust/pull/159746)
- [Trait methods are now resolved on an adjusted never type (producing a FCW)](https://github.com/rust-lang/rust/pull/156047)
- [Coerce from inference variables to trait objects if the inference variable is related via subtyping to a type that is known to be `Sized`](https://github.com/rust-lang/rust/pull/157820)
- [Stabilize `#[my_macro] mod foo;`](https://github.com/rust-lang/rust/pull/157857). This allows outlined modules (`mod foo;`) anywhere in the body of a custom attribute or derive macro.
- [Fix the `overflowing_literals` lint with repeated negation](https://github.com/rust-lang/rust/pull/158302). For instance, it will now no longer lint on `--128_i8`, which is already detected by the `arithmetic_overflow` lint.
- [Add POSIX symbols to the `invalid_runtime_symbol_definitions` and `suspicious_runtime_symbol_definitions` lints](https://github.com/rust-lang/rust/pull/158522)
- [Lint unused `#[path]` attributes on inline modules](https://github.com/rust-lang/rust/pull/158835)
- [Enable `unreachable_cfg_select_predicates` lint as part of `unused` lint group](https://github.com/rust-lang/rust/pull/159179)
- [Stabilize passing 128-bit integers via vector registers with `asm!` on x86](https://github.com/rust-lang/rust/pull/159525)
- [Explicitly document that some allocations are allowed to grow in-place (but none are allowed to shrink)](https://github.com/rust-lang/rust/pull/159729)
- We now [guarantee](https://github.com/rust-lang/rust/pull/159730) that the contents of an `UnsafeCell` can be accessed without going through `get`
  - [The `invalid_reference_casting` lint was adjusted accordingly](https://github.com/rust-lang/rust/pull/159960)
- [Account for globally enabled target features in `global_asm!`](https://github.com/rust-lang/rust/pull/160594)
- [Warn if an invalid `doc` attribute is used on a macro invocation](https://github.com/rust-lang/rust/pull/161003)

<a id="1.99.0-Compiler"></a>

## Compiler

- [Convert `-Ctarget-cpu` into a target-modifier for AVR, AMDGCN and NVPTX](https://github.com/rust-lang/rust/pull/150732)
- [Enable `static_position_independent_executables` on all gnu targets](https://github.com/rust-lang/rust/pull/158510)
- When providing a suggestion about a missing method, rustc now prefers an exactly matching name from a [doc alias attribute](https://doc.rust-lang.org/rustdoc/advanced-features.html#add-aliases-for-an-item-in-documentation-search) over a similarity search from other method names. If your new users sometimes expect a method under a different name, adding a doc alias will now help them find it via rustc suggestions, in addition to helping them find it via rustdoc search: [When suggesting method names, prefer *exact* doc aliases over similar names](https://github.com/rust-lang/rust/pull/160369)

<a id="1.99.0-Platform-Support"></a>

## Platform Support

- [Promote `riscv64-unknown-linux-musl` to Tier 2 with host tools](https://github.com/rust-lang/rust/pull/158766)

Refer to Rust's [platform support page](https://doc.rust-lang.org/rustc/platform-support.html) for more information on Rust's tiered platform support.

<a id="1.99.0-Libraries"></a>

## Libraries

- Iteration on `RangeInclusive` (`a..=b` ranges) is now [optimized better in some circumstances](https://github.com/rust-lang/rust/pull/155114). As a side effect of this, the behavior of `RangeInclusive` values that has already been exhausted (as an iterator) has changed. For example, the return values of `start()` and `end()` on such ranges may return different values, and using such ranges as slice indexes may have different behavior. These behaviors were not guaranteed to be stable, so these changes are considered to not be breaking changes.
- [Relax `transmute_copy` to accept `?Sized` types](https://github.com/rust-lang/rust/pull/155989)
- [Update `transmute_copy` to use a non-unwinding panic](https://github.com/rust-lang/rust/pull/155989)
- [Don't escape U+FF9E and U+FF9F in `escape_debug_ext`](https://github.com/rust-lang/rust/pull/158057)
- [Re-export `core::fmt::NumBuffer` in `alloc` (and `std`)](https://github.com/rust-lang/rust/pull/161430)

<a id="1.99.0-Stabilized-APIs"></a>

## Stabilized APIs

- [`IntoIterator` for `Box<[T; N]>`](https://doc.rust-lang.org/stable/std/iter/trait.IntoIterator.html#impl-IntoIterator-for-Box%3C%5BT;+N%5D,+A%3E)
- [`IntoIterator` for `&Box<[T; N]>`](https://doc.rust-lang.org/stable/std/iter/trait.IntoIterator.html#impl-IntoIterator-for-%26Box%3C%5BT;+N%5D,+A%3E)
- [`IntoIterator` for `&mut Box<[T; N]>`](https://doc.rust-lang.org/stable/std/iter/trait.IntoIterator.html#impl-IntoIterator-for-%26mut+Box%3C%5BT;+N%5D,+A%3E)
- [`VecDeque::retain_back`](https://doc.rust-lang.org/stable/std/collections/struct.VecDeque.html#method.retain_back)
- [`core::ffi::VaList`](https://doc.rust-lang.org/stable/core/ffi/struct.VaList.html)
- [`Box::into_non_null`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.into_non_null)
- [`Box::from_non_null`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.from_non_null)
- [`Vec::into_parts`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#method.into_parts)
- [`Vec::from_parts`](https://doc.rust-lang.org/stable/std/vec/struct.Vec.html#method.from_parts)
- [`core::mem::size_of_val_raw`](https://doc.rust-lang.org/stable/core/mem/fn.size_of_val_raw.html)
- [`core::mem::align_of_val_raw`](https://doc.rust-lang.org/stable/core/mem/fn.align_of_val_raw.html)
- [`core::alloc::Layout::for_value_raw`](https://doc.rust-lang.org/stable/core/alloc/struct.Layout.html#method.for_value_raw)
- [`String::from_utf8_lossy_owned`](https://doc.rust-lang.org/stable/std/string/struct.String.html#method.from_utf8_lossy_owned)
- [`string::FromUtf8Error::into_utf8_lossy`](https://doc.rust-lang.org/stable/std/string/struct.FromUtf8Error.html#method.into_utf8_lossy)
- [`FusedIterator for StepBy<I>`](https://doc.rust-lang.org/stable/std/iter/struct.StepBy.html#impl-FusedIterator-for-StepBy%3CI%3E)
- [`std::fs::set_times`](https://doc.rust-lang.org/stable/std/fs/fn.set_times.html)
- [`std::fs::set_times_nofollow`](https://doc.rust-lang.org/stable/std/fs/fn.set_times_nofollow.html)
- [`<LocalKey<Cell<T>>>::update`](https://doc.rust-lang.org/stable/std/thread/struct.LocalKey.html#method.update)

<a id="1.99.0-Cargo"></a>

## Cargo

- Add a new built-in profile `debug`. This is a preparation for transitioning the `dev` profile away from debugging to give a saner default for faster development iterations. Currently there is no difference between `dev` and `debug` profiles. [docs](https://doc.rust-lang.org/nightly/cargo/reference/profiles.html#debug-1) [\#17214](https://github.com/rust-lang/cargo/pull/17214)
- Workspace members on edition 2024 or later can now override an inherited workspace dependency's `default-features` field. For example, `serde = { workspace = true, default-features = false }` now turns off default features even when the workspace definition enables them. On earlier editions, `default-features = false` is ignored with a warning. ([RFC 3945](https://github.com/rust-lang/rfcs/pull/3945)) [\#17126](https://github.com/rust-lang/cargo/pull/17126)

See also the [full Cargo changelog](https://doc.rust-lang.org/nightly/cargo/CHANGELOG.html#cargo-199-2026-10-01)

<a id="1.99.0-Rustdoc"></a>

## Rustdoc

- [Add new `unused_footnote_definition` rustdoc lint](https://github.com/rust-lang/rust/pull/137858)
- Smarter filtering of trait impls yields performance improvements of 20% on average and up to 40% on some real-world crates. ([1](https://github.com/rust-lang/rust/pull/159623), [2](https://github.com/rust-lang/rust/pull/159721), [3](https://github.com/rust-lang/rust/pull/159779), [4](https://github.com/rust-lang/rust/pull/159854), [5](https://github.com/rust-lang/rust/pull/159091))

<a id="1.99.0-Compatibility-Notes"></a>

## Compatibility Notes

- [Fully deprecate the legacy integral modules](https://github.com/rust-lang/rust/pull/146882). For example, `std::i32::MAX` should be accessed via `i32::MAX` instead.
- [Upgrade `no_mangle_generic_items` into hard error](https://github.com/rust-lang/rust/pull/154585)
- [The `Pin::new_unchecked` has had its safety invariants changed slightly](https://github.com/rust-lang/rust/pull/156935)
- [Do not promote references to extern statics](https://github.com/rust-lang/rust/pull/157641)
- [Ensure that the inferred types of `let` patterns typecheck](https://github.com/rust-lang/rust/pull/157841)
- [hermit/fs: Return `unsupported()` instead of `from_raw_os_error(22)`](https://github.com/rust-lang/rust/pull/158247)
- [Fixed a bug where `#[repr(simd)]` was accidentally allowed on macro invocations on stable Rust](https://github.com/rust-lang/rust/pull/158523)
- [Abort const-eval when there are generics in the type of the value being produced](https://github.com/rust-lang/rust/pull/159504)
- [Attributes not applying to anything are now an error in code blocks in doc comments](https://github.com/rust-lang/rust/pull/159849)
- [`Box::leak`: tell people to avoid unleaking](https://github.com/rust-lang/rust/pull/160323)
- [PowerPC inline ASM: Fix scalar floats being in the wrong vector lane on little endian](https://github.com/rust-lang/rust/pull/160441)
- [Do not take `doc(cfg())` into account when filtering doctests](https://github.com/rust-lang/rust/pull/159014)
- [Infer anonymous lifetimes in the types of associated consts as `'static`](https://github.com/rust-lang/rust/pull/156508)
- Macros that expand to a semicolon now produce a warning lint (`semicolon_in_expressions_from_non_local_macros`) even when the macro comes from another crate. Previously, such warnings only appeared for macros from the same crate, to avoid showing warnings that can't be fixed locally; however, this masked problems, as integration tests from the crate providing the macro get compiled as a separate crate, so tests often wouldn't reveal this issue. If you encounter a lint like this, please make sure to report it to the crate providing the macro so they can fix it; don't just silence it in your own crate.
  - [`semicolon_in_expressions_from_macros`: Lint on non-local macros too](https://github.com/rust-lang/rust/pull/159222)
  - [Split non-local `semicolon_in_expressions_from_macros` into a separate lint](https://github.com/rust-lang/rust/pull/159700)
- In Cargo, incremental compilation is now disabled by default when running in CI. CI is detected via the `CI` environment variable. [\#17220](https://github.com/rust-lang/cargo/pull/17220)
- [The Rust Reference no longer recommends using a single pattern to match a union alongside another value, such as in a manually-written tagged union](https://github.com/rust-lang/reference/pull/2303). This was because it was found that such code would, in some circumstances, result in the compiler reading the contents of the union before checking if the rest of the scrutinee matches the rest of the pattern. This can cause undefined behavior in code similar to what the reference previously recommended.

<a id="1.99.0-Internal-Changes"></a>

## Internal Changes

These changes do not affect any public interfaces of Rust, but they represent significant improvements to the performance or internals of rustc and related tools.

- [Update to LLVM 23](https://github.com/rust-lang/rust/pull/158734)


=== 1.98.1 published 2026-09-03
<a id="1.98.1"></a>

- [rustc: fix miscompilation in generating vtables](https://github.com/rust-lang/rust/issues/161441)


=== 1.98.0 published 2026-08-20
<a id="1.98.0-Language"></a>

## Language

- [Allow shortening lifetime of `&mut` when unsize-coercing, even in an invariant position.](https://github.com/rust-lang/rust/pull/149219) For example, you can now coerce a `Cell<&'long mut i32>` to a `Cell<&'short mut dyn Send>`. Such shortenings were already previously allowed when coercing a `&mut` to a `&`, or coercing a `&` to a `&`.
- [Add deny-by-default `invalid_runtime_symbol_definitions` lint and warn-by-default `suspicious_runtime_symbol_definitions` lint](https://github.com/rust-lang/rust/pull/155521)
  - The lints currently specifically targets `core` runtime symbols like `memcmp`, `memset`, `strlen`, ... and is planned to be expanded in the next few releases.
- [Add warn-by-default `c_void_returns` lint to check `core::ffi::c_void` as a return type](https://github.com/rust-lang/rust/pull/156379)

<a id="1.98.0-Platform-Support"></a>

## Platform Support

- [Add `powerpc64-unknown-linux-gnuelfv2` as Tier 3](https://github.com/rust-lang/rust/pull/144220)
- [Add `aarch64-unknown-linux-pauthtest` as Tier 3 target](https://github.com/rust-lang/rust/pull/155722)
- [Promote `thumbv7a-none-eabi` to Tier 2](https://github.com/rust-lang/rust/pull/155763)
- [Promote `thumbv7a-none-eabihf` to Tier 2](https://github.com/rust-lang/rust/pull/155763)
- [Promote `thumbv7r-none-eabi` to Tier 2](https://github.com/rust-lang/rust/pull/155763)
- [Promote `thumbv7r-none-eabihf` to Tier 2](https://github.com/rust-lang/rust/pull/155763)
- [Promote `thumbv8r-none-eabihf` to Tier 2](https://github.com/rust-lang/rust/pull/155763)

Refer to Rust's [platform support page](https://doc.rust-lang.org/rustc/platform-support.html) for more information on Rust's tiered platform support.

<a id="1.98.0-Libraries"></a>

## Libraries

- [Change `Location<'_>` lifetime to `'static` in `Panic[Hook]Info`](https://github.com/rust-lang/rust/pull/146561)
- [Document panic in `RangeInclusive::from(legacy::RangeInclusive)`](https://github.com/rust-lang/rust/pull/155421)
- [Document that `ManuallyDrop`'s `Box` interaction has been fixed](https://github.com/rust-lang/rust/pull/155750)
- [Stabilize LoongArch CRC Intrinsics](https://github.com/rust-lang/rust/issues/156908)
- [The `derive` macro is available at `{core,std}::derive`.](https://github.com/rust-lang/rust/issues/154645) This was previously [unintentionally stabilized in 1.96](https://github.com/rust-lang/rust/issues/159856), but is now [explicitly accepted](https://github.com/rust-lang/rust/issues/154645) as a stabilized API.
  - Please note that the MSRV for `{core,std}::derive` will be 1.96, and not 1.98.

<a id="1.98.0-Stabilized-APIs"></a>

## Stabilized APIs

- [`str::substr_range`](https://doc.rust-lang.org/stable/std/primitive.str.html#method.substr_range)
- [`[T]::subslice_range`](https://doc.rust-lang.org/stable/std/primitive.slice.html#method.subslice_range)
- [`core::fmt::NumBuffer`](https://doc.rust-lang.org/stable/core/fmt/struct.NumBuffer.html)
- [`<{integer}>::format_into`](https://doc.rust-lang.org/stable/core/primitive.usize.html#method.format_into)
- [`Send/Sync for std::process::CommandArgs`](https://doc.rust-lang.org/stable/std/process/struct.CommandArgs.html#impl-Send-for-CommandArgs%3C'a%3E)
- [`{fN}::algebraic_add`](https://doc.rust-lang.org/stable/core/primitive.f32.html#method.algebraic_add)
- [`{fN}::algebraic_sub`](https://doc.rust-lang.org/stable/core/primitive.f32.html#method.algebraic_sub)
- [`{fN}::algebraic_mul`](https://doc.rust-lang.org/stable/core/primitive.f32.html#method.algebraic_mul)
- [`{fN}::algebraic_div`](https://doc.rust-lang.org/stable/core/primitive.f32.html#method.algebraic_div)
- [`{fN}::algebraic_rem`](https://doc.rust-lang.org/stable/core/primitive.f32.html#method.algebraic_rem)
- [`NonZero<{integer}>::from_str_radix`](https://doc.rust-lang.org/stable/core/num/struct.NonZero.html#method.from_str_radix-4)
- [`String::from_utf16le`](https://doc.rust-lang.org/stable/std/string/struct.String.html#method.from_utf16le)
- [`String::from_utf16le_lossy`](https://doc.rust-lang.org/stable/std/string/struct.String.html#method.from_utf16le_lossy)
- [`String::from_utf16be`](https://doc.rust-lang.org/stable/std/string/struct.String.html#method.from_utf16be)
- [`String::from_utf16be_lossy`](https://doc.rust-lang.org/stable/std/string/struct.String.html#method.from_utf16be_lossy)
- [`[T]::strip_circumfix`](https://doc.rust-lang.org/stable/core/primitive.slice.html#method.strip_circumfix)
- [`str::strip_circumfix`](https://doc.rust-lang.org/stable/core/primitive.str.html#method.strip_circumfix)
- [`Atomic<T>::from_mut`](https://doc.rust-lang.org/stable/core/sync/atomic/struct.Atomic.html#method.from_mut)
- [`Atomic<T>::get_mut_slice`](https://doc.rust-lang.org/stable/core/sync/atomic/struct.Atomic.html#method.get_mut_slice)
- [`Atomic<T>::from_mut_slice`](https://doc.rust-lang.org/stable/core/sync/atomic/struct.Atomic.html#method.from_mut_slice)
- [`std::range::legacy`](https://doc.rust-lang.org/stable/std/range/legacy/index.html)
- [`bool::ok_or`](https://doc.rust-lang.org/stable/std/primitive.bool.html#method.ok_or)
- [`bool::ok_or_else`](https://doc.rust-lang.org/stable/std/primitive.bool.html#method.ok_or_else)
- [`Option::map_or_default`](https://doc.rust-lang.org/stable/std/option/enum.Option.html#method.map_or_default)
- [`Result::map_or_default`](https://doc.rust-lang.org/stable/std/result/enum.Result.html#method.map_or_default)
- [`Box::as_ptr`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.as_ptr)
- [`Box::as_mut_ptr`](https://doc.rust-lang.org/stable/std/boxed/struct.Box.html#method.as_mut_ptr)
- [`Path::is_empty`](https://doc.rust-lang.org/stable/std/path/struct.Path.html#method.is_empty)
- [`PathBuf::into_string`](https://doc.rust-lang.org/stable/std/path/struct.PathBuf.html#method.into_string)
- [`arch::{arm,aarch64}::vdot*`: NEON dot product intrinsics](https://github.com/rust-lang/rust/issues/117224)

<a id="1.98.0-Compatibility-Notes"></a>

## Compatibility Notes

- [If fully elided, lifetime bounds of trait object types may now resolve differently or even get rejected in very specific niche scenarios](https://github.com/rust-lang/rust/pull/129543)
- [Error in more cases of ambiguous imports](https://github.com/rust-lang/rust/pull/145108)
- [Switch the destructors implementation for thread locals on Windows to use Fiber Local Storage (FLS)](https://github.com/rust-lang/rust/pull/148799)
- [Convert some cases of the `ambiguous_glob_imports` lint into a hard error](https://github.com/rust-lang/rust/pull/149195)
- [Where-bounds of the form `Type = Type` and `Type == Type` are no longer syntactically allowed](https://github.com/rust-lang/rust/pull/153513)
- [Ensure Send/Sync is not implemented for std::env::Vars{,Os}](https://github.com/rust-lang/rust/pull/155153)
- [Fix that in some attributes, arguments were not properly rejected](https://github.com/rust-lang/rust/pull/155193)
- [`repr(transparent)` is now more strict about which fields have "trivial" layout and hence can be ignored: `repr(C)` types, types with private fields, and `#[non_exhaustive]` types are no longer considered "trivial"](https://github.com/rust-lang/rust/pull/155299)
- [Correctly check whether types have equal size in `transmute()` when some `repr` attributes are involved.](https://github.com/rust-lang/rust/pull/155418)
- [More characters are escaped when printing strings and chars](https://github.com/rust-lang/rust/pull/155527)
- [Implement fast path for `derive(PartialOrd)` when deriving `Ord`](https://github.com/rust-lang/rust/pull/155598) This can break crates in practice where a type's PartialOrd and Ord impls were inconsistent with each other.
- [Add temporary scope to `assert_eq` and `assert_ne`](https://github.com/rust-lang/rust/pull/155739)
- Closed a hole in the pattern matching [structural equality](https://doc.rust-lang.org/reference/patterns.html#constant-patterns) check, preventing cases where a match of a constant would be allowed, despite disagreeing with a manually written `PartialEq` implementation, when a `derive(PartialEq)` implementation for that type also exists.
- [On Emscripten the WASM exception handling ABI is now unconditionally used](https://github.com/rust-lang/rust/pull/156928) The `-Zemscripten-wasm-eh=false` flag to switch back to JS exceptions has been removed.
- [The UNSAFE\_CODE lint is now consistently emitted for all unsafe attributes](https://github.com/rust-lang/rust/pull/157201)
- [Solaris: remove `File::lock` implementation, it has the wrong semantics (return "unsupported" instead)](https://github.com/rust-lang/rust/pull/157509)
- [Windows-gnu targets now specify baseline tools versions](https://github.com/rust-lang/rust/pull/158020)
- [rustfmt now discovers module files that are defined in `cfg_select!`](https://github.com/rust-lang/rust/pull/158372) This may cause more code to be formatted which was previously ignored.


=== 1.97.1 published 2026-07-16
<a id="1.97.1"></a>

- [rustc: Fix miscompilation in LLVM optimization](https://github.com/rust-lang/rust/issues/159035) This backports an LLVM submodule bump to include the LLVM-side fix and a revert of the rustc change that is one known trigger for the bug. The rustc side revert should not be strictly necessary but is done out of abundance of caution.




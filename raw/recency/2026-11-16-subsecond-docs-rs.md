https://docs.rs/subsecond/latest/subsecond/
2026-11-16

### Expand description

## §Subsecond: Hot-patching for Rust

Subsecond is a library that enables hot-patching for Rust applications. This allows you to change the code of a running application without restarting it. This is useful for game engines, servers, and other long-running applications where the typical edit-compile-run cycle is too slow.

Subsecond also implements a technique we call “ThinLinking” which makes compiling Rust code significantly faster in development mode, which can be used outside of hot-patching.

## §Usage

Subsecond is designed to be as simple for both application developers and library authors.

Simply call your existing functions with

```
call
```

and Subsecond will automatically detour
that call to the latest version of the function.

```
```
for x in 0..5 {
    subsecond::call(|| {
        println!("Hello, world! {}", x);
    });
}
```
```

To actually load patches into your application, a third-party tool that implements the Subsecond compiler and protocol is required. Subsecond is built and maintained by the Dioxus team, so we suggest using the dioxus CLI tool to use subsecond.

To install the Dioxus CLI, we recommend using

```
cargo binstall
```

:

```
```
cargo binstall dioxus-cli
```
```

The Dioxus CLI provides several tools for development. To run your application with Subsecond enabled,
use

```
dx serve
```

- this takes the same arguments as

```
cargo run
```

but will automatically hot-reload your
application when changes are detected.

As of Dioxus 0.7, “–hotpatch” is required to use hotpatching while Subsecond is still experimental.

```
```
dx serve --hotpatch
```
```

### §How it works

Subsecond works by detouring function calls through a jump table. This jump table contains the latest version of the program’s function pointers, and when a function is called, Subsecond will look up the function in the jump table and call that instead.

Unlike libraries like detour, Subsecond does not modify your process memory. Patching pointers is wildly unsafe and can lead to crashes and undefined behavior.

Instead, an external tool compiles only the parts of your project that changed, links them together using the addresses of the functions in your running program, and then sends the new jump table to your application. Subsecond then applies the patch and continues running. Since Subsecond doesn’t modify memory, the program must have a runtime integration to handle the patching.

If the framework you’re using doesn’t integrate with subsecond, you can rely on the fact that calls
to stale

```
call
```

instances will emit a safe panic that is automatically caught and retried
by the next

```
call
```

instance up the callstack.

Subsecond is only enabled when debug\_assertions are enabled so you can safely ship your application with Subsecond enabled without worrying about the performance overhead.

### §Workspace support

Subsecond currently only patches the “tip” crate - ie the crate in which your

```
main.rs
```

is located.
Changes to crates outside this crate will be ignored, which can be confusing. We plan to add full
workspace support in the future, but for now be aware of this limitation. Crate setups that have
a

```
main.rs
```

importing a

```
lib.rs
```

won’t patch sensibly since the crate becomes a library for itself.

This is due to limitations in rustc itself where the build-graph is non-deterministic and changes to functions that forward generics can cause a cascade of codegen changes.

### §Globals, statics, and thread-locals

Subsecond does support hot-reloading of globals, statics, and thread locals. However, there are several limitations:

* You may add new globals at runtime, but their destructors will never be called.
* Globals are tracked across patches, but renames are considered to be new globals.
* Changes to static initializers will not be observed.

Subsecond purposefully handles statics this way since many libraries like Dioxus and Tokio rely on persistent global runtimes.

HUGE WARNING: Currently, thread-locals in the “tip” crate (the one being patched) will seemingly reset to their initial value on new patches. This is because we don’t currently bind thread-locals in the patches to their original addresses in the main program. If you rely on thread-locals heavily in your tip crate, you should be aware of this. Sufficiently complex setups might crash or even segfault. We plan to fix this in the future, but for now, you should be aware of this limitation.

### §Struct layout and alignment

Subsecond currently does not support hot-reloading of structs. This is because the generated code assumes a particular layout and alignment of the struct. If layout or alignment change and new functions are called referencing an old version of the struct, the program will crash.

To mitigate this, framework authors can integrate with Subsecond to either dispose of the old struct or to re-allocate the struct in a way that is compatible with the new layout. This is called “re-instancing.”

In practice, frameworks that implement subsecond patching properly will throw out the old state and thus you should never witness a segfault due to misalignment or size changes. Frameworks are encouraged to aggressively dispose of old state that might cause size and alignment changes.

We’d like to lift this limitation in the future by providing utilities to re-instantiate structs, but for now it’s up to the framework authors to handle this. For example, Dioxus apps simply throw out the old state and rebuild it from scratch.

### §Pointer versioning

Currently, Subsecond does not “version” function pointers. We have plans to provide this metadata
so framework authors can safely memoize changes without much runtime overhead. Frameworks like
Dioxus and Bevy circumvent this issue by using the TypeID of structs passed to hot functions as
well as the

```
ptr_address
```

method on

```
HotFn
```

to determine if the function pointer has changed.

Currently, the

```
ptr_address
```

method will always return the most up-to-date version of the function
even if the function contents itself did not change. In essence, this is equivalent to a version
of the function where every function is considered “new.” This means that framework authors who
integrate re-instancing in their apps might dispose of old state too aggressively. For now, this
is the safer and more practical approach.

### §Nesting Calls

Subsecond calls are designed to be nested. This provides clean integration points to know exactly where a hooked function is called.

The highest level call is

```
fn main()
```

though by default this is not hooked since initialization code
tends to be side-effectual and modify global state. Instead, we recommend wrapping the hot-patch
points manually with

```
call
```

.

```
```
fn main() {
    // Changes to the `for` loop will cause an unwind to this call.
    subsecond::call(|| {
        for x in 0..5 {
            // Changes to the `println!` will be isolated to this call.
            subsecond::call(|| {
                println!("Hello, world! {}", x);
            });
        }
   });
}
```
```

The goal here is to provide granular control over where patches are applied to limit loss of state when new code is loaded.

### §Applying patches

When running under the Dioxus CLI, the

```
dx serve
```

command will automatically apply patches when
changes are detected. Patches are delivered over the Dioxus Devtools
websocket protocol and received by corresponding websocket.

If you’re using Subsecond in your own application that doesn’t have a runtime integration, you can
build an integration using the

```
apply_patch
```

function. This function takes a

```
JumpTable
```

which
the dioxus-cli crate can generate.

To add support for the Dioxus Devtools protocol to your app, you can use the dioxus-devtools
crate which provides a

```
connect
```

method that will automatically apply patches to your application.

Unfortunately, one design quirk of Subsecond is that running apps need to communicate the address
of

```
main
```

to the patcher. This is due to a security technique called ASLR
which randomizes the address of functions in memory. See the subsecond-harness and subsecond-cli
for more details on how to implement the protocol.

### §ThinLink

ThinLink is a program linker for Rust that is designed to be used with Subsecond. It implements the powerful patching system that Subsecond uses to hot-reload Rust applications.

ThinLink is simply a wrapper around your existing linker but with extra features:

* Automatic dynamic linking to dependencies
* Generation of Subsecond jump tables
* Diffing of object files for function invalidation

Because ThinLink performs very to little actual linking, it drastically speeds up traditional Rust development. With a development-optimized profile, ThinLink can shrink an incremental build to less than 500ms.

ThinLink is automatically integrated into the Dioxus CLI though it’s currently not available as a standalone tool.

### §Limitations

Subsecond is a powerful tool but it has several limitations. We talk about them above, but here’s a quick summary:

* Struct hot reloading requires instancing or unwinding
* Statics are tracked but not destructed

### §Platform support

Subsecond works across all major platforms:

* Android (arm64-v8a, armeabi-v7a)
* iOS (arm64)
* Linux (x86\_64, aarch64)
* macOS (x86\_64, aarch64)
* Windows (x86\_64, arm64)
* WebAssembly (wasm32)

If you have a new platform you’d like to see supported, please open an issue on the Subsecond repository. We are keen to add support for new platforms like wasm64, riscv64, and more.

Note that iOS device is currently not supported due to code-signing requirements. We hope to fix this in the future, but for now you can use the simulator to test your app.

### §Adding the Subsecond badge to your project

If you’re a framework author and want your users to know that your library supports Subsecond, you can add the Subsecond badge to your README! Users will know that your library is hot-reloadable and can be used with Subsecond.

```
```
[![Subsecond](https://img.shields.io/badge/Subsecond-Enabled-orange)](https://crates.io/crates/subsecond)
```
```

### §License

Subsecond and ThinLink are licensed under the MIT license. See the LICENSE file for more information.

### §Supporting this work

Subsecond is a project by the Dioxus team. If you’d like to support our work, please consider sponsoring us on GitHub or eventually deploying your apps with Dioxus Deploy (currently under construction).

## Structs§

* HotFn
* A hot-reloadable function.
* HotFnPanic
* A panic issued by the

  ```
  call
  ```

  function if the caller would be stale if called. This causes an unwind to the next

  ```
  call
  ```

  instance that can properly handle the panic and retry the call.
* HotFnPtr
* A pointer to a hot patched function
* JumpTable

## Enums§

## Traits§

* HotFunction
* A trait that enables types to be hot-patched.

## Functions§

* apply\_patch⚠
* Apply the patch using a given jump table.
* call
* Call a given function with hot-reloading enabled. If the function’s code changes,

  ```
  call
  ```

  will use the new version of the function. If code above the function changes, this will emit a panic that forces an unwind to the next

  ```
  call
  ```

  instance.
* get\_jump\_⚠table
* Get the current jump table, if it exists.
* register\_handler
* Register a function that will be called whenever a patch is applied.

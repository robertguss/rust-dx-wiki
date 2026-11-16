https://raw.githubusercontent.com/DioxusLabs/dioxus/main/packages/subsecond/README.md
2026-11-16

# Subsecond
Subsecond is a hot-reloading library for Rust. It makes it easy to add Rust hot-reloading to your
existing Rust project with minimal integration overhead.
## Usage:
For library authors you can use "hot" functions with the `subsecond::current` function:
```rust
/// A user-facing tick / launch / start function
///
/// Typically this will be a request/response handler, a game loop, a main function, callback, etc
///
/// `current` accepts function pointers and Fn types
pub fn tick(handler: Fn(Request) -> Response) {
// Create a "hot" function that we can inspect
let hot\_fn = subsecond::current(handler);
// Check if this function has been patched
if hot\_fn.changed() {
// do thing
}
// Register a handler to be called when the function is patched
hot\_fn.on\_changed(|| /\* do thing \*/);
// Call the hot function
hot\_fn.call((request))
}
```
For application authors, you can use `subsecond::call()` to make a function hot-reloadable:
```rust
fn handle\_request(request: Request) -> Response {
subsecond::call(|| {
// do\_thing...
})
}
```
If a hot function is actively being called, then subsecond will rewind the stack to the "cleanest" entrypoint. For example, a hot-reloadable server will have two "hot" points: at the start of the server, and at the start of the request handler. When the server is reloaded, subsecond will rewind the stack to the first hot point, and then call the function again.
```rust
// Changes to `serve` will reload the server
fn serve() {
let router = Router::new();
router.get("/", handle\_request);
router.serve("0.0.0.0:8080");
}
// Changes below "handle\_request" won't be reload the router
fn handle\_request(request: Request) -> Response {
// do thing
}
```
Framework authors can interleave their own hot-reload entrypoints alongside user code. This lets you add new anchors into long-running stateful code:
```rust
fn main() {
// serve is "hot" and will rebuild the router if it changes
webserver::serve("0.0.0.0:8080", || {
Router::new()
// get is "hot" and changes to handle\_request won't rebuild the router
.get("/", |req| Response::websocket(handle\_socket))
})
}
fn handle\_socket(ws: &WebSocket) {
subsecond::call(|| {
// do things with the websocket
})
}
```

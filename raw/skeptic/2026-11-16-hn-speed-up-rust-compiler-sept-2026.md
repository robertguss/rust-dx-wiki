https://news.ycombinator.com/item?id=49920896
2026-11-16

title: How to speed up the Rust compiler in September 2026 | Hacker News
published_date: None
final_url: https://news.ycombinator.com/item?id=49920896

Funny to see this now. I’ve got a private branch I am in the process of shaping up this weekend to show the compiler team. For deep nested projects like rust analyzer, if you emit the meta data about function types earlier for downstream slots to use, before successful type checking, you can start other crates earlier and use all the slots you have instead of sitting around waiting for the full type checking of the bodies (which other crates largely don’t care about). Something like 40% wall time speed up, maybe 10% to 15% if you have the parallel frontend on.

Nice, excited to see that. This is basically deeper pipelining, IIUC. Nick (the author of the blog) implemented the current version of this "emit metadata sooner," optimization and already experimented with pushing it even sooner a while back.

We have discussed this briefly on last All Hands, the problem will probably be dealing with compiler errors, when they happen in builds that already emitted metadata. I believe this was the reason why it wasn't merged in the first place.

Yes I think I read a post of his from like 2019 were something was tried like this before. My guess is that this will be an interesting and hopefully informative PR for you all to see, but will likely not be merged as is. I had to add the ability for rustc to pause after early meta data emission and that was hacked together I feel, not well designed per se.

I view this as speculative execution/compilation and just throw out any errors from a crate that depended on another crate that ultimately errors out. It has the same outcome (same errors are printed in both cases) you just have a chance of having totally wasted some cpu time (that was otherwise just sitting around though).

Sounds lovely, give it a try on the codex-rs which seems to be getting close to using 2K crates in their repository any time now. Takes like 30 minutes to compile on a my beefy machine and it's a goddamn TUI, not sure what's going on, and not too interested in diving into that beast either.

It has 1.8 million lines of rust. That compilation time seems close to what I'd expect at that size. If you want something faster you should focus on distributed build caching rather than speeding up the compiler. Also note that crates are effectively equivalent to a single file in c++ as it's the compilation unit. This is similar to compiling 2k files that average 1k loc each in c++. I'm sure it's much worse when you account for macro expansion and generics.

As they say, it's a damn TUI for a chat bot. 1.8 MLoC is like 50x what you'd expect from something like that. If you want to speed up compilation, reducing that absolutely insane bloat would be a good start

> If you want something faster you should focus on distributed build caching rather than speeding up the compiler

... But the whole point is that that project is big, unwieldy and has lots of crates, both their own and 3rd party. Slapping a cache in front of it kind of defeats the purpose here, to see how parent's thing would speed things up for really large projects.

Sure, that compiles in a few minutes for me too, give it a try with a release build and compiling the full workspace though, since the point here is to stress the compiler :)

If there's a project that takes 45 minutes to produce a debug build from scratch, that's not a Rust problem, that's a them problem.

Let's compare. I just checked out ripgrep and built it and all its dependencies from scratch. Total time to produce a debug build: 6.92 seconds. This is inside a 16GB VM on a random Linux laptop (on battery); no beefy hardware here.

Let's try something beefier. I just checked out uutils (an implementation of coreutils) and built it from scratch. Total time to produce debug builds, for eighty binaries and all their dependencies: 30.26 seconds.

Let's try something beefier. I just checked out Servo, an entire browser engine, and built it and all its dependencies from scratch. Total time to build and link its one-thousand one-hundred and ten compilation units (along with its infamously huge and serial servo-script bottleneck) into a binary: 4 minutes and 38 seconds.

If Codex takes 45 minutes to build from scratch, that's an indictment of OpenAI and their development processes.

Arguably it is a rust problem. Rust can be improved to reduce the need to do as much manual maintenance of crates dynamics to allow for faster build times. The "you're holding it wrong" answer is not a good perspective to apply and I am surprised to see a prominent member of the rust community using it.

No, one can write pathological code in any language. I welcome efforts to improve the performance of the Rust compiler, but nobody is served by optimizing for degenerate use cases to the detriment of legitimate use cases. It is, in fact, possible to hold it wrong; this isn't blithe dismissiveness, but rather an accurate statement of reality, and pretending otherwise doesn't lead to a better language.

I feel like there is an assumption here that solving the problems described will result in a worse outcome for the average rust user, but I'm not sure that's the case. Perhaps the existing way of compilation makes sense for release mode, but a different tact could be taken for compilation modes which are optimized for developer productivity.

I agree with the sentiment that you can't solve for everyone, but if a problem is prevelant in your userbase, it's worth optimizing for solving it. Not every tool will be used the way it was designed to be used.

I've abandoned zig for rust. I expected to be annoyed by rust build times, but so far it's been quite good for my needs. To the contrary it has not been any impediment even when prost etc all drag in many deps from a cold build.

The zig compiler apart from a couple of cross build or linker issues is darn good. Switch to rust is a function of library support, private struct fields. Rust itself is better organized and far better documented compared to zig.

However, rust has got to get their allocators for container support straightened out soon. I do SAAS for fintech and low level packet transports. Both benefit greatly with allocators custom designed for job at hand.

The allocator API has been stabilized, to be released in Rust 1.100 in November. (Though only Vec and Box will support custom allocators immediately; the rest of the standard library collections are coming later.)

> Incremental compilation is not cleaned up. Older deps pile up and don’t get cleaned.

This is one of those problems that’s both huge/important, and probably impossible to solve. It bites me all the time, I have a measly 1TB nvme disk and I basically have to wipe my target directory and docker build cache (I have a shared cargo cache volume across builds) every other day. I’ve had this workstation for 2.5 years now and I’m honestly worried about nand endurance coming to bite me soon.

How would one even solve this? When do you know a cache entry won’t be used any more? Trace back provenance of artifacts to their sources, and if the mtimes have been bumped just delete the artifacts? It’s not like resetting source files to older mtimes is a good idea anyway…

I disagree it’s impossible to solve. Huge C++ projects don’t have continuously growing build directories and can still compile incrementally correctly.

That’s because they overwrite the old artifacts with new ones every time, which has its own problems: you could end up reusing stale artifacts if your compiler version changes, or if different compiler args are used for the same artifact, and a bunch of other stuff. Rust computes a digest of all the relevant build environment settings that may need a different artifact to be built, and uses that digest in the file name. That means you basically never have issues like “oh crap the incremental build broke, do a clean build instead”. (Amongst a whole lot of other benefits I’m sure.)

But this technique errs on the side of not using invalid artifacts, at the cost of not having a good system for expiring them. To maintain the goal of never having to worry about when to require a clean rebuild, solving cleaning of stale artifacts becomes a much harder problem.

> It’s insane. 45 minutes to build debug from scratch. Linking is super slow even in debug and that’s without LTO.

How much memory do you have, and do you have swap turned on?

I have 32GB of RAM, and it barely manages to build release if I shut down everything else on the system that uses RAM. 64GB would be better. If you have 32GB or less and you have swap on, the performance might be mostly because you're spending a lot of time swapping. And that's for release; debug on a repo that size may spend a lot of time and memory linking debug info.

I will email you when I have something up for sure! First cargo check has it at about 28% reduced on codex rs, from 383 seconds down to 277 seconds on a 16 core machine. No -Zthreads yet though, and that typically has a similar effect and reduces the speed up the early meta data gives.

Depends on what you are editing I would say, if it's something deeper in the stack then it should help. The last numbers I have is that this is a 6-8% improvement for incremental editing of the code for cargo itself, but I'm having the benchmark be rerun now, as I've landed a fair amount of changes since then.

I'm glad to see the donations from big companies to open source maintainers are making measurable difference to the Rust experience. Telling these companies that their employees spend 5% less time waiting for compilation might motivate future investment in people like Nick and the others mentioned.

I finally gave in to the rust hype and built a new project in it (or my agent fleet did). Almost instant regret. My poor machine with just 2TB HDD and 24 cores was almost immediately crippled by agents each working in their own sandbox, each one building and compiling

Most projects my fleet works on are in other languages (TS, Go, Elixir) and can comfortably handle 10+ agents working in parallel, but not rust. I had to cap the fleet to 5 workers and build a dedicated resource monitor to step in and tidy up every time the disk almost filled up

That and general progress on building is far slower, with far more time spent building and testing than any other language I use.

Ended up rebuilding in Go, the perf gains weren't worth it

You should have set up https://github.com/mozilla/sccache at minimum. Setting up compiler caching is routine for people coming from older compiled language backgrounds but it's often missed by people coming from languages like JS/TS who have never been exposed to these ideas.

There's a new project called kache https://github.com/kunobi-ninja/kache that takes this even further and handles more edge cases with worktrees, but it's newer.

If you were pulling the entire project fresh and rebuilding everything in every worktree all the time without any caching then it would be frustrating. You could have asked your agent to set up basic caching and solved most of your problem in minutes.

Cargo could definitely improve with some inter-project sharing by default, but simultaneously working with a bunch of workspaces of the same project is a very new phenomena...

You really shouldn't build software with rust if your workflow involves 10+ agents. Why aren't you using Python or Typescript for things like that?

Rust is what you use when you want to maximize on the runtime performance. It will build software that requires significantly less memory and maximize the CPU that will save time and energy. It's a system language for writing software meant to access the hardware.

A couple recs for sccache, which is great, but I upgraded to mbx (https://github.com/jdx/mr-boxington/) which goes beyond sccache by wrapping cargo to give you better rust-specific management, including incremental compilation.

I've moved from Rust to Go for most things because in the era of agents, being able to iterate quickly on a project is a huge advantage and Rust is way, way slower than Go for compilation. There are times when Rust is more appropriate, but for the vast majority of things Go is perfectly fine.

Checked out your GitHub profile. This is an insane amount of LLM usage. You created 7 full-blown apps, and each of them is very recent. The earliest commit was only 2 days ago.

I'm normally against fully vibe-coded apps, but at this point, I'm just impressed.

Be impressed when professionals actually test them and find them competitive. Maybe these apps are good, maybe they aren't, absent real data just being vibe-coded doesn't imply quality and a claim like "I one-shotted Photoshop" should cause alarm even if you're all in on GenAI.

At some point we have to move on from amazement at what these models can do to actually caring about the quality of the product.

btw. That could actually make it slower to compile. The compiler uses the orphan rule to short circuit some checks IIRC.

Nevertheless, people in the project are trying to figuring out a way to relax the rule while still maintaining coherence, so this might happen some day.

there are good reasons, obviously, but it's my #1 PITA, #2 is comptime type introspection (it looks like @yara-blue is making some progress, so fingers crossed)

Rust doesn't let you write an impl a trait that wasn't declared in your crate for a type that wasn't declared in your crate. At least one of the two needs to be locally declared. This makes splitting projects into multiple crates harder than it could be, but on the other hand it makes the crates ecosystem less brittle than it otherwise would be.

Some people propose relaxing this rule for "workspaces" (local projects with multiple crates that are not published individually). I haven't researched whether that would be technically feasible.

If you built two impls, your compiler wouldn't know which to pick. Or to phrase it differently, if you wanted to be able to choose the right one, it wouldn't be 'orphan impls', it would be 'orphan impls plus some selection mechanism'. E.g. Scala implicits. And once you have Scala implicits, non-orphan impls probably start looking like a pretty sweet alternative!

Very cool projects! I agree, desktop apps are one of the areas that Rust beats Go. It's too bad though, since I feel anything with a heavy GUI like this can benefit from a rapid iteration cycle which is painful with Rust.

It is right there in the 5 GL language, unless you want to convince us that all your PR come with the corresponding Assembly that the compiler generated, while doing all the compiler passes with PhD level knowledge from everyone that has worked in LLVM since 2003.

> because in the era of agents, being able to iterate quickly on a project is a huge advantage and Rust is way, way slower than Go for compilation.

Incremental changes in a normal project shouldn’t cause massive compile times. Even for my large projects, the compile times are trivial compared to the duration of an LLM turn.

Very large projects should be broken into logical modules so only the changed part is incrementally compiled. If linking is taking a long time there are alternate linkers that can be used.

If you’re using work trees a lot, set up compiler caching to avoid rebuilding everything from zero on every new work tree is important.

I know these things are frustrating to new Rust users who just want everything to be automatic and easy, but if we’re talking about LLM development anyway then these optimizations would have come up the first time you asked your LLM what could be done about improving compile times. LLMs are very good at setting up these optimizations.

What kind of work are you doing where the LLM turns are only taking "seconds" and it's recompiling all the time?

This morning so far my LLM rounds have taken between 10-15 minutes. An incremental compile happens a couple times at most.

Even on the largest Rust codebases I've been working with (OSS projects), incremental compiles are not taking multiple minutes unless I do something that triggers a full recompile.

I don't really understand why Rust seems to be the go-to language for llms. Yes sure it has a good type system, but in practice llms seem to trip over it as much as I do, and given how fast llms are at writing code, that just makes compile times a much larger bottleneck.

Go is full of footguns and LLMs still cannot be trusted to follow the rules they themselves conjured up out of thin air. Unlike humans, they don't need to be taught the language (which is the hardest part of using Rust, by far), so they get more benefits out of it than many humans do.

LLMs do trip up when they generate Rust code, but they also do when generating any other language. The big difference is that the Rust compiler refuses to compile broken code faster, whereas Go will just let you SIGSEGV on edge cases without warning.

The recent TLA+ hype here on HN shows that Rust may just be the beginning here. There are valid, safe Rust programs that will crash, the language isn't perfect. The older languages with more math and validation behind them (Ada?) are probably even better suited for generated code, but they don't have the hype culture to capture mainstream attention (and even fewer people have the ability to really review that code).

There's an alternative solution of course: use platforms like JS/.NET/JVMs/Python to run code that cannot violently crash because of the language runtime around it. That comes with a performance overhead but it's good for prototyping without as many stability footguns and with faster compilations.

Rust is built on the idea that code that compile must be correct, to the best of its abilities. LLMs are fast and sloppy, Rust keeps them in check by not letting them get away with preventable bugs.

Of course, Rust can't do anything for spec bugs, like making the stop light green when it should be red, but it can help with crashes and vulnerabilities.

Another thing I might add is that Rust is a relatively popular language, with a culture of writing high quality code. Many people, starting by those of Mozilla chose Rust to write security-critical, efficient software. They wouldn't chose it for throwaway, low skill, non-critical code, as there are languages that are more appropriate for this.

The result is a large amount of high quality code a LLM can train on. Compare to Zig for instance, which is a fine language, but not as popular so lacking in volume for good training. You then can understand why Anthropic ported Bun from Zig to Rust if they intend to vibe code. Languages like PHP, while actually quite decent today, have a long history of terrible code, so not great for a LLM as most of its training dataset is poisoned.

The unfortunate part is that it may not last. If Rust becomes the de-facto language for LLM production, overall quality may decrease. It is a common problem with many machine learning techniques including LLMs: feeding them their own output tend to decrease quality.

OpenAI is a Rust Foundation platinum level donor. They gave straight cash which can go toward paying maintainers, which is better IMO. This actually made a lot of people angry because they saw it as a risk of OpenAI gaining influence or something. Can't make everyone happy.

OpenAI also hands out free subscriptions to open source maintainers: https://developers.openai.com/community/codex-for-oss They're time limited for now, but they've been pretty generous about who gets them. Anyone who can show Rust contributions would have been able to get one before.

I tend to disregard anyone who complains about foundational open source being funded like this. As long as the donor doesn't have dictatorial control over the product, why obsess over this?

Because not having dictatorial control doesn't protect anyone from anything; politicians take 'donations' (bribes) and then argue or enact laws for what the donor wants, no dictating involved.

Or in software terms, BigCorp sponsors you to develop an open source tool fulltime. If you make the tool more useful for them while making it more complex or worse or ignoring things for others, they might fund you next year as well. If you don't develop things that help them, they might stop and send that money elsewhere and you will need to get a normal job instead and drop your tool work to part-time. Even though they aren't dictating anything, what are you incentivised to do?

There's definitely a cost in terms of features BigCo doesn't need that get deprioritized. But that work still gets done if other people need it, it's just slower, and I don't think you could ever pull off making things worse on purpose in a big community run project like Rust.

The only times this actually happened are C++ and CORBA as far as I remember. Both of them were bureaucratic design by committee efforts from the start, the people doing it weren't users but implementors looking to stop competition, and it all happened before the open source era.

Can't confirm this "pretty generous", many people with lots of contributions to popular projects got any from OpenAI, not even a response to their request.

LLMs are useful in engineering even if the PRs don't include LLM-written code.

>I’m still writing all my own code and text, because (a) that’s paramount, and (b) the project policy requires it, but I had useful LLM analysis assistance on several of the PRs mentioned in this post.

This is one of the most important objectives in software today.

Rust is the best language to serialize agentic LLM output to. It's native, well constructed, low-defect due to design. It's also easy for humans to read and debug if necessary.

The biggest problem with Rust is the compile times. The cycle has to get faster. And we need to start thinking about making the artifact cache non-blocking so multiple agents can work simultaneously - that'll be a big task, but essential if we want to speed up work on one machine rather than spinning up clusters of agent sandboxes (the alternative, perhaps superior solution).

Doing stuff isn't free. For instance, Go compiles relatively quickly for a modern language, but the biggest reason for that is that it does less stuff than most compilers... less optimization, less checking, and some stuff built into the language to avoid some of the problems with having to read lots of headers just to compile a file and other ways of doing less stuff, but mostly the key is it does less stuff, in both the good and bad senses of that.

If you want something like Rust that offers guarantees and checks and cross-checks by the boatload, it adds up. Macros, monomorphization, implicit code generation with traits and all those other things add up too. And you can't always get O(n) or O(n log n) code to implement those checks. Maybe it can be sped up and maybe there's tricks here or there, but at the Pareto frontier, a language that has more checks will be slower to compile than one that has fewer.

And that's not a bad thing or a deficit in Rust, it's just the nature of the beast.

Instead of Go, you could have reached out to complex languages with fast compilation times like D, OCaml, Haskell, Ada, Delphi, C++.

All of them have alternative implementations with fast compilation times.

D, use dmd for fast development workflows, gdc or ldc for the ultimate performance at the expense of compilation times.

OCaml, use the REPL or bytecode interpreter for fast development times, the full blow compiler for ultimate performance.

Haskell, use the REPL, GHCi for the fast development cycles, GHC for the release build.

Ada and Delphi, have had fast implementations since forever, although Ada/SPARK is indeed somehow expensive.

C++, yes it isn't a mistake. Use Live++, VS hot reload, coupled with binary libraries, or a REPL like CINT (nee ROOT), binary libraries for dependencies, incremental compilation and incremental linking for the development workflow.

The problem with Rust isn't the language itself, rather the ecosystem currently lacking such kind of options being available.

including c++ with all of those qualifiers would be like me saying rust is fast with sccache, subsecond, cranelift, and making every single module a separate crate.

The difference being the adoption culture across the ecosystem.

C++ game engines also don't need Bevy like tutorials, because most studios aren't compiling them from scratch, and tools like Live++ or VC++ hot reload are relatively easy to use.

unreal engine is compiled from scratch (depending on your definition of "from scratch") and has notoriously long compile times. heck you have to recompile the editor to make certain gameplay code changes. and it's by far the most popular AAA game engine on the planet. if it was so easy to fix with your suggestions they would have done it already.

but hey, just add subsecond and switch to cranelift. problem solved :)

Unreal Engine has an installer, and they have done my suggestions, as they are the main customers of Live++ [0], advocates of tooling like Blueprints and now Verse for doing full games.

Many studios have delivered games with little to no changes to the underlying C++ code.

so... c++ compile times are fast, because you can simply not compile c++ and instead use blueprints? seems odd since we're talking about c++/rust compile times. turns out you can make rust compile times infinitely faster by not compiling it too...

but when you do have to compile c++, it can be real slow. maybe not as slow as rust, but it's not in the same league as eg. go, c#, zig, etc.

ue5's hot reload is by no means perfect either - many gameplay code changes require recompiling the editor. exposing c++ properties on a blueprint? recompile. modify a constructor? recompile. changing parameters, return types, or adding/removing UFUNCTION or UPROPERTY macros? recompile. you can simply search the web to read the experiences of thousands of ue devs complaining about slow compile times and workflows. it's the same with unity btw, search "reloading domain unity".

also verse is not in unreal engine. no studio is using verse for ue games. not sure why you threw that in.

i get you love c++ and dislike rust, but you aren't really making a good case for c++ when you group it in with other languages that have fast compile times ootb, make arguments that involve not using c++ (like blueprints, lol), and rely on brittle third-party hot-reloading solutions.

I threw that in, because if you knew Unreal Engine, you would be aware of the roadmap for Unreal 6.

No one is saying that C++ compile times are anywhere close to Delphi or D, although they are much better when using modules actually.

Rather that C++ ecosystem has a developer culture and tools, that makes compiling from scratch and pure distribution of source code for what is a compiled language, something rare, thus despite its slowness, the average impact is less felt than on Rust projects.

Rust wants badly to have its cake and eat it too. I get it, but it's not the sensibilities I have. The rustc compiler, if it really can achieve everything all at once, will be a beast like none other, making C++ compilers look simple by comparison.

I'd love something halfway. Go is maybe a bit radical in some regards, but also, with the news of the new SIMD package for Go, it has occured to me just how little I missed having things like, say, autovectorization.

(I know also that some people have tried halfway, but the big thing is figuring out how to keep a relatively simple type system that can still support a borrow checker. Even if there is some middleground, is it truly worth it? As nice as it sounds, I've been more skeptical. Go seems to exist in a very narrow space where its simplifications barely can be made to work.)

And since you bring up Go and contrast the compile time with Rust, it's been experienced at Google (and also Volvo and other places) that Rust and Go teams are as productive whereas C++ is less than half as productive: https://www.youtube.com/watch?t=27012&v=6mZRWFQRvmw&feature=...

So the focus on Rust compile time is misplaced. It's not a big deal in terms of overall productivity.

I don't think that follows - just that compile times aren't the only thing that matters. Maybe rust could be twice as productive as go if compile times went to zero for instance (or maybe not - just disputing that the evidence proves the claim here).

But it can't go to zero, that was the point -- at some level you have to pay for what you get. I'm not saying the compile times couldn't be better, but Rust can't be Go in terms of compile times if it wants to offer the guarantees and options it does. Meanwhile if Go wants to offer more options and stronger guarantees, it won't be able to preserve the short compile times everyone points to.

The Cranelift backend is extremely fast. Most of the slowness is all the crazy optimizations that LLVM does + other things (generating debug info etc).

For symbol heavy projects, linking is a surprising bottleneck.

Some ideas to speed up compilation by not evaluating items that are not used might pan out significantly for big crates in your dep tree (that behavior might never be stable because that would allow items with compile errors in a crate that would still let your application compile, which is against the Rust approach). The same work to do that would also allow overlapping of crate evaluation between different rustc instances called by cargo, as it would require partial evaluation of crates (to do name res only and gather the symbols needed from its deps).

Another thing is that stable rust doesn't treat macros as idempotent (because that wasn't a requirement from the start, there are crates that do dynamic IO to generate types), but if they are then incr comp can be faster by not evaluating them unnecessarily.

I know people are working on a bunch of different strategies to improve both first and incremental compile times, and I'm looking forward to the fruit of their labor.

Compile times are rarely the bottleneck for me, but that doesn't mean I won't welcome any improvements on that front.

> For symbol heavy projects, linking is a surprising bottleneck.

Is that still true with modern linkers like `wild`? Seems like it can link Chromium in 1-2s.

> Another thing is that stable rust doesn't treat macros as idempotent

This seems absolutely insane to me given how pervasive macros are in Rust (I wonder how much of incremental compilation time is just repeated serde derives?). Obviously we can't just blindly treat all macros as idempotent, but an opt-in attribute on a macros that pinky-promises that it is seems like it ought to be pretty easy to implement?

Maybe somebody's looked into it and it doesn't help much? But I've heard (unverified) rumours of the opposite.

> Is that still true with modern linkers like `wild`? Seems like it can link Chromium in 1-2s.

Wild improves things significantly, but it really depends on the kind of project. For some a third of the time can be linking. And not everyone configures their environment to use a different linker. Another thing that can easily improve performance is changing the global allocator, but I've seen teams that measured 10% perf improvements in their own metrics decide against going with anything other than the "default".

I fully expect that if wild delivers an effective incremental linking architecture, then rustc will be able to produce the patches directly (instead of wild having to produce patches from two versions of the object files), which would mean both that rustc is producing less LLVM bytecode and that wild gets to do what it (will) do best and make linking as fast as mechanically possible.

> This seems absolutely insane to me given how pervasive macros are in Rust

Part of the problem I see is that crates will have to opt-in (and we might be able to change the default over an edition boundary) to get the perf benefit, and it might require a granularity lower than "a crate" (which would complicate implementation). I haven't seen additional discussions around these design considerations (needed to stabilize), which will need to happen before people can see progress.

Sadly, Rust is, like many open source projects, a show-up-o-cracy: you need a motivated (group of?) individual(s) to deliver a feature to fruition, and if the person driving a feature is fine with using nightly for their purposes, and only needs a subset of a feature, they will drive the feature to that state (lets say 80% completion), and then the feature will linger (until someone else with enough motivation to see the other 80% through shows up). This is exacerbated because the project is unwilling to have 80% solutions on stable unless the state is very clearly not going to preclude other future work, or the path to completion is 100% visible (but if that were the case, then it would have been completed already). So we end up with situations like the Allocator APIs.

(I did a quick test, and I'm seeing between 15-20% for https://github.com/servo/stylo which is a macro-heavy crate. I guess it only matter for crates you're actually editing though, macro will already be cached as part of "entire crate is unchanged")

> Another thing that can easily improve performance is changing the global allocator, but I've seen teams that measured 10% perf improvements in their own metrics decide against going with anything other than the "default".

Yeah, although I think there's more of a trade-off there. Alternative allocators can add significant amounts of compile time. Whereas, modulo maturity, I think a faster linker is more of a pure win. I would imagine we will make wild the default linker at some point if development continues on the trajectory it seems to be on.

I’m not sure if Cranelift support will ever become stable. It’s really complex, it has tradeoffs like you mentioned, and it requires its own backend to be maintained. TPDE looks like something that could more realistically be stabilized as it just slots into the existing LLVM support.

Zero-cost abstractions aren't zero cost in compilation time. High-level abstractions translate to a lot of boilerplate that the compiler has to optimize out.

In unoptimized builds often the linker is the bottleneck. Rust/Cargo can parallelize most of the build, generating tons of code and debug info, but then the poor linker has to consume all of it at once. The object/exe formats were designed in ancient times, so they're hard to build incrementally or in parallel (some linkers are trying).

Is there any experimentation with new ABIs? I mean certain linker flags like --f-lto literally hijack the linker protocol to dump an AST into the backend.

At least for the fully static binary part of rust, there should be some optimizations there w.r.t. compilation. Sure you're not going to interface with shared libraries well but maybe a small experimental feature for fully owned projects? Idk.

Rust already uses MIR-based libraries for LTO, and uses thinLTO by default.

ABIs won't help automatically. The overhead comes mainly from generics and macros. Cross-crate monomorphic generics and AST macros are impossible to express in an ABI. Turning them into polymorphic usually wouldn't remove the many abstraction layers that need to be peeled off, and only make them cost at runtime too.

So far MIR optimizations were helpful. Rust can simplify high-level MIR quicker than LLVM can simplify the same code after it's been lowered to lots of low-level instructions.

I once heard (and don't know if it's still true) that the biggest compile-time sinks are macros and codegen.

Both are kind of outside the Rust compiler's influence. Macros can be almost arbitrarily complex: you pay for what you order. Codegen is LLVM, and that's a fixed choice. You can use Cranelift to get around it, but then you pay elsewhere.

Also, generics and monomorphization regularly come up in these discussion, while common wisdom seems to be that cost for the additional static analysis over other languages like C++ is no a major contributor.

Regardless, it's nice to see performance improvements in the compiler, even if you have to cooperate to benefit from them (e.g. by keeping your macros light and use less generics).

Its similar to C++ compilers, there is no one reason. It is a language that tries to optimize a lot, its a big language, it does safety checks, it uses llvm which is a bit slow, its a language that makes use of generics which generate extra code etc etc.

C++ compilers have it better, despite the fame, because on the C++ world, people like their binary libraries (not compiling the world from scratch on each git clone), there better support for incremental compilation, and incremental linking, there are interpreters and hot code reload tooling available.

Some C++ compilers and linkers have better support for incremental compilation and linking, and do it more fine grained than Rust, e.g. VC++.

Some tooling ideas go all the way back to when C++ vendors started adopting ideas from Smalltalk and Lisp, e.g. Energize C++ or Visual Age for C++ v4.

Or build systems like ClearMake from ClearCase, where the object files and binary libraries are shared across everyone on the cluster with the same views (ClearMake speak for what files/branches are selected).

First of all, the fact that the article talks about "speeding up" the rust compiler doesn't automatically mean that the compiler is "slow"[0].

Now, is rustc slower than e.g. clang? by how much? why?

Those are different (and complicated) questions. It really depends on what you're compiling, but I'd say rustc can be 1-5x slower (maybe more at times?).

The reasons are many and varied, but in general rust compilation is slower because the compiler is doing way more things compared to C (monomorphization, complex trait resolution + type inference, borrow checker..)

[0]: Also I'd argue that "slow" without a concrete point of reference is a meaningless term in this context.

The go compiler is considered fast, yet Google spends effort speeding up the go compiler. Not to the same extent, but Google has a lot of go code, so it does make a difference.

Ultimately it's the fact that compile time was not a first-class consideration during the design of Rust's important features. There's only so much you can do to mitigate the consequences.

Compilation times were a consideration, but they were a subservient consideration to the prime considerations of 1) being as memory-safe as GC'd languages, 2) exploring the limits of statically-guaranteed thread safety, and 3) being as fast and memory-efficient as C and C++. If Rust had been willing to compromise on those goals and instead had just, for example, used a virtual machine with pervasive garbage collection and been designed for dynamically-dispatched generics then you'd get a lot of compilation time reductions for free, but the world didn't need another Java, it needed a more secure systems language to stand up against C++ where every previous challenger had failed.

While it has found success on mainstream, it basically proven Cyclone ideas were right, and now we have other languages adopting similar ideas into their type systems, which helps closing the gap with 3).

Since the 2000's we have been on the wrong path, many developers kept reaching for C and C++, not because they needed the actual features of a systems programming language, rather they didn't knew anything else that would ahead of time compile to native code, or even if they did the mindshare wasn't relevant for them.

Now thankfully we are circling back to how it should have been all along.

However all of this might be meaningless in the age of AI driven programming, where developers have no clue if the agent is driving automatic or stick, while delivering on the Markdown file plan.

No, Rust is not at the paretto frontier for your mentioned 1, 2, 3 and also 4 compilation speed. It could have all of those things and also just have faster compilation. Rust devs have talked about how they have some regrets about not optimizing more for compilation, but instead another attribute got optimized in terms of paretto efficiency - the language's development time. Arguably I think that is the single worst trait you can optimize for in language development, because by saving a little time developing the language you cost humanity, let's say hundreds of millions of hours of development time downstream from you, with millions of users being less productive.

> It could have all of those things and also just have faster compilation.

Rust was originally a research language. It wasn't even clear that their primary three goals--"safe, concurrent, fast"--were simultaneously achievable to their desired degree. That it turned out to be possible was one of the most surprising and impactful results in the history of language design; even the early formulations of Rust assumed that both a garbage collector and a green thread runtime would be necessary, neither of which turned out to be true. That Rust could have faster compilation is both true and vacuous; there's always more optimizations to be eked out. The main question is whether or not significant performance wins could be gained by having made different, fundamentally-backwards-incompatible design decisions, and the answer is no, not really. Performance-related features like referentially-transparent procmacros can easily be made the default over an edition, and polymorphization can be implemented via an alloca-based virtual-dispatch ABI vis-a-vis Swift.

> Rust devs have talked about how they have some regrets about not optimizing more for compilation, but instead another attribute got optimized in terms of paretto efficiency - the language's development time.

No, the early Rust devs got this right. They were in fact highly incentivized to care about compiler performance, because rustc has been bootstrapped since 2011, making them the most serious users of the language in earnest (with the second-most serious users being the Servo devs one cubicle over). Rust spent years getting its basic design nailed down, then it did the hardest thing for any language: understanding the importance of shipping, resisting the urge to endlessly pursue perfection, and future-proofing what they could. Without shipping a useful language you can't get in the hands of users, and without getting in the hands of users you can't discover your most important flaws in practice. And because Rust shipped in 2015, it had ten years to hammer itself into shape to weather the agentic era; it could have easily still been on version 0.113 by now, puttering around in an ivory tower with no commitment to stability and no real users to give feedback.

This is not actually the main reason, most of the time.

Generics/monomorphization and how iterators work results in a lot of compiler bytecode that has to be churned through. More bytecode = longer compilation. It increases the size of the (debug) binaries, the debuginfo in general, causes performance issues with debug binaries in some situations unless you bump the optimization level, causes more IO, etc.

It's unlikely that many people are using Rust without using Option<T> or Result<T, U> a fair bit. Idiomatic Rust fundamentally uses a lot of generics. And a basic for loop expands into quite a lot of intermediate representation due to Iterator.

Other languages support generics, monomorphization, and iterators (e.g. Zig or D), but they're not as slow as Rust to compile, what's the reason for that?

It's likely easier to answer for specific languages

All three of those words can mean "just like Rust" but equally "Not at all like Rust" for different languages.

Two examples to contrast: In C++ the iterators are basically a pointer analog (in some cases they're just literally pointers) and that's a very difference "feature" but it's still definitely iterators. In Ginger Bill's Odin, the iterators are a function, possibly generic, which returns a pair, the next item and a boolean telling you whether the iterator was exhausted.

Trait solving isn't a bottleneck for Rust compilation unless you're doing some extremely cursed things like trying to implement Doom in the type system. At the end of the day it's still mostly that Rust just generates a ton of IR for LLVM to chew on (because of monomorphization), then LLVM takes a while to process all of it (because LLVM is designed primarily to produce high-performance code, often resulting in reasonable tradeoffs against compilation speed), and then the linker takes a while to connect it all together. With an alternative backend to LLVM (e.g. Cranelift) you could choose to design it with a greater emphasis on compilation speed (likely trading off generated code quality in the process). And with a more radical vertically-integrated model where Rust controls the linker you could do in-place linking and nearly completely skip the final step (at least for debug builds), but that's a big change compared to the classic C-style build model.

Yes this seems like the main way to go. With dependency injection using "dyn" traits on top of that, it seems that this mostly solves the compilation issues with Rust. It might be better for tests and agents to split code in small chunks too.

I am experimenting with this in my project right now. I haven't reached a verdict yet, but in theory it sounds good. I think you're still paying the linking cost though?

Splitting out a project into multiple crates reduces what needs to be recompiled during development. I tend to break out areas of my application that aren't going to change regularly so I'm only having to rebuild the main application.

In a production scenario where you're probably building your application in some CI environment, unless you cache the release build artifacts to re-use when applicable, the entire project will be rebuilt every run.

It’s honestly my biggest issue right now during development. I’m refactoring into a “vertical slice” architecture and then will try crating by feature… fingers crossed.

Incremental seems to keep winning the easy wins, so the interesting part is whether the remaining compile-time still lives in the same places as last year.

I recall a talk about makepad.dev, I think it was by Rik Arends, that explained how they achieved outstanding compilation times in rust for makepad.

I can't find that talk again, but it was quite interesting: the rust compiler is fast, but often times it has to perform a lot of unnecessary checks because crates contain more stuff than needed. By stripping unnecessary work, the makepad team made building pretty fast.

I think there are a few more. Especially cranelift, but I would not use it for production stuff and it is missing a lot of llvm intrinsics that will just trap if you are trying to use them. But for most it seems to be just fine for regular dev builds with a HUGE speedup.

It’s not compiling C code, so that’s not really possible to answer. C is uniquely fast to compile, especially compared with more featureful languages like C++ and Rust.

In practice, C++ and Rust feel pretty similar, mostly due to the kind of code people tend to write in both languages (favoring static dispatch, generics/templates, etc.).

Rephrased question: How does the Rust compiler's speed compare to the C compiler GCC's speed with respect the language each is compiling, i.e., rust and C, respectively

I don't understand why developers are interested in Rust.

- Raw performance doesn't actually matter for the vast majority of use cases. Performance does not equate scalability. Moreover, differences usually disappear in practice once you've actually developed the software because time and storage complexity of operations usually dwarf constant resource costs. Furthermore, do you realize how much more computational resources AI uses compared to a classic piece of software? Trying to optimize tools in the age of AI is like putting lipstick on a pig.

- It's more verbose than most other languages; waste of tokens, context window, time and AI reasoning capacity. The strain most devs feel when reading Rust, also impacts LLMs. It obfuscates essential logic and replaces it with ceremony.

- The Rust training set is far smaller than other popular programming languages. It's also quite different from other programming languages so it probably doesn't benefit as much from cross-language patterns; in fact, could be problematic.

- You have to wait for a compiler; more wasted time which the AI agent could have been using to write code.

It's like TypeScript. Devs became obsessed with TypeScript. Everyone was sure that it would be better for AI. Not the case. LLMs essentially never make type errors in JavaScript (or TypeScript). Static typing is completely redundant. These are the most trivial kinds of errors to avoid. Seriously, try Claude with vanilla JavaScript on Node.js. TypeScript is worse with AI because people who used it tended to over-engineer, also a lot of TypeScript is ceremonial and performative complexity intended for a bureaucratic audience; those are the main patterns which AIs picked up from their training set.

Seriously, try working with a TypeScript codebase and notice how Claude invents all these contrived abstractions, spread out over a huge number of files with unclear separation of concerns and full of lengthy, highly contrived comments.

It's the same issue with all these over-engineered languages which were developed for people who were not good at coding and needed a whole bunch of extra safety features in order to produce functioning software. It's like training wheels on a bike; great to learn in the early stages but if you want to learn how the pros do it, you've got to look at the people who compete in the Olympics; and note that there's a reason none of them still have training wheels on their bikes!

Goodness. What a terrible take on every point. My favorites are the claim that raw performance doesn't matter and that memory safety is only for bad programmers, despite this industry having nearly a half-century history of severe memory vulnerabilities regardless of experience level.

I agree that automatic resource management is a real prize, and something that Scala 2 had in libraries but was hard to guarantee at compile time. I think I fix a leaked resource a month in our Scala code.

The EverInitializedPlaces example really stands out. Going from ~1.5M to ~90K apply\_effects\_in\_block calls by changing the CFG traversal is a reminder that the biggest compiler optimizations often come from changing the algorithm, not optimizing the hot loop itself.

It also seems like the new Polonius/trait-solver work is pushing compiler performance toward a more interesting problem: doing expensive analysis only when it is actually needed.

4.57% mean wall-time reduction across 629 benchmarks in two months is pretty remarkable. Great progress.

> reminder that the biggest compiler optimizations often come from changing the algorithm, not optimizing the hot loop itself.

Isn't this true for most optimizations, not just in compilers? My usual goto process for optimizing is "Find stuff we're doing that we don't have to do, re-evaluate what data structures we use and then re-evaluate what algorithms we use" basically, with minor changes depending on the results. Served me well so far, and haven't (intentionally) written any compilers.

https://github.com/rust-lang/rfcs/pull/3924
2026-11-16

## Conversation

### **joshtriplett** commented Feb 23, 2026 • edited by rustbot Loading Uh oh! There was an error while loading. Please reload this page.

Copy link
 

Copy Markdown

Member

*View all comments*

This RFC adds a mechanism for crates to *hint* that builds should use  
optimization by default, while still allowing the top-level crate to  
easily override this.

Important

When responding to RFCs, try to use inline review comments (it is possible to leave an inline review comment for the entire file at the top) instead of direct comments for normal comments and keep normal comments for procedural matters like starting FCPs.

This keeps the discussion more organized.

Rendered

`Cargo: hints.min-opt-level`

`44fc14e`

```
This RFC adds a mechanism for crates to *hint* that builds should use
optimization by default, while still allowing the top-level crate to
easily override this.
```

joshtriplett
added
the 
T-cargo
Relevant to the Cargo team, which will review and decide on the RFC.
label
Feb 23, 2026

github-project-automation
Bot
added this to Cargo status tracker
Feb 23, 2026

`RFC 3924`

`c55f830`

**Kobzol**
reviewed

Feb 23, 2026

View reviewed changes

Comment thread

text/3924-cargo-hints-min-opt-level.md

Resolved

### Uh oh!

There was an error while loading. Please reload this page.

`1a0f38b`

**epage**
reviewed

Feb 23, 2026

View reviewed changes

Comment thread

text/3924-cargo-hints-min-opt-level.md

Resolved

### Uh oh!

There was an error while loading. Please reload this page.

**epage**
reviewed

Feb 23, 2026

View reviewed changes

Comment thread

text/3924-cargo-hints-min-opt-level.md

Resolved

### Uh oh!

There was an error while loading. Please reload this page.




Comment thread

text/3924-cargo-hints-min-opt-level.md

Resolved

### Uh oh!

There was an error while loading. Please reload this page.




Comment thread

text/3924-cargo-hints-min-opt-level.md

Resolved

### Uh oh!

There was an error while loading. Please reload this page.

**Noratrieb**
reviewed

Feb 23, 2026

View reviewed changes

Comment thread

text/3924-cargo-hints-min-opt-level.md

Resolved

### Uh oh!

There was an error while loading. Please reload this page.

**hanna-kruppe**
reviewed

Feb 23, 2026

View reviewed changes

Comment thread

text/3924-cargo-hints-min-opt-level.md

Resolved

### Uh oh!

There was an error while loading. Please reload this page.

ehuss
moved this to **RFC needs review**
in Cargo status tracker
Feb 24, 2026

**JarredAllen**
reviewed

Feb 28, 2026

View reviewed changes

Comment thread

text/3924-cargo-hints-min-opt-level.md

Resolved

### Uh oh!

There was an error while loading. Please reload this page.

**tgross35**
reviewed

Mar 2, 2026

View reviewed changes

Comment thread

text/3924-cargo-hints-min-opt-level.md

Resolved

### Uh oh!

There was an error while loading. Please reload this page.

joshtriplett
and others
added 8 commits
March 5, 2026 16:54

`Expand motivation`

`b806002`

`fb7b4c3`

```
…zed code
```

`Remove stray whitespace`

`2997fa1`

```
Co-authored-by: nora <48135649+Noratrieb@users.noreply.github.com>
```

`40e53d4`

`3f53e4b`

```
…imum

Particularly relevant for `"*"` overrides.
```

`Add alternative about supporting "s" or "z"`

`383f360`

`7772471`

```
Crates optimizing for size are likely to want size-over-speed
optimizations in their dependencies as well.
```

`78b164f`

```
Aiming for an improvement on balance, but it won't be an improvement for
*every* user.
```

### **joshtriplett** commented Mar 6, 2026

Copy link
 

Copy Markdown

Member

Author

|  |
| --- |
| ---   I've incorporated all feedback as of this comment. |

joshtriplett
added
the 
I-cargo-nominated
Nominated for discussion during a cargo team meeting.
label
Mar 6, 2026

ehuss
moved this from **RFC needs review**
to **Nominated**
in Cargo status tracker
Mar 8, 2026

### **epage** commented Mar 10, 2026

Copy link
 

Copy Markdown

Contributor

|  |
| --- |
| Can we call out that we should document overriding dependency opt-level when debugging? |

### **joshtriplett** commented Mar 10, 2026

Copy link
 

Copy Markdown

Member

Author

|  |
| --- |
| Would love to get feedback from crates that are likely to want this.  cc @alice-i-cecile for Bevy.  cc @abonander for sqlx. |

### **AMDmi3** commented Mar 10, 2026

Copy link
 

Copy Markdown

|  |
| --- |
| Maybe also @LaurentMazare for candle (the perf difference is so large it's likely pointless to use unoptimized candle as a dependency), and @mitsuhiko for insta (insta suggests to set opt-level, though I've never in fact witnessed even a slight difference). |

### **epage** commented Mar 10, 2026

Copy link
 

Copy Markdown

Contributor

|  |
| --- |
| An interesting case is rsa which has  **Note:** If you encounter unusually slow key generation time while using `RsaPrivateKey::new` you can try to compile in release mode or add the following to your `Cargo.toml`. Key generation is much faster when building with higher optimization levels, but this will increase the compile time a bit.  ``` [profile.debug] opt-level = 3 ```  If you don't want to turn on optimizations for all dependencies,  you can only optimize the `num-bigint-dig` dependency. This should  give most of the speedups.  ``` [profile.dev.package.num-bigint-dig] opt-level = 3 ```  Though that is removed for the next version (RustCrypto/RSA#523) because they switched dependencies.  CC @tarcieri |

**abonander**
reviewed

Mar 10, 2026

View reviewed changes

Comment thread

text/3924-cargo-hints-min-opt-level.md

|  |  |  |
| --- | --- | --- |
|  |  |  |
|  |  | Crates could overuse this mechanism, requiring optimization even when they |
|  |  | don't actually need it. We should provide clear documentation recommending when |
|  |  | to use it and when not to use it. |

### **abonander** Mar 10, 2026

Copy link
 

Copy Markdown

There was a problem hiding this comment.

### Choose a reason for hiding this comment

The reason will be displayed to describe this comment to others. Learn more.

I was unable to un-resolve the previous thread myself so I'm just starting a new one instead:

I would definitely be hesitant to set this by default in SQLx because I can *easily* see people coming to us complaining that it's suddenly building a lot slower. Clean build performance doesn't normally affect *my* workflow, at least for local development builds, but one place it does come up a lot is in CI.

Caching is finicky to set up and configure, can be really flaky and is nearly impossible to debug when it is, and when using the `actions/cache` action or any actions built on it like `swatinem/rust-cache`, it can be a lot slower on self-hosted runners because of throttling. I've actually seen build times go *down* after deleting the caching step simply because it was bottlenecking on uploading the archive (sometimes even to the point of timing out).

It would obviously be a major behavior change, but I've been thinking for a while that users who care about performance in dev builds should have the option to just build *all* dependencies with optimizations+debuginfo by default. I started opining on this until I realized that this already existed, which I didn't know before because it's only mentioned in passing in one spot in the Cargo book:

> The precedence for which value is used is done in the following order (first match wins):
>
> 1. `[profile.dev.package.name]` — A named package.
> 2. `[profile.dev.package."*"]` — For any non-workspace member.
> 3. ...

### **epage** Mar 10, 2026

Copy link
 

Copy Markdown

Contributor

There was a problem hiding this comment.

### Choose a reason for hiding this comment

The reason will be displayed to describe this comment to others. Learn more.

> I've been thinking for a while that users who care about performance in dev builds should have the option to just build all dependencies with optimizations+debuginfo by default.

We're tracking this at rust-lang/cargo#15931

> I started opining on this until I realized that this already existed, which I didn't know before because it's only mentioned in passing in one spot in the Cargo book:

We also talk about that config at https://doc.rust-lang.org/nightly/cargo/guide/build-performance.html#reduce-amount-of-generated-debug-information but only for debug info and not optimizations

### **epage** Mar 10, 2026

Copy link
 

Copy Markdown

Contributor

There was a problem hiding this comment.

### Choose a reason for hiding this comment

The reason will be displayed to describe this comment to others. Learn more.

> I would definitely be hesitant to set this by default in SQLx because I can easily see people coming to us complaining that it's suddenly building a lot slower. Clean build performance doesn't normally affect my workflow, at least for local development builds, but one place it does come up a lot is in CI.

Your docs mention opt-level 3. What is the incremental improvement between opt-level 0, 1, and 3? If 3 is noticeable enough, I wonder if a min-opt-level of 1 would strike a good balance.

### **abonander** Mar 10, 2026

Copy link
 

Copy Markdown

There was a problem hiding this comment.

### Choose a reason for hiding this comment

The reason will be displayed to describe this comment to others. Learn more.

I think it'd be all right if Cargo emitted a message informing the user that an override was being applied automatically here, but then again if it did that for every crate in the graph that specified an override then it'd just get lost in the noise.

However, I definitely feel that "somehow educate the user and let them make the decision" would be the most Rust-y way to do this.

### **abonander** Mar 11, 2026

Copy link
 

Copy Markdown

There was a problem hiding this comment.

### Choose a reason for hiding this comment

The reason will be displayed to describe this comment to others. Learn more.

> Your docs mention opt-level 3. What is the incremental improvement between opt-level 0, 1, and 3? If 3 is noticeable enough, I wonder if a min-opt-level of 1 would strike a good balance.

That advice is specifically for speeding up the proc macros, since they're so much more heavyweight than pretty much anything else out there. It can really have an outsized effect on compile times.

It's definitely dependent on the project, but for this example project which uses a number of query macros as well as `#[sqlx::test]` invocations, `cargo build` with a fully cached dep tree goes from 2.7 seconds to 2.6 to 2.4 for `profile.dev.package."*".opt-level = 0`, `1` and `3` respectively.

Just setting `profile.dev.build-override.opt-level` seems to be more of a wash, though. When I tried `0`, `1` and `3` with the same procedure (`cargo clean && cargo build -q && cargo clean -p sqlx-example-postgres-axum-social && cargo build`), I got 2.55s, 2.73s and 2.74s, respectively.

The differences here are not exactly something a human would notice anyway, but I just don't have a huge project using SQLx close to hand anymore since I started my new job.

### **obi1kenobi** commented Mar 10, 2026

Copy link
 

Copy Markdown

Member

|  |
| --- |
| Would love to get feedback from crates that are likely to want this.  cargo-semver-checks and its Trustfall dependency both would benefit from a hint that recommends enabling optimizations even in debug profiles.  While I can't seem to find the concrete issue, I recall at one point @epage having a performance concern about cargo-semver-checks being very slow that turned out to be due to unoptimized builds causing poor `Iterator` performance when Trustfall and cargo-semver-checks use iterators *very* heavily.  A hint to set a minimum optimization level would have prevented that problem entirely.  Ideally, we'd be able to neatly specify "`trustfall` + selected dependencies" should be optimized, since there are often multiple crates in play: `trustfall`, `trustfall_core`, the adapter which is usually a separate crate (e.g. `trustfall-rustdoc-adapter`), etc. But I wouldn't let perfect be the enemy of "good enough and shipped" here :)  I have not benchmarked the differences between `opt-level` being set to 1 / 2 / 3. From a downstream user perspective, `trustfall` and related dependencies only get compiled ~once, so set-and-forget to `3` has been fine so far IMHO. We have not needed `s / z` optimization modes thus far. |

### **tarcieri** commented Mar 11, 2026

Copy link
 

Copy Markdown

|  |
| --- |
| Something like this would definitely be useful, as we inevitably get asked about why things are slow in debug builds, e.g. RustCrypto/RSA#144 |

ehuss
removed
the 
I-cargo-nominated
Nominated for discussion during a cargo team meeting.
label
Mar 31, 2026

joshtriplett
mentioned this pull request
Apr 21, 2026

### **joshtriplett** commented Jun 25, 2026

Copy link
 

Copy Markdown

Member

Author

|  |
| --- |
| Based on feedback from @tarcieri and @obi1kenobi, it sounds like this will get some use. It might help to have *additional* support for applying recursively to dependencies, but that'd take a lot more design.  Let's not let the perfect be the enemy of the good, here.  @rfcbot merge cargo |

### **rust-rfcbot** commented Jun 25, 2026 • edited by 0xPoe Loading Uh oh! There was an error while loading. Please reload this page.

Copy link
 

Copy Markdown

Collaborator

|  |
| --- |
| @joshtriplett has proposed to merge this. The next step is review by the rest of the tagged team members:   * @0xPoe * @Eh2406 * @Muscraft * @arlosi * @ehuss * @epage * @joshtriplett * @weihanglo   No concerns currently listed.  Once a majority of reviewers approve (and at most 2 approvals are outstanding), this will enter its final comment period. If you spot a major issue that hasn't been raised at any point in this process, please speak up!  See this document for info about what commands tagged team members can give me. |

rust-rfcbot
added
proposed-final-comment-period
Currently awaiting signoff of all team members in order to enter the final comment period.

disposition-merge
This RFC is in PFCP or FCP with a disposition to merge it.
labels
Jun 25, 2026

### **epage** commented Jun 29, 2026

Copy link
 

Copy Markdown

Contributor

|  |
| --- |
| I'm hesitant though unsure yet if its strong enough to raise a blocking concern.  Most of this comes back to #3924 (comment)  When maintainers document this and users adopt dependency overrides, they are making an explicit choice in build time trade offs between full and incremental builds. The baseline this is building from is consistent.  With this feature, there isn't a clear path to having any kind of consistency with how this is applied. Some won't be aware of it. Some may optimize for one workflow, another, or a mix. The user can't predict what is happening and there is no visibility into this.  Theoretically, maybe something similar can be said for `hint-mostly-unused` except   * that is binary * that has much more limited use cases where pretty much the only packages that should set it are `windows-sys` and `aws-sdk`.   Some of the benefits of this might also be reduced enough by other efforts, like rust-lang/cargo#15931, that we should instead put our efforts there. Unsure how this balances out with proc-macro expansion caching and which would be preferred long term. |

ehuss
moved this from **Nominated**
to **FCP merge**
in Cargo status tracker
Jun 30, 2026

joshtriplett
added 2 commits
July 7, 2026 07:42

`Document use cases`

`f2108b3`

```
This should make its way into the documentation of the feature.
```

`87c77bc`

```
…t-level
```

### **epage** commented Jul 8, 2026

Copy link
 

Copy Markdown

Contributor

|  |
| --- |
| Most of this comes back to #3924 (comment)  I brought up my hesitance in the Cargo team meeting and Josh's updates reflect ideas that came from that, including   * Softly encouraging intended uses to try to get some level of consistency with this feature * Finding ways to be transparent to users about this, like with `--timings`   + One big issue is the transitive nature of this. Just showing it in `cargo add` for a direct dependency doesn't tell you what is done deeper down   + Commands using the `cargo update` output are limited by `cargo update` where we might not necessarily have downloaded the `.crate` files to look at this   + Commands like `cargo info` and views like what docs.rs offer additional ways of communicating this   Some of the benefits of this might also be reduced enough by other efforts, like rust-lang/cargo#15931, that we should instead put our efforts there. Unsure how this balances out with proc-macro expansion caching and which would be preferred long term.  While this wasn't necessarily resolved, the overall effort for this is fairly low that putting a lot of investigative burden on this to weigh out the options does not seem worthwhile. |

### **epage** commented Jul 8, 2026

Copy link
 

Copy Markdown

Contributor

|  |
| --- |
| As `phf` might be another motivating case for this, I was asked to benchmark it in `typos` as it finds identifiers and splits them into words and passes them through a very large phf map.  Repo: https://github.com/crate-ci/typos  Commit: bc212b92c93b7d2c8acb5fcb114250694513595b  Benchmarked change:  ``` diff --git c/Cargo.toml w/Cargo.toml index d5127b43..031ba836 100644 --- c/Cargo.toml +++ w/Cargo.toml @@ -93,6 +93,18 @@ zero_sized_map_values = "warn"  [profile.dev]  panic = "abort"  +[profile.dev.package.phf] +opt-level = 3 + +[profile.dev.package.phf_shared] +opt-level = 3 + +[profile.dev.package.unicase] +opt-level = 3 + +[profile.dev.package.siphasher] +opt-level = 3 +  [profile.release]  panic = "abort"  codegen-units = 1 ```  Running:  ``` $ cargo clean && time cargo build -p typos-cli ```  Before: 0m22.007s  After: 0m21.477s  Then when running the binaries within the cargo repo:  ``` $ time ../typos/baseline/debug/typos > /dev/null  real    0m2.311s user    0m26.111s sys     0m0.079s  $ time ../typos/override/debug/typos > /dev/null  real    0m2.400s user    0m27.046s sys     0m0.077s ```  Yes, these aren't very scientific numbers but I figured that we are focusing on end-user impact and don't care as much about single-digit percentage changes. |

rust-rfcbot
added
final-comment-period
Will be merged/postponed/closed in ~10 calendar days unless new substational objections are raised.
and removed
proposed-final-comment-period
Currently awaiting signoff of all team members in order to enter the final comment period.
labels
Jul 28, 2026

### **rust-rfcbot** commented Jul 28, 2026

Copy link
 

Copy Markdown

Collaborator

|  |
| --- |
| 🔔 **This is now entering its final comment period**, as per the review above. 🔔 |

rust-rfcbot
added
finished-final-comment-period
The final comment period is finished for this RFC.

S-waiting-on-review
Status: This is awaiting some action from the reviewer.

to-announce
and removed
final-comment-period
Will be merged/postponed/closed in ~10 calendar days unless new substational objections are raised.
labels
Aug 7, 2026

### **rust-rfcbot** commented Aug 7, 2026

Copy link
 

Copy Markdown

Collaborator

|  |
| --- |
| The final comment period, with a disposition to **merge**, as per the review above, is now **complete**.  As the automated representative of the governance process, I would like to thank the author for their work and everyone else who contributed. |

weihanglo
mentioned this pull request
Aug 7, 2026

1 task

### **weihanglo** commented Aug 7, 2026

Copy link
 

Copy Markdown

Member

|  |
| --- |
| Thanks people! This has passed FCP. Merging.  Further discussion would happen in rust-lang/cargo#17334. Subscribe to track the progress. |

weihanglo
merged commit `583c5cc`
into

rust-lang:master
Aug 7, 2026

joshtriplett
deleted the

cargo-hints-min-opt-level
 
branch
August 21, 2026 08:59

This file contains hidden or bidirectional Unicode text that may be interpreted or compiled differently than what appears below. To review, open the file in an editor that reveals hidden Unicode characters.
Learn more about bidirectional Unicode characters

Show hidden characters

Sign up for free
**to join this conversation on GitHub**.
Already have an account?
Sign in to comment

### Uh oh!

There was an error while loading. Please reload this page.

### Labels

disposition-merge
This RFC is in PFCP or FCP with a disposition to merge it.

finished-final-comment-period
The final comment period is finished for this RFC.

S-waiting-on-review
Status: This is awaiting some action from the reviewer.

T-cargo
Relevant to the Cargo team, which will review and decide on the RFC.

to-announce

### 16 participants

Add this suggestion to a batch that can be applied as a single commit.This suggestion is invalid because no changes were made to the code.Suggestions cannot be applied while the pull request is closed.Suggestions cannot be applied while viewing a subset of changes.Only one suggestion per line can be applied in a batch.Add this suggestion to a batch that can be applied as a single commit.Applying suggestions on deleted lines is not supported.You must change the existing code in this line in order to create a valid suggestion.Outdated suggestions cannot be applied.This suggestion has been applied or marked resolved.Suggestions cannot be applied from pending reviews.Suggestions cannot be applied on multi-line comments.Suggestions cannot be applied while the pull request is queued to merge.Suggestion cannot be applied right now. Please check back later.

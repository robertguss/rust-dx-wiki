https://reddit.com/r/rust/comments/1w4a61z/how_i_managed_multiagent_worktrees_in_a_large
2026-11-16

title: How I managed multi-agent worktrees in a large Rust codebase : r/rust
published_date: 2026-09-01T12:12:04.532Z
final_url: https://www.reddit.com/r/rust/comments/1w4a61z/how_i_managed_multiagent_worktrees_in_a_large/

r/rust
 3mo ago 

u/iltumio

# How I managed multi-agent worktrees in a large Rust codebase




iltumio.dev

Six problems that only show up when a big Rust repo meets ten agents in ten worktrees: snapshots, a shared target dir, its build lock, duplicated compilation, orphaned artifacts, and copy-on-write. One fix each.

Open

I wanted to share my experience working on a large Rust codebase in Omarchy and how I managed to have multiple agents working on multiple worktrees in parallel






 





tmobile
•

Ad

Your phone plan has been calling the shots for too long. Not anymore. Introducing T-Mix by T-Mobile.

Learn More

t-mobile.com


  











Best

Open comment sort options

# Comments Section






diplofocus\_


 3mo ago

AAAAAAAAAAAAAAAAAAAAAAA

Everywhere I look it's just Claude. We're living in the most mundane version of the matrix

iltumio



 2mo ago

You're right, I used claude to do the job and to write the article. What you are missing is how many iteration I did and the effort I put to give claude directions to achieve this, so:  
- do I use AI? yes  
- do I tell AI what to do? yes  
- is AI able to convince me that it's proposed solution is good for my needs? very often, nowadays  
- do I just ask AI to write an article and publish it regardless of the content? no

numberwitch


 2mo ago

dude just run cargo clean when you run outta space bruh





SethDusek5


 3mo ago

I sure am glad we'll be replacing arduous stuff like writing code and thinking so I can focus on stuff like doing the dishes and cleaning

numberwitch


 2mo ago

"farm reddit karma - make no mistakes"





numberwitch


 2mo ago

Hey dude, I just wanted to let you know that i'm not claude yet but I'm becoming claude





forloopy


 3mo ago

Snooze

numberwitch


 3mo ago

“Seperate the code into modules and use a worktree before starting any work.”

Then it’s just down to scoping your features. Ta-da!!!!! Multi agent workflows

That’s my blog post

numberwitch


 3mo ago

Managing target directory is the least boring rust problem there is





insanitybit2


 3mo ago

This is trivializing a much more complex problem, like managing the target directories. You want to split the target directory up so that you can avoid lock contention, but you also want to avoid cold building, and then you have to manage each target dir growing in size independently (1TB is no longer sufficient for rust development tbh), etc. It's much much harder than you're implying.

numberwitch


 2mo ago

I just don't think it's very interesting because I don't run into it. I parallelize agents using worktrees and I don't have this problem because it's easy to avoid the complexity.

So you say "it's trivializing the complex" and I say "its complicating the trivial".

Like... you can just cargo clean. I don't want to read a fucking blog post about someone's claude code session. Sorry but this is the hill i die on.

tafia97300


 2mo ago

https://github.com/mozilla/sccache and https://github.com/holmgr/cargo-sweep work ok for me

iltumio



 2mo ago

I was using sccache, but I migrated to kache-rs that is faster and save space





numberwitch


 2mo ago

yeah, there are existing tools that work and don't rely on false self-intellectualization using llm

u/upwork
•

Ad

Choose hourly or fixed-price work and hire a freelancer who fits your project and budget.

Sign Up

upwork.com

insanitybit2


 3mo ago

I do think that compile times, disk usage, and concurrency are going to be increasingly important. We are leaning in hard with rust at work but we routinely have hundreds of GB of build artifacts, lock contention, build contention, etc. I've ended up with a merge coordination system, sccache, and a bunch of other stuff to try to solve this. Interesting to see some of the work done here.

numberwitch


 2mo ago

only if you suck so bad at making software that you zoom in on "what the target/ dir is doing" instead of building your actual software. navel gazers all of ye

iltumio



 2mo ago

I just wanted to share my experience and how I managed to solve a real problem I had. Everything is explained already in the article, so no need for me to repeat myself.

I personally don't like your style, but I accept your critics.

I probably suck so bad at software like you said, but I still prefer to spend my time building actual software, even if it's bad, instead of spending all of my time to be in the top 1% commenter on reddit.





insanitybit2


 2mo ago

I have no clue what you're on about but you sound like you're in denial. You should embrace rust's flaws, it's how the language improves.

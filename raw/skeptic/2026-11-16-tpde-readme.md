https://github.com/tpde2/tpde
2026-11-16

fetched_with: gh api repos/tpde2/tpde --jq '"full_name: \(.full_name)\ndescription: \(.description)\nstars: \(.stargazers_count)\narchived: \(.archived)\npushed_at: \(.pushed_at)\nupdated_at: \(.updated_at)\ncreated_at: \(.created_at)\nopen_issues: \(.open_issues_count)"'; echo 'latest_release:'; gh api repos/tpde2/tpde/releases/latest --jq '"\(.tag_name) \(.published_at)"' 2>/dev/null; echo; echo '--- README ---'; gh api repos/tpde2/tpde/readme -H 'Accept: application/vnd.github.raw'

full_name: tpde2/tpde
description: A fast framework for writing baseline compiler back-ends in C++
stars: 681
archived: false
pushed_at: 2026-11-15T23:32:59Z
updated_at: 2026-11-11T19:02:31Z
created_at: 2025-05-30T16:31:25Z
open_issues: 9
latest_release:
{"message":"Not Found","documentation_url":"https://docs.github.com/rest/releases/releases#get-the-latest-release","status":"404"}
--- README ---
# TPDE Compiler Back-End Framework

TPDE is a fast compiler back-end framework that adapts to existing SSA IRs.
The primary goal is low-latency compilation while maintaining reasonable (`-O0`) code quality, e.g., as baseline compiler for JIT compilation or unoptimized builds.
Currently, TPDE only targets ELF-based x86-64 and AArch64 (Armv8.1) platforms.

This repository contains:

- TPDE: the core compiler framework.
- TPDE-Encodegen: a utility for easing the use of TPDE by deriving code generators through LLVM's Machine IR.
- TPDE-LLVM: a standalone back-end for LLVM-IR, which compiles 10--20x faster than LLVM -O0 with similar code quality, usable as library (e.g., for JIT), as tool (`tpde-llc`), and integrated in Clang/Flang (with a patch).

For more information and getting started, consult the [documentation](https://docs.tpde.org/).

### Publications

- Tobias Schwarz, Tobias Kamm, and Alexis Engelke. TPDE: A Fast Adaptable Compiler Back-End Framework. [arXiv:2505.22610](https://arxiv.org/abs/2505.22610) [cs.PL]. 2025.

### License

Generally: Apache-2.0 WITH LLVM-exception. (Detailed license information is attached to every file. Dependencies may have different licenses.)


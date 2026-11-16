import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
WORK = Path(sys.argv[1])
ONLY = sys.argv[2:]
RESULTS = HERE / "results.jsonl"
LOGS = HERE / "logs"
MOLD_BIN = WORK / "tools/mold-3.0.0-x86_64-linux/bin"
TRIPLE = "x86_64-unknown-linux-gnu"

PROJECTS = {
    "ripgrep": ("ripgrep", "rg", "crates/core/main.rs", "crates/matcher/src/lib.rs"),
    "helix": ("helix-term", "hx", "helix-term/src/main.rs", "helix-core/src/lib.rs"),
    "atuin": ("atuin", "atuin", "crates/atuin/src/main.rs", "crates/atuin-common/src/lib.rs"),
    "nushell": ("nu", "nu", "src/main.rs", "crates/nu-protocol/src/lib.rs"),
    "meilisearch": ("meilisearch", "meilisearch", "crates/meilisearch/src/main.rs", "crates/milli/src/lib.rs"),
}

NO_DEBUG = ["profile.dev.debug=false"]
CONFIGS = {
    "baseline": ([], False),
    "no-debug": (NO_DEBUG, False),
    "preset": (NO_DEBUG, True),
    "preset+macro-opt": (NO_DEBUG + ["profile.dev.build-override.opt-level=3"], True),
    "deps-no-debug": (['profile.dev.package."*".debug=false'], False),
}

ENV = dict(os.environ, HELIX_DISABLE_AUTO_GRAMMAR_BUILD="1", PATH=f"{MOLD_BIN}:{os.environ['PATH']}")


def run(cmd, cwd, env=ENV):
    start = time.monotonic()
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    elapsed = time.monotonic() - start
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed in {cwd}:\n{proc.stderr[-3000:]}")
    return elapsed, proc.stderr


def config_args(src, settings, mold):
    settings = list(settings)
    if mold:
        minor = int(re.search(r"rustc 1\.(\d+)", subprocess.run(["rustc", "-V"], cwd=src, capture_output=True, text=True).stdout).group(1))
        flags = ['"-Clink-arg=-fuse-ld=mold"']
        if minor >= 90:
            flags.insert(0, '"-Clinker-features=-lld"')
        settings.append(f"target.{TRIPLE}.rustflags=[{','.join(flags)}]")
    return [arg for setting in settings for arg in ("--config", setting)]


def edit(path):
    stamp = time.time_ns()
    with open(path, "a") as handle:
        handle.write(f"\n#[allow(dead_code)]\nfn __killtest_{stamp}() -> u64 {{ {stamp} }}\n")


def rebuilds(path, build):
    times, compiled = [], []
    for _ in range(3):
        edit(path)
        elapsed, stderr = build()
        times.append(round(elapsed, 2))
        compiled.append(len(re.findall(r"^\s*Compiling ", stderr, re.M)))
    return {"times": times, "median": statistics.median(times), "crates_recompiled": compiled[-1]}


def linker_of(binary):
    comment = subprocess.run(["readelf", "-p", ".comment", str(binary)], capture_output=True, text=True).stdout
    for name in ("mold", "LLD"):
        if name in comment:
            return name.lower()
    return "system"


def dir_bytes(path):
    return int(subprocess.run(["du", "-sb", str(path)], capture_output=True, text=True).stdout.split()[0])


def measure(project, config):
    package, binary, leaf, deep = PROJECTS[project]
    settings, mold = CONFIGS[config]
    src = WORK / "src" / project
    target = WORK / f"target-{project}"
    shutil.rmtree(target, ignore_errors=True)
    env = dict(ENV, CARGO_TARGET_DIR=str(target))
    args = config_args(src, settings, mold)
    build_cmd = ["cargo", "build", "-p", package, "--locked", *args]

    def build(*extra):
        return run([*build_cmd, *extra], src, env)

    try:
        clean, stderr = build("--timings")
        shutil.copy(target / "cargo-timings/cargo-timing.html", LOGS / f"{project}-{config}-clean-timing.html")
        result = {
            "project": project,
            "config": config,
            "rustc": subprocess.run(["rustc", "-V"], cwd=src, capture_output=True, text=True).stdout.strip(),
            "commit": subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=src, capture_output=True, text=True).stdout.strip(),
            "clean": round(clean, 2),
            "crates_compiled": len(re.findall(r"^\s*Compiling ", stderr, re.M)),
        }
        result["leaf"] = rebuilds(src / leaf, build)
        result["deep"] = rebuilds(src / deep, build)
        edit(src / deep)
        build("--timings")
        shutil.copy(target / "cargo-timings/cargo-timing.html", LOGS / f"{project}-{config}-deep-timing.html")
        edit(src / leaf)
        _, passes = run(
            ["cargo", "rustc", "-p", package, "--bin", binary, "--locked", *args, "--", "-Ztime-passes"],
            src,
            dict(env, RUSTC_BOOTSTRAP="1"),
        )
        (LOGS / f"{project}-{config}-time-passes.txt").write_text(passes)
        result["linker"] = linker_of(target / "debug" / binary)
        result["binary_bytes"] = (target / "debug" / binary).stat().st_size
        result["target_bytes"] = dir_bytes(target)
        return result
    finally:
        subprocess.run(["git", "checkout", "--", leaf, deep], cwd=src)
        shutil.rmtree(target, ignore_errors=True)


def main():
    LOGS.mkdir(exist_ok=True)
    done = set()
    if RESULTS.exists():
        done = {(row["project"], row["config"]) for row in map(json.loads, RESULTS.read_text().splitlines())}
    for project in ONLY or PROJECTS:
        run(["cargo", "fetch", "--locked"], WORK / "src" / project)
        for config in CONFIGS:
            if (project, config) in done:
                continue
            row = measure(project, config)
            with open(RESULTS, "a") as handle:
                handle.write(json.dumps(row) + "\n")
            print(json.dumps(row), flush=True)


main()

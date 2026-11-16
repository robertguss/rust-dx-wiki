https://api.github.com/search/code (queries: "<action>" path:.github/workflows)
2026-11-16

fetched_with: gh api -X GET search/code -f q='"<action>" path:.github/workflows' --jq .total_count

Swatinem/rust-cache total_count=164864
mozilla-actions/sccache-action total_count=5744
actions-rust-lang/setup-rust-toolchain total_count=15744
Leafwing-Studios/cargo-cache total_count=273
kunobi-ninja/kache total_count=170
runs-on/cache total_count=192

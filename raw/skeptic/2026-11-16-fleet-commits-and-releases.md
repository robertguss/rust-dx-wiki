https://github.com/suptejas/fleet
2026-11-16

fetched_with: gh api 'repos/suptejas/fleet/commits?per_page=5' --jq '.[]|"\(.commit.author.date[:10]) \(.commit.message|split("\n")[0])"'; echo releases:; gh api 'repos/suptejas/fleet/releases?per_page=2' --jq '.[]|"\(.tag_name) \(.published_at[:10])"'; echo issues:; gh api 'repos/suptejas/fleet/issues?state=open&per_page=5' --jq '.[]|"#\(.number) \(.created_at[:10]) \(.title)"'

2023-04-13 edit todo
2023-04-13 edit todo
2023-04-09 edit readme
2023-04-02 readme typo fix
2023-03-04 Update README
releases:
issues:
#129 2026-04-22 chore(deps): bump openssl from 0.10.40 to 0.10.68
#66 2023-06-06 fleet.rs domain unavailable
#63 2023-02-02 missing tags?
#62 2023-01-11 Fleet crashed 
#61 2023-01-08 i can't install it 


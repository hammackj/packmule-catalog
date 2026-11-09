# Packmule catalog

The addon list behind the Browse tab of
[Packmule](https://github.com/hammackj/packmule), the World of Warcraft addon
manager, with the code reviews of each addon's releases. Packmule fetches
`catalog.json` from here at startup, so changes reach everyone without an app
release.

## What's here

- `catalog.json`: the addons. Each entry names the GitHub repository whose
  releases Packmule installs, the game versions it has builds for
  (`flavors`), the folders it installs (used to recognise hand-installed
  copies), and optionally a release stream (`tagPrefix`) and other entries it
  needs (`requires`).
- `verified`: someone checked the repository is the author's official one,
  and whether its zips are built by CI.
- `reviews` and `reviews/`: Claude and Codex reviews of specific release
  zips, pinned by SHA-256. How they work and what they look for is in
  [REVIEWS.md](REVIEWS.md).

## Adding an addon

An addon qualifies when its official GitHub repository publishes releases with
a packaged `.zip` (the BigWigs packager's `release.json` lets Packmule pick
the right build per game version).

1. Add an entry to `catalog.json`.
2. From a [Packmule](https://github.com/hammackj/packmule) checkout next to
   this one, fill in its flavors and folders from the latest release:
   `GITHUB_TOKEN=$(gh auth token) cargo run --example update-catalog`
3. Optionally review it: `cargo run --example review -- <id>` (see
   [REVIEWS.md](REVIEWS.md)).
4. `python3 scripts/check.py`, then open a pull request. CI runs the same
   check.

## License

MIT

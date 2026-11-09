# Spoken: Bosses (English) bosses-audio/v1.0.0

- Repository: https://github.com/rusty-key/spoken-wow
- Reviewed: 2026-11-09
- Scope: all of the code
- Verdicts: Claude **pass**, Codex **pass**

Zips (SHA-256):

- `SpokenBossesAudio-1.0.0.zip` `9d023d923bbf7894d0f92fec025ff99bbfb64cba42b86d1659874f422e1e71d6`

Pre-scan:

```
Mail / gold: 0
Trade / gold: 0
Guild bank / guild: 0
Auction house: 0
Uses or moves bag items: 0
Destroys items: 0
Chat / whispers: 0
Addon messages: 0
Runs code from strings: 0
Macros / bindings: 0
Logout / quit: 0
Links / addresses: 0
Escaped bytes: 0
Very long lines: 0
Files that aren't addon files: 0
```

## Claude

## Report: Spoken Audio: Bosses (English) v1.0.0

**What it does:** This is a data-only audio pack for the "Spoken" addon. It has about 277 files, mostly narrated boss-lore MP3s under `Sounds/<mapID>/`, plus one icon `.tga`, a README, a `.toc` and one Lua file.

**Code reviewed (all of it):**
- `SpokenBossesAudio.toc` loads only `Data/Sounds.lua`. The metadata is benign: a title, a license note and credits to warcraft.wiki.gg. It has no URLs and no text addressed to a reviewer.
- `Data/Sounds.lua` is auto-generated. Lines 8–358 are a table that maps boss names to `file`, `len` and `times` (word timings). Lines 362–375 do three things:
  - read the `.toc` metadata through `GetAddOnMetadata`;
  - fill in the `pack` fields;
  - register the pack in the global `SpokenBossesAudioPacks[ADDON_NAME]`.
- I checked for `loadstring`, `RunScript`, `load(`, `_G`, `getfenv`, `SendChat`, `Mail`, and escaped-byte or hex strings across the Lua, `.toc` and README files. There were no matches. The table strings are plain paths and numbers, with no embedded code or blobs.

**Risky behaviours checked:**
- **Prescan:** `REVIEW_PRESCAN.txt` reports no risky API hits and no unusual files.
- **Gold, items and mail:** there are no API calls for mail, trade, the auction house, the guild bank or item deletion.
- **Chat and addon messages:** there are no chat, whisper, Battle.net or `SendAddonMessage` calls.
- **Hidden code:** there are no string-to-code execution calls and no obfuscation.
- **Phishing:** the only links are CurseForge pages for the author's own project, and they appear in the README only.
- **Macros, keybindings and logout:** none.
- **Non-addon files:** the only file types are `.mp3`, `.tga`, `.lua`, `.toc` and `.md`. There are no executables or scripts. I globbed for common script and binary extensions and found none.

**Concerns:** None. The one global it writes (`SpokenBossesAudioPacks`) is a namespaced registry that the parent addon reads.

VERDICT: PASS

## Codex

This release is an English boss narration pack for Spoken. I reviewed all code under `builds/` and checked the manifest, README, data tables, and file types.

Paths below are relative to `builds/SpokenBossesAudio-1.0.0/SpokenBossesAudio/`.

- **Prescan:** `REVIEW_PRESCAN.txt:1` says “No risky APIs or unusual files found.” Code inspection supports that result.
- **Execution and data:** `SpokenBossesAudio.toc:23` loads only `Data/Sounds.lua`. Its 272 boss entries contain literal audio paths, durations, and numeric timestamps. Lines 362–370 read addon metadata; lines 374–375 register the pack using `SpokenBossesAudioPacks[ADDON_NAME] = pack`. No hidden code, string execution, timers, or event handlers were found.
- **Gold, items, and player control:** No mail, trade, auction, guild-bank, item destruction, macro, binding, or logout operations.
- **Communication and phishing:** No chat, whispers, Battle.net messages, addon messages, or player-data transmission. README links at lines 1, 3, and 15 point to related addon pages and lore attribution; no phishing interface was found.
- **Package contents:** One Lua file, one TOC, one README, 272 files identified as MPEG audio, and one TGA image. No standalone executables or scripts, or reviewer-directed instructions, were found.

No malicious behavior identified. This assessment covers this audio pack, not the separately installed Spoken addon.

VERDICT: PASS (nothing malicious)

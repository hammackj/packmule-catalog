# Spoken: Books (English) readables-audio/v2.3.0

- Repository: https://github.com/rusty-key/spoken-wow
- Reviewed: 2026-11-09
- Scope: all of the code
- Verdicts: Claude **pass**, Codex **pass**

Zips (SHA-256):

- `SpokenReadablesAudio-2.3.0.zip` `7ef8d681a54b8b36c3096763795d45ec85f086df1135a70668f9fe7695bebbfa`

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

**Report: Spoken Audio: Readables (English) v2.3.0**

**What it does:** This is a data-only audio pack for the Spoken Readables addon. The zip holds:
- a `.toc` file
- one Lua file, `Data/Sounds.lua`
- `README.md`
- `Textures/AddonIcon.tga`
- about 1,140 `.mp3` narration clips

**Code review:**
- `Data/Sounds.lua` has 1,159 lines. Lines 14–1156 are a plain table that maps page IDs to a file name and a clip length, such as `[15] = { file = "15", len = 21.394 }`.
- The only executable lines are at the end. They register the table as `SpokenReadablesAudioPacks[ADDON_NAME] = pack` (lines 1158–1159).
- There are no function calls, no `loadstring`, `load` or `RunScript`, no escaped bytes and no encoded blobs.
- I searched for anything that isn't a table entry, and the only hits were the header comments, the table setup and those two registration lines.

**Risky behaviours checked:**
- **Gold, items, mail, trade, auction house, deletion:** none. The prescan found no risky APIs.
- **Chat, whispers, addon messages, data leaks:** none.
- **Hidden code or obfuscation:** none.
- **Phishing:** the README links to the CurseForge page for the parent addon and to the author's Buy Me a Coffee page. That is the author's own project and donation link, and it's in the README only, not shown in-game.
- **Macros, key bindings, logout:** none.
- **Non-addon files:** none. The only files besides `.mp3`, `.lua`, `.toc` and `.md` are the `.tga` icon. I did not parse the mp3 or tga contents, but WoW only plays or displays them.
- **Instructions aimed at an AI or reviewer:** none found in the files I read (`.toc`, README and `Sounds.lua`).

**Concerns:** none. The addon is inert data that matches its description.

VERDICT: PASS

## Codex

This release is an English narration data pack for Spoken’s Readables module. I reviewed all code under `builds/`, its manifest and README, and the prescan.

Paths below are relative to `builds/SpokenReadablesAudio-2.3.0/SpokenReadablesAudio/`.

- **Code and hidden execution:** `SpokenReadablesAudio.toc:12` loads only `Data/Sounds.lua`. Its 1,134 page entries contain numeric filenames and durations. Lines 1158–1159 simply register the table: `SpokenReadablesAudioPacks[ADDON_NAME] = pack`. No dynamic execution, obfuscation, callbacks or timers.
- **Gold, items and destructive actions:** No mail, trade, auction, bank, item deletion, macro, binding or logout operations.
- **Messages and data leakage:** No chat, whisper, Battle.net or addon-message calls, and no player-data collection.
- **Phishing and reviewer manipulation:** README lines 3 and 17 contain ordinary project and donation links. No fake Blizzard messages, phishing UI or text targeting AI reviewers.
- **Packaged files:** Found one Lua file, manifest, README, 1,139 MP3s and one TGA image. File-type checks identify the media as audio/image files; no external scripts, executables or symlinks.
- **Prescan:** `REVIEW_PRESCAN.txt:1` reports “No risky APIs or unusual files found.” Code inspection agrees.

No malicious behavior found. This assessment covers the supplied audio pack; the separate Spoken playback addon is outside this review.

VERDICT: PASS

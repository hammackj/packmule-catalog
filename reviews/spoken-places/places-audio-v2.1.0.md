# Spoken: Zones (English) places-audio/v2.1.0

- Repository: https://github.com/rusty-key/spoken-wow
- Reviewed: 2026-11-09
- Scope: all of the code
- Verdicts: Claude **pass**, Codex **pass**

Zips (SHA-256):

- `SpokenPlacesAudio-2.1.0.zip` `dc61d74619f40d7f91fa2ab8e547046a43dadac82d6095e07dd82ea335196e4b`

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
Files that aren't addon files: 1
```

## Claude

# Spoken Audio: Places 2.1.0 review

**What it does:** This is a data-only audio pack for the Spoken addon. It contains about 847 narrated zone and subzone mp3 files, one icon texture, a README, a `.toc` file and one Lua file, `Data/Sounds.lua`. It registers a table of file paths and durations in the global `SpokenPlacesAudioPacks`. It also reads its own `.toc` metadata (quality, bitrate, version, language) with `GetAddOnMetadata`.

**Checks**
- **`Data/Sounds.lua` (all 978 lines):** Lines 11–950 are a plain table of `file = "…", len = …` entries. Lines 955–977 are the only logic: metadata reads and the registry assignment. A grep for `loadstring`, `RunScript`, `load(`, `_G`, `setfenv`, escaped-byte sequences, `SendChat`, `SendMail` and `SendAddon` found nothing. There is no code built from strings, no obfuscation, and no gold, item, mail, chat or addon-message APIs.
- **`.toc`:** It loads only `Data/Sounds.lua`. The comments are ordinary developer notes, and none of the text is addressed to a reviewer or an AI.
- **README:** It links to the author's CurseForge page, spoken.rusty.one and a buymeacoffee donation page. These are the author's own project and support links, which is normal. The addon shows no popups and no in-game links.
- **Prescan hit:** `Sounds/.from-takes` is a 0-byte hidden file. It is empty and harmless. It looks like a leftover from the author's build tooling, so it is odd but not a finding.
- **Non-addon files:** I found no executables or scripts in the zip. I searched with a glob for files not ending in `3`, which surfaced only the `.toc`, `.tga`, `.md`, the dotfile and the `.lua`. I did not open the mp3s or the `.tga`, since WoW only plays or renders them.
- **Limit of the check:** The mp3 count and the absence of other file types come from the file listing, which was truncated at 100 of 847 entries. The non-mp3 glob was not truncated.

**Concerns:** None.

VERDICT: PASS

## Codex

This is an English zone narration pack containing 841 MP3s, an icon, and one Lua file. Its code registers sound paths, durations, and pack metadata for Spoken to use.

Reviewed all executable code under `builds/` and checked the large sound table for embedded code. Paths below are relative to `builds/SpokenPlacesAudio-2.1.0/SpokenPlacesAudio/`.

- **Gold, items, and destructive actions:** No mail, trade, guild bank, auction, or item/mail deletion calls.
- **Messaging and data leaks:** No chat, whisper, Battle.net, or addon-message calls. `Data/Sounds.lua:977` only registers the local table: `SpokenPlacesAudioPacks[ADDON_NAME] = pack`.
- **Hidden code and automation:** No string execution, obfuscation, timers, event handlers, macro/binding changes, or logout calls. `Data/Sounds.lua:955–967` reads addon metadata and converts the bitrate to a number.
- **Phishing and reviewer manipulation:** No instructions addressed to an AI or reviewer. README links concern the project, feedback, donations, and lore attribution (`README.md:1,9,23,27`); no account/support impersonation or in-game phishing interface.
- **Prescan finding:** Its only hit is `Sounds/.from-takes` (`REVIEW_PRESCAN.txt:2`). Confirmed empty, so it contains no executable payload. File-type checks identified the media as MP3 audio and a TGA image; no external scripts or executables were found.

No malicious behavior found in this package. The separate Spoken addon is outside this review.

VERDICT: PASS (nothing malicious)

# Spoken: Quests (English) quests-audio/v2.5.0

- Repository: https://github.com/rusty-key/spoken-wow
- Reviewed: 2026-11-09
- Scope: all of the code
- Verdicts: Claude **pass**, Codex **pass**

Zips (SHA-256):

- `SpokenQuestsAudioAll-2.5.0.zip` `bbe702b71f00f8c3586b6fd1c7d74ba67581449513b558627dfdc9787b0eb790`

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
Runs code from strings: 4
Macros / bindings: 0
Logout / quit: 0
Links / addresses: 0
Escaped bytes: 0
Very long lines: 0
Files that aren't addon files: 0
```

## Claude

# Spoken: Quests (English) audio data, v2.5.0 review

## What it is
This release has four data-only sub-addons: `SpokenQuestsAudioShared`, `Alliance`, `Horde` and `Gossip`. They hold about 15,000 `.ogg` voice files plus generated Lua lookup tables. Each is a load-on-demand module for the parent "Spoken Quests" (VoiceOver) addon, and each registers itself with `VoiceOver.DataModules:Register(...)`. All the logic is a short `Module.lua` per module, which turns a file name and event into a sound path such as `generated\sounds\quests\%s.ogg`.

## Checks
- **Prescan hits (4).** These are `setfenv(1, VoiceOver)` at line 6 of each `Module.lua`. It only switches the function's environment to the VoiceOver table so `Enums` and `format` resolve. It takes no string input and runs no dynamic code. I read all four `Module.lua` files and they are identical apart from the module name. This is not a finding.
- **Hidden code.** A grep across all files for `loadstring`, `RunScript`, `load(`, `getfenv`, `_G[`, and escaped-byte or hex patterns returned nothing.
- **Gold, items, mail, trade, auction, guild bank, deletion.** No API calls for any of these exist. A grep for `Send*`, `Delete*` and `Pickup*` in the generated files only matched quest and item names, such as "Gold Pickup Schedule" and "An Easy Pickup".
- **Chat, addon messages, and data leaks.** There is no `SendChatMessage`, `SendAddonMessage` or Battle.net call anywhere.
- **Phishing and URLs.** There are no URLs and no popups.
- **Macros, bindings, logout.** None.
- **Generated Lua tables.** A regex for any line that isn't a table entry, brace, comment or the first two lines of each file found only two things. The first line of each file is `if not VoiceOver ... then return end`. The second is a table assignment such as `SpokenQuestsAudioShared.X = {`. The files contain no functions and no code beyond table data. I did not read every row.
- **Non-addon files.** The prescan lists none. The Lua, TOC and `.ogg` files are all expected addon files. A file-type glob for `.exe`, `.sh`, `.bat`, `.py`, `.js`, `.dll` and `.ps1` returned nothing in the first 100 hits, but I could not list the whole tree. I only inspected the `.ogg` files by file name, not their contents. The `.toc` file I read (Shared) is normal.
- **Text aimed at a reviewer.** None found.

## Concerns
None. I could not run Bash in this session, so the file-type check was done with glob and grep rather than a full file listing.

VERDICT: PASS

## Codex

This release supplies quest and NPC dialogue audio for Spoken/VoiceOver through Alliance, Horde, Shared, and Gossip modules.

Reviewed all four modules and manifests, skimmed the generated data, and statically checked all 104 generated Lua files: each contains only a dependency guard and a literal lookup-table assignment.

- **All four prescan hits are harmless:** `setfenv(1, VoiceOver)` appears at line 6 of `Module.lua` in `SpokenQuestsAudioAlliance`, `SpokenQuestsAudioGossip`, `SpokenQuestsAudioHorde`, and `SpokenQuestsAudioShared`, under `builds/SpokenQuestsAudioAll-2.5.0/`. It selects the function’s namespace. Lines 7–12 format local `.ogg` paths; no strings are executed.
- **Gold, items, and player communication:** No code sends mail, trades, operates auctions or guild banks, destroys items, sends chat/Battle.net/addon messages, or transmits player data.
- **Hidden code and account manipulation:** No dynamic code loading, obfuscated executable payloads, macro/key-binding changes, forced logout, phishing links, or reviewer-directed instructions found.
- **Archive contents:** Only Lua, addon manifests, four TGA icons, and 14,925 Ogg audio files occur under `builds/`. Audio headers match Ogg/Vorbis. No external executables or installation scripts found.

No malicious behavior found in this package. The separate Spoken/VoiceOver core is outside this review.

VERDICT: PASS (nothing malicious)

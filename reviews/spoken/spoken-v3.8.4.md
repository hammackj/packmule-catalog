# Spoken spoken/v3.8.4

- Repository: https://github.com/rusty-key/spoken-wow
- Reviewed: 2026-11-09
- Scope: all of the code
- Verdicts: Claude **pass**, Codex **pass**

Zips (SHA-256):

- `Spoken-3.8.4.zip` `746192ebe1a9de2ad34d19c85884f9161532bf3b6bd400bb78cdadb478ff3c8d`

Pre-scan:

```
Mail / gold: 0
Trade / gold: 0
Guild bank / guild: 0
Auction house: 0
Uses or moves bag items: 2
Destroys items: 0
Chat / whispers: 0
Addon messages: 0
Runs code from strings: 104
Macros / bindings: 3
Logout / quit: 0
Links / addresses: 8466
Escaped bytes: 0
Very long lines: 256
Files that aren't addon files: 0
```

## Claude

# Spoken 3.8.4 review

## What it does
Spoken is a voice and subtitle addon for WoW. It has these modules:
- `Spoken` is the core, with the sound queue, subtitles, options and a transcript/compendium UI.
- `Spoken_Quests` is a fork of the VoiceOver addon. It plays voiced quest and gossip text and bundles Ace3 libraries.
- `Spoken_Bosses`, `Spoken_Places` and `Spoken_Readables` handle boss stories, zone lore and book reading.

Most of the zip is data: story text, subzone tables with warcraft.wiki.gg source links, locale files and textures.

## Risky behaviours checked
- **Bag items (`Spoken_Readables/Opener.lua:111-114`):** this is a `hooksecurefunc` post-hook on `C_Container.UseContainerItem`. It only records which item id was right-clicked, so it can work out which book opened. It does not use, move or pick up items.
- **Code from strings:** every prescan hit is `setfenv(1, SpokenEnv)` or `setfenv(1, VoiceOver)`. These are environment sandboxes, documented in `Spoken/Environment.lua:1-31`. `getfenv(0)` there only grabs `_G` for the `__index` fallback. The one `loadstring` hit is `AceAddon-3.0.lua:49`, a local alias in the stock Ace library, and it is never called on built or downloaded strings. I found no `RunScript` or `load` on dynamic strings.
- **Key bindings (`Spoken/UI/Options.lua:610-622`):** `SetBinding` runs only when the player picks a key for one of Spoken's own bindings in its options (`BINDINGS` list, `Bindings.xml`). It refuses in combat. If the key is already taken, it asks the player to confirm first (`Options.lua:630-634`).
- **Chat, mail, trade, auction and logout:** a grep of the whole build found no `SendChatMessage`, `SendAddonMessage`, `C_ChatInfo`, mail, trade, auction, guild bank, `DeleteCursorItem`, macro or logout calls. The addon has no outbound messaging.
- **Links and phishing:** URLs are the author's own (spoken.quest, the GitHub repo, CurseForge, Wago, Discord, Buy Me a Coffee) plus wiki source links in data. The `CopyLink.lua` files (Readables, Bosses, Places) show a StaticPopup with a read-only, pre-selected edit box so the player can copy the address. Nothing opens a browser or posts to chat. `Spoken/Contribute.lua` only builds a `spoken.quest/contribute#e1=…` URL from base64url-compressed text, which the player copies by hand. The `Core.lua:696-715` popup lists old Spoken folders the addon disabled and offers a reload. This is not a scam prompt.
- **Obfuscation:** the long lines in the prescan are story text in `Spoken_Bosses/Data/Stories.lua`. The escaped bytes (for example `\226\128\153` and `\194\160`) are plain UTF-8 punctuation and pattern ranges for text handling, not hidden code. `LibDeflate` is a standard compression library. I did not read the other long-line files in the prescan beyond `Stories.lua`. They are data tables, and the greps over the whole build turned up no code in them.
- **Non-addon files:** a glob for `.exe`, `.dll`, `.sh`, `.bat`, `.py`, `.js`, `.ps1`, `.jar`, `.vbs`, `.cmd`, `.so`, `.dylib` and `.zip` found nothing. The zip holds only `.lua`, `.xml`, `.toc`, `.md` and texture files (`.tga`, `.blp`).
- **Text aimed at a reviewer or AI:** I found none in the files I read.

## Limits of this review
I read the prescan hits and every risky-API match across the build. I read the code files behind those hits in full: `Opener.lua`, `CopyLink.lua`, `Environment.lua`, the binding code in `Options.lua` and the `Core.lua` popup. I did not read every UI file line by line. The greps were broad, and I confirmed none of the other files call any harmful API.

## Concerns
None found.

VERDICT: PASS

## Codex

Spoken adds narration and subtitles for quests, NPC dialogue, books, locations, and boss stories. Static inspection found no malicious behavior.

Paths below are relative to `builds/Spoken-3.8.4/`.

- **Gold, items, and mail:** No transfer or destruction calls found. `Spoken_Readables/Opener.lua:112` uses `hooksecurefunc(container, "UseContainerItem", ...)` only to identify a book the player opened. AceGUI’s `ClearCursor()` calls finish user drag-and-drop into text fields; they do not delete items.
- **Chat and data transmission:** No outgoing chat, whisper, Battle.net, or addon-message calls found. NPC-chat listeners trigger narration. Debug simulations use local `DEFAULT_CHAT_FRAME:AddMessage` and playback callbacks (`Spoken_Quests/Followup.lua:370`, `:399`).
- **Code from strings:** The `setfenv` hits establish addon namespaces (`Spoken/Environment.lua:18`, `Spoken_Quests/Environment.lua:27`); `Spoken/UI/Actions.lua:542` changes a defined function’s environment. AceAddon’s `loadstring` reference is an unused local alias (`Spoken_Quests/Libs/AceAddon-3.0/AceAddon-3.0.lua:49`). No string-execution path found. Compression/base64 produces contribution links, not executable payloads (`Spoken/Contribute.lua:83`).
- **Bindings and reloads:** `SetBinding(key, name)` is reached through the player’s settings interaction, with confirmation before replacing another action (`Spoken/UI/Options.lua:610`). The four bindings control playback and the compendium (`Spoken/Bindings.xml:7`). Reloads require button acceptance; no forced logout found.
- **Links and collection:** Links lead to project, distribution, community, donation, or reference pages—not account-verification prompts. Missing-line collection is **enabled by default**, but stored locally (`Spoken/Gather.lua:42`). Sharing requires copying a link or uploading saved data. Contribution code replaces player-name tokens and excludes mail (`Spoken_Quests/Contribute.lua:283`; `Spoken_Readables/Contribute.lua:111`).
- **Packaged files and long lines:** Long lines contain localized lore data. No separate executable or installer script found. LibDeflate’s command-line file operations are guarded by `if io and os and debug and _G.arg then`, unavailable inside WoW (`Spoken/Libs/LibDeflate/LibDeflate.lua:3370`).

Two additional observations: older conflicting addon folders are automatically disabled with a displayed explanation (`Spoken/Core.lua:688`). AI-related comments describe diagnostic exports (`Spoken/Developer.lua:85`; `Spoken/API.lua:911`, `:947`); they contain no instructions addressed to this reviewer or attempts to influence the verdict.

VERDICT: PASS

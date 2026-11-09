# Plater Plater-v663

- Repository: https://github.com/Tercioo/Plater-Nameplates
- Reviewed: 2026-11-09
- Scope: all of the code
- Verdicts: Claude **pass**, Codex **unsure**

Zips (SHA-256):

- `Plater-v663.zip` `fb7125dea1d09f3896dc8154b40745efeb4d696f44357bd89f50ed9ef48d2136`

Pre-scan:

```
Mail / gold: 4
Trade / gold: 10
Guild bank / guild: 4
Auction house: 0
Uses or moves bag items: 0
Destroys items: 0
Chat / whispers: 16
Addon messages: 17
Runs code from strings: 35
Macros / bindings: 6
Logout / quit: 0
Links / addresses: 96
Escaped bytes: 0
Very long lines: 9
Files that aren't addon files: 4
```

## Claude

# Plater v663: security review

## What it does
Plater is a nameplate customization addon. It includes a scripting and mod system with a code editor, and import/export of profiles and scripts, compatible with wago.io. The libraries are Ace3, the DetailsFramework (`libs/DF`), LibDeflate, LibCompress, LibCustomGlow and similar. I read the prescan hits and the code around each one. I did not read every line of the large data and library files.

## Risky behaviours checked

**Mail, trade, guild bank, macros, guild commands, `RunScript`, `loadstring`/`setfenv` (Plater.lua:13098–13141, fw.lua:6674–6711)**
- These are not calls. They are entries in a blocklist (`privateFunctions`) that hides these APIs from user-written Plater scripts.
- `buildShadowTable` returns `nil` for each listed key, so scripts cannot reach `SendMail`, `AcceptTrade`, `C_AuctionHouse`, `C_GuildBank`, `CreateMacro`, `SetBindingMacro`, `GuildDisband` or `loadstring`.
- This is protective. `DF/fw.lua` has the same list.

**`loadstring` in Plater.lua:13372, 13424, 13637 and 13767**
- This is the legitimate mod and script engine. Plater compiles the Lua the user has stored or imported as mods and scripts.
- The compiled code runs inside the restricted environment above via `SetPlaterEnvironment`, which calls `setfenv`.
- As with WeakAuras, this is by design. Imported scripts are user-chosen, and the sandbox blocks the harmful APIs.

**`loadstring` in Plater_ScriptingPanels.lua:1781**
- It only syntax-checks the editor text with `"return " .. text`. The result is never called.

**`loadstring` in the DF widget files (`button.lua`, `dropdown.lua`, `panel.lua` and others)**
- The pattern is `loadstring("return _G['"..object:GetName().."']:"..funcName.."(...)")`.
- This is the standard DetailsFramework method-forwarding shim. It builds strings from widget names and method names inside the library, not from external data.

**`LibCompress.lua:1665–1666`**
- It builds encode and decode functions from a table of escape characters. This is a known, standard library pattern. It is not obfuscation.

**Chat and addon messages**
- The `ChatThrottleLib` and `AceComm` hits are the stock Ace library code.
- Plater's own sends are in `Plater_Comms.lua:107, 110, 1004, 1067` and `Plater_ImportExport.lua:547, 550`.
  - They go on Plater's own comm prefix to RAID or PARTY, or to a sharing channel.
  - They carry script messages, a script group the player chose to export, and NPC/cast colour customization data.
  - The NPC/cast data includes `UnitName`, `GetRealmName` and `UnitGUID` as sender identification. That is normal.
- On receive, `CommReceived` (`Plater_Comms.lua:137`) only dispatches to a fixed handler table.
  - Received script groups go through `Plater.ScriptReceivedFromGroup`, which is a prompt-based import path. I did not read it in depth.
  - Received script messages are dispatched as data to existing hooks.
- `Plater.SendComm` is only compiled into the "Send Comm Message" hook, which is verified by `VerifyScriptIdForComm`.
- I found no `SendChatMessage` call that Plater itself makes.

**Links**
- The URLs are `wago.io`, `curseforge`, `discord.gg/AGSzAZX`, `patreon` and `youtube`, plus library headers and XML schema namespaces.
- They are shown as copyable text boxes. Nothing opens a browser or sends a chat link.

**`ReloadUI`**
- It is only called from user-confirmed prompts or options buttons. It does not log the player out.

**Non-addon files**
- `Plater/Plater` is the `.toc` file without its extension. It contains a normal file list.
- The others are `LibDeflate` docs (`config.ld`, `ldoc.css`) and `stylua.toml`. All are harmless.
- There are no executables or scripts targeting the person unpacking the zip.

**Long lines in `Plater_ScriptLibrary.lua`**
- Lines of 3 to 6 KB are built-in script templates, which I did not read in full. They are stored as strings for the mod library.

**Hidden text addressed to a reviewer or AI**
- None found in the files I read.

## Concerns
None. The `loadstring` and comm features are the addon's documented scripting system. The addon sandboxes that system and blocks the gold and item, mail, macro and guild APIs from it.

VERDICT: PASS

## Codex

Plater customizes nameplates, health and cast bars, aura indicators, and user-written Lua scripts.

**No confirmed malicious behavior found. However, I did not complete the requested reading of every code file under `builds/`; this first review remains incomplete.**

Checks completed (paths below are relative to `builds/Plater-v663/Plater/`):

- **Gold, items, guild actions, and macros:** Prescan matches are blocklist entries, including `["SendMail"] = true` in `Plater.lua:13102` and `libs/DF/fw.lua:6675`. The inspected paths contain no transfers, item destruction, or malicious macro changes.
- **Chat and Battle.net:** Calls in `libs/AceComm-3.0/ChatThrottleLib.lua:540–684` implement generic messaging wrappers and throttling. No unsolicited-chat caller was found.
- **Addon communications:** `Plater_Comms.lua:59–110` sends character name, realm, GUID, and script payloads to party/raid channels. Lines 1004 and 1067 send NPC/cast customizations through the guild channel. These support group sharing; no gold or account-data exfiltration was found.
- **Received Lua:** Incoming scripts enter `ScriptsWaitingApproval` at `Plater_ImportExport.lua:524–527`. The acceptance callback calls `Plater.AddScript(scriptObject)` at line 577. Compilation uses `loadstring` in `Plater.lua:13372`, `13424`, `13637`, and `13767`; these implement the advertised scripting feature.
- **Other string execution:** `Plater_ScriptingPanels.lua:1781` checks syntax without invoking the result. DetailsFramework generates widget-method wrappers; LibCompress generates encoding functions (`libs/LibCompress/LibCompress.lua:1665–1666`).
- **Encoded content:** Decoded all 61 bundled script strings and inspected their distinct code. They implement display effects and indicators; no malicious payload was found. The remaining long lines at `Plater_ScriptLibrary.lua:652` and `654` are identical aura-layout code inside a commented-out patch.
- **Links and unusual files:** Inspected links concern projects, documentation, or script sharing. The four unusual files are a manifest, documentation configuration, CSS, and formatter configuration. No executable payload or reviewer-directed instructions were found.

**Concern:** Imported scripts execute Lua, so this assessment cannot cover subsequently imported content. A complete source review is still needed before issuing a first-review PASS.

VERDICT: UNSURE

## Maintainer sign-off

Passed by hammackj on 2026-11-09 (Claude: pass, Codex: unsure): Codex found nothing malicious but didn't finish reading every file of this large addon; Claude passed it. Plater runs scripts players import, which a review of the addon itself can't cover.

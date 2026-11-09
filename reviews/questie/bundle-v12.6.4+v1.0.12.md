# Questie bundle/v12.6.4+v1.0.12

- Repository: https://github.com/Questie/Questie
- Reviewed: 2026-11-09
- Scope: all of the code
- Verdicts: Claude **pass**, Codex **unsure**

Zips (SHA-256):

- `Questie-v12.6.4+v1.0.12.zip` `47c990587950c9977af2ec1a4f1c9cf0414bbe400eabcedb8a4509226cb1bc76`

Pre-scan:

```
Mail / gold: 0
Trade / gold: 0
Guild bank / guild: 0
Auction house: 0
Uses or moves bag items: 0
Destroys items: 3
Chat / whispers: 18
Addon messages: 17
Runs code from strings: 6
Macros / bindings: 1
Logout / quit: 0
Links / addresses: 337
Escaped bytes: 0
Very long lines: 6
Files that aren't addon files: 0
```

## Claude

# Questie v12.6.4 (bundle v1.0.12) security review

**What it does:** Questie is a quest helper addon. It puts quest givers, objectives and turn-ins on the map and minimap and tracks quests. The bundle is mostly large static quest, NPC, item and zone data (`QuestieDB/`, `Database/`). The rest is ordinary UI and logic plus the usual Ace3 libraries, including AceComm and ChatThrottleLib.

## Prescan hits checked

- **Item destruction:** `QuestEventHandler.lua:244-253` only *hooks* `DeleteCursorItem` with `hooksecurefunc`. When the player deletes a quest item, the hook refreshes the quest state. It does not delete anything itself. Not a problem.
- **Chat:** The ChatThrottleLib hits are the standard library throttling and wrapping send functions. The two real senders are both normal Questie features:
  - `QuestieAnnounce.lua:202` posts quest-progress announcements to RAID, INSTANCE_CHAT or PARTY. It only does so when the player has enabled the option, and it has a "shut up" setting.
  - `QuestieSlash.lua:235` sends an EMOTE with the player's quest count, but only for the explicit `/questie flex` command.
- **Addon messages:** All hits are in AceComm and ChatThrottleLib. I saw no addon-message code that sends gold, character or account data. `QuestieComms.lua` is the group quest-sync feature. It only uses `string.char` to decode quest packets, and I found no `loadstring` or `RunScript` fed from received messages.
- **Code from strings:**
  - `SupportValidation.lua:90` runs `loadstring` on the bundled data strings, for example `[[return { ... }]]` in `QuestieDB/support/Zones/subZoneToParentZone.lua:6`. The input is static table literals shipped in the addon, and the call is wrapped in `pcall`. Its own comment says it catches malformed data rather than untrusted code.
  - `QuestsByZoneTab.lua:141` runs `loadstring` on that same bundled string. It is not built from network or user input.
  - The `AceAddon`, `AceBucket` and `LibSharedMedia` hits are only local aliases of `loadstring` and `getfenv(0)`. The `overlay.lua:212` hit is a function named `lookups.load`, not Lua's `load`.
- **Key binding:** `QuestieJourney.lua:222` sets `;` to Questie's own "Toggle My Journey" binding. It does this once, and only if the key is unbound and the player has no existing binding for that action.
- **Links:** Nearly all of the 337 hits are wowhead and GitHub URLs in comments or in help text for the author's project page. The only live URLs are the Questie Discord invite (`QuestieDebugOffer.lua:724`, shown in an edit box for the player to copy) and a wowhead link builder in `TrackerMenu.lua:425`. No phishing or "account/support" text.
- **Long lines:** The six hits in `sodBaseNPCs.lua` are long NPC data rows. They are not obfuscated code.

## Other checks

- I found no executables or scripts in the zip. A glob for `.exe`, `.dll`, `.sh`, `.bat`, `.ps1`, `.py`, `.js` and similar returned nothing.
- I found no mail, trade, auction, guild bank, `RunScript`, macro-editing, logout or hex-escaped code in the Lua. A grep for these APIs matched only the `string.char` uses above.
- I found no text addressed to an AI or a reviewer.

I did not read every line of the data files. I skimmed and searched them for embedded code and found none.

**Concerns:** None. The behaviours that need scrutiny are explicit, user-controlled features.

VERDICT: PASS

## Codex

Questie provides quest maps, objective tracking, tooltips, quest history, and group progress sharing. **I found no confirmed malicious payload, but a privacy issue needs human review before approval.**

Paths below are relative to `builds/Questie-v12.6.4+v1.0.12/`.

- **Concern — quest progress disclosed to an unchecked requester.** `Questie/Modules/Network/QuestieComms.lua:1036–1076` accepts legacy addon messages without checking group membership. At line 939, a request triggers `BroadcastQuestLogV2(..., "WHISPER", self.playerName)`. Lines 656–658 require the *recipient* to be grouped, but never verify that the requester belongs to that group. Lines 741–757 send quest IDs and objective progress back to that requester. This appears to be an authorization bug, not evidence of deliberate malware; it needs in-client confirmation and a sender-membership check.

- **Gold, items, and deletion:** No mail, trade, auction, or guild-bank transfer calls were found. `Questie/Modules/EventHandler/QuestEventHandler.lua:245` uses `hooksecurefunc("DeleteCursorItem", ...)` to refresh quests after deletion; it does not delete items. Auto quest turn-in and breadcrumb abandonment are configurable and disabled by default (`Questie/Modules/Options/QuestieOptionsDefaults.lua:145–153`).

- **Chat and addon messages:** `Questie/Modules/QuestieAnnounce.lua:202` sends labeled, deduplicated quest announcements to the configured group channel. Party objective/item announcements are enabled by default. `Questie/Modules/QuestieSlash.lua:235` sends a completion-count emote through the player’s `/questie flex` command. AceComm/ChatThrottleLib hits implement transport, throttling, and traffic accounting; no separate Battle.net messaging campaign was found. Ordinary group sync is legitimate; the unchecked requester above is the concern.

- **Code from strings and encoded data:** `Questie/Database/SupportValidation.lua:90` and `Questie/Modules/Journey/tabs/QuestsByZone/QuestsByZoneTab.lua:141` execute bundled table strings. The inspected payloads contain numeric table literals, not hidden commands. Incoming messages use data deserialization. The other prescan hits are unused `loadstring` aliases, global-environment access, and a localization callback named `load`. Large TOC payloads are decoded as CBOR; all six flagged long lines are NPC coordinates.

- **Bindings, links, and packaged files:** `Questie/Modules/Journey/QuestieJourney.lua:222` assigns an unused semicolon binding to open Journey. No malicious macros or logout calls were found. Links are project/support, documentation, or Wowhead references. No separate executable payloads or reviewer-directed instructions were found. LibDeflate’s standalone file-processing branch is guarded and inactive inside WoW.

VERDICT: UNSURE (something needs a human to look)

## Maintainer sign-off

Passed by hammackj on 2026-11-09 (Claude: pass, Codex: unsure): Codex's concern is a privacy bug in party quest sharing (an outsider can request quest progress), not malicious code. Claude passed it.

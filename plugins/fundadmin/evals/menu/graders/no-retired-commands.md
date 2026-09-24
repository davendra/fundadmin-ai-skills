---
type: regex
name: no-retired-commands
target: last_message
pattern: "^(?![\\s\\S]*(?:vault-init|vault-sync|Inbox folder|KNOWLEDGE MANAGEMENT))[\\s\\S]+"
weight: 1
---

Deterministic precheck: the menu no longer lists the retired vault-init / vault-sync commands, the "KNOWLEDGE MANAGEMENT" heading or the old "download to an Inbox folder" monitor-email line.

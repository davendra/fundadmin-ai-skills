---
type: regex
name: skill-fired
target: last_message
pattern: "AI Fund Administration Assistant[\\s\\S]{0,80}60 Commands"
flags: i
weight: 1
---

Slash-command path: `/fundadmin:fund` injects the fund skill body via host
`<command-name>` (Skill tool_use count may be 0). Treat that injected-skill
answer shape as skill-fired — requiring `tool_used: Skill` is a false negative
for this host path; skill-body prose cannot force a redundant Skill call.

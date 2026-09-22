---
type: regex
name: spreadsheet
target: last_message
pattern: "KYC-TRACKER-[^\\s`]*\\.(?:xlsx|csv)"
flags: i
weight: 2
---

Deterministic precheck: the answer names a spreadsheet companion of the tracker report (.xlsx, or .csv when openpyxl is missing).

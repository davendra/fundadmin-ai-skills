# Host checks

These are observed synthetic integration checks for **v1.3.2**, performed on **13 October 2026**. They are not a full host/model qualification matrix or production certification. The test used the complete eight-page `OBRELUND-LPA-QUICKSTART.pdf`; no approved FundAdmin AI Workspace records were changed.

| Route | Install / setup | LPA review and PDF | Remaining limitation |
|---|---|---|---|
| Local Codex CLI, supplementary runtime check | Pinned marketplace install succeeded; all 169 plugin files matched the released payload; 61 skills and five agent definitions | Five sequential inline stages completed; saved source, Markdown, sidecar, workpapers and a 53-page PDF | Desktop interface not exercised; model identifier unavailable; not a full qualification matrix |
| ChatGPT desktop, local Codex task | Pinned shared local catalogue installed through the supported CLI; a separate desktop task used the installed skill | Five sequential inline stages completed; source, Markdown, validated sidecar, workpapers and a 57-page PDF saved | Exact model identifier and native named-agent execution unavailable; GUI installer clicks were not automated |
| ChatGPT cloud, personal plugin in Chat mode | Archive import/install succeeded and recognised 61 skills; verified bundle staging made helpers available to Python | Full source read and packaged scoring ran; final report and PDF were not completed | Account data-analysis limit interrupted validation and blocked a later Python continuation preflight; runtime had ReportLab 4.4.9 rather than pinned 5.0.1 |
| ChatGPT cloud Work | Package route documented | Not completed | The available account did not have Work enabled |

The local PDF was extracted across all 53 pages and rendered for inspection. Of 1,423 content checks, 1,419 matched directly; the remaining four cells were verified across page continuations. No missing findings were found, although long-table wrapping reduced readability. The report contains 66 findings and remains **PARTIAL**, with compliance and aggregate scores **UNAVAILABLE** because required regulatory facts and current authorities were not supplied.

The local test also attempted an unnecessary nested CLI launch which failed sandbox initialisation. That failure is retained separately; the actual outer ephemeral CLI process completed its installed workflow. It is not desktop UI evidence.

The separate desktop task completed on the installed v1.3.2 skill through its documented inline fallback. It read all eight pages and verified all 52 numbered section texts and page citations against the retained source. Its sidecar has 85 findings; all five stage workpapers and scoring inputs/outputs were retained. Python 3.9.6, ReportLab 5.0.1 and pypdf 6.19.0 were used. All 57 PDF pages were extracted and rendered; 1,566 of 1,570 elements matched directly, with four page-split cells reconstructed and visually checked. All 1,570 elements and 93 headings were preserved. The requesting chat separately checked the source and Markdown hashes, split-cell pages, first page and final limitations. Split rows, repeated headers, awkward word wrapping and a sparse final disclaimer page remain layout limitations; the PDF is untagged. Report status is **PARTIAL** with compliance and aggregate **UNAVAILABLE**, and 18 regulatory checks remain unavailable.

This is evidence for a **desktop local Codex task**, using the shared catalogue installation route below. It is not a test of every native installer screen, a cloud Work task, all 61 skills, an exact model matrix or production readiness. The user chose to continue testing the current cloud account's Chat mode; its code-tool quota remains a blocker, and no upgrade was requested.

## Issues found and setup fixes

- System Python lacked ReportLab. The local check used a new isolated environment with the release's pinned dependencies; the install guide now checks these before the first review.
- Cloud plugin instructions were readable while helper files were not mounted into Python. A separate, checksum-verified standalone release ZIP supplied the exact helper and agent files. This staging method is now documented; automatic mounting is not assumed.
- Evidence sidecars with uppercase finding IDs were rejected by the packaged validator. The local run corrected them and retained the failed attempt. Cloud correction was interrupted by the account limit. Never skip validation or call a rejected sidecar complete.
- A cloud plugin import does not unlock Work, change a subscription or provide connected-service permissions. Setup prompts now record the actual execution mode and missing capabilities.

## Finish a host check

Use the [full LPA and PDF quick start](/guide/quick-start#full-lpa-and-pdf-check) in a new isolated task on the host you intend to use. Record the installed version, tag, host/model/runtime, helper paths, dependency versions and whether specialist stages ran separately or inline.

Require actual downloadable or saved Markdown, sidecar, PDF and source/audit files. Validate the sidecar and source binding, extract and inspect the PDF including final limitations and table continuations. If code tools, dependencies or quota are unavailable, retain the attempt as **BLOCKED**; an in-chat draft does not fulfil the saved-report test.

A completed synthetic report is still draft analysis. Qualified human review is required before relying on it.

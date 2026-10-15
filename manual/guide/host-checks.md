# Host checks

These are observed synthetic integration checks for **v1.3.2**, performed on **13–15 October 2026**. They are not a full host/model qualification matrix or production certification. The test used the complete eight-page `OBRELUND-LPA-QUICKSTART.pdf`; no approved FundAdmin AI Workspace records were changed.

| Route | Install / setup | LPA review and PDF | Remaining limitation |
|---|---|---|---|
| Local Codex CLI, supplementary runtime check | Pinned marketplace install succeeded; all 169 plugin files matched the released payload; 61 skills and five agent definitions | Five sequential inline stages completed; saved source, Markdown, sidecar, workpapers and a 53-page PDF | Desktop interface not exercised; model identifier unavailable; not a full qualification matrix |
| ChatGPT desktop, local Codex task | Pinned shared local catalogue installed through the supported CLI; a separate desktop task used the installed skill | Five sequential inline stages completed; source, Markdown, validated sidecar, workpapers and a 57-page PDF saved | Exact model identifier and native named-agent execution unavailable; GUI installer clicks were not automated |
| ChatGPT cloud, personal plugin in Chat mode | Archive import/install recognised 61 skills; exact release-bundle staging and explicit packaged-helper API guidance | Saved Markdown, validated sidecar with 89 findings, five inline stages, 27-page PDF and downloaded audit ZIP; source/hash/text checks passed independently | Full LPA qualification remains open: incorrect operative citations/quotes and unsupported ratings need correction; final cloud-side fidelity refresh hit quota; ReportLab 4.4.9 used rather than pinned 5.0.1 |
| ChatGPT cloud Work | Package route documented | Not completed | The available account did not have Work enabled |

The local PDF was extracted across all 53 pages and rendered for inspection. Of 1,423 content checks, 1,419 matched directly; the remaining four cells were verified across page continuations. No missing findings were found, although long-table wrapping reduced readability. The report contains 66 findings and remains **PARTIAL**, with compliance and aggregate scores **UNAVAILABLE** because required regulatory facts and current authorities were not supplied.

The local test also attempted an unnecessary nested CLI launch which failed sandbox initialisation. That failure is retained separately; the actual outer ephemeral CLI process completed its installed workflow. It is not desktop UI evidence.

The separate desktop task completed on the installed v1.3.2 skill through its documented inline fallback. It read all eight pages and verified all 52 numbered section texts and page citations against the retained source. Its sidecar has 85 findings; all five stage workpapers and scoring inputs/outputs were retained. Python 3.9.6, ReportLab 5.0.1 and pypdf 6.19.0 were used. All 57 PDF pages were extracted and rendered; 1,566 of 1,570 elements matched directly, with four page-split cells reconstructed and visually checked. All 1,570 elements and 93 headings were preserved. The requesting chat separately checked the source and Markdown hashes, split-cell pages, first page and final limitations. Split rows, repeated headers, awkward word wrapping and a sparse final disclaimer page remain layout limitations; the PDF is untagged. Report status is **PARTIAL** with compliance and aggregate **UNAVAILABLE**, and 18 regulatory checks remain unavailable.

This is evidence for a **desktop local Codex task**, using the shared catalogue installation route below. It is not a test of every native installer screen, a cloud Work task, all 61 skills, an exact model matrix or production readiness. The user chose the current cloud account's Chat mode. Its export now works with the explicit staging/helper guidance below, but the substantive review has outstanding source-evidence corrections. No upgrade was requested.

## Issues found and setup fixes

- System Python lacked ReportLab. The local check used a new isolated environment with the release's pinned dependencies; the install guide now checks these before the first review.
- Cloud plugin instructions were readable while helper files were not mounted into Python. A separate, checksum-verified standalone release ZIP supplied the exact helper and agent files. This staging method is now documented; automatic mounting is not assumed.
- Evidence sidecars with uppercase finding IDs were rejected by the packaged validator. The local run corrected them and retained the failed attempt. Cloud continuation used the exact schema and the packaged public helper functions. Structural validation passed, but it did not catch incorrect operative-clause citations. Never skip validation or treat it as factual verification.
- A cloud plugin import does not unlock Work, change a subscription or provide connected-service permissions. Setup prompts now record the actual execution mode and missing capabilities.

## Cloud continuation 15 October 2026

The account's analysis tool became available, while its earlier working files had expired. Both original uploads still matched their hashes. A fresh run used all 169 byte-verified release files and the actual packaged `create_run`, `validate`, `write_report`, `score_lpa` and PDF renderer interfaces within the cloud Python process. This was an assisted continuation with explicit schema/API guidance, rather than an unassisted install-and-run claim. Python 3.13.5 and ReportLab 4.4.9 were observed; the release's 5.0.1 pin was not installed or qualified here.

The cloud saved five dependency-ordered inline stage workpapers, 52 inventoried numbered sections, a Markdown report, its validated 89-finding sidecar, a 27-page PDF and an audit ZIP. The downloaded archive's SHA-256 was `9e13254dd67b6de564b4f2fd05eb58d4148ac43e10dd4b2323fe5638b6242b54`; the PDF's was `4cd27fd328746ff5e4ed2a70fb66a8414f87abefb9123c0dd285e3eb2c5f989a`. All original source and Markdown bindings were checked independently, as were the 169 released files and deterministic scoring output.

Cloud quota returned during a stricter final text check. The requesting local chat checked the downloaded PDF rather than generating a replacement: 734 of 735 normalised Markdown lines/table cells matched directly; the remaining paragraph was complete across pages 16–17 after removing page footers. All 27 pages were rendered and inspected in a contact sheet, with individual checks of the table continuation, split paragraph and final limitations. No missing report content was found. Narrow table wrapping, repeated headers, labelled-record fallbacks for wide tables and the untagged PDF remain presentation/accessibility limitations. The original cloud archive was preserved; a separate local audit package adds independent checks and failure history. A refreshed final archive was not generated in cloud after quota returned.

**The full LPA check has not passed.** Content review found that the fee, expense, carry and commitment-period assessments quoted the opening Affiliate definition in section 1.1 instead of their operative provisions. The key-issues reporting row also cited section 1.1 instead of sections 16.1–16.3. Correct the quotations and locators, complete the economic/period assessment, reassess affected ratings, propagate changes through the dependent stages and regenerate a new cloud report. Do not rely on those dimension inputs until this is done. Genuine matching source bytes, a valid sidecar and complete PDF text do not establish that a quotation supports the finding beside it.

The report remains a **PARTIAL synthetic draft**, with compliance and aggregate **UNAVAILABLE**. Source-section inventory coverage describes extraction only. It is not full substantive review, current regulatory verification or production certification. The next scheduled continuation will address these content findings when code-tool capacity returns; it must preserve the downloaded originals and approved Workspace records.

## Finish a host check

Use the [full LPA and PDF quick start](/guide/quick-start#full-lpa-and-pdf-check) in a new isolated task on the host you intend to use. Record the installed version, tag, host/model/runtime, helper paths, dependency versions and whether specialist stages ran separately or inline.

Require actual downloadable or saved Markdown, sidecar, PDF and source/audit files. Validate the sidecar and source binding, extract and inspect the PDF including final limitations and table continuations. If code tools, dependencies or quota are unavailable, retain the attempt as **BLOCKED**; an in-chat draft does not fulfil the saved-report test.

A completed synthetic report is still draft analysis. Qualified human review is required before relying on it.

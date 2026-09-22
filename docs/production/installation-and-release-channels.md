# Installation and release channels

How a release reaches a user, which sources are installation targets and which are not, and what a supervised pilot pins and records. Read it with the [operator guide](README.md) and the [verification record](verification.md).

## What `main` is

`main` in the public marketplace repository `davendra/fundadmin-ai-skills` is the public marketplace source, and it carries a release only after that release's checks pass: production-policy sync, the generated-tree check, strict plugin and marketplace validation, the runtime and contract suites, and candidate-bound host evidence accepted by `tools/verify_release_evidence.py`. Content that has not passed those checks does not reach it.

`main` in the source repository `davendra/fundadmin-ai` is a development branch. It is a build input, never an installation target.

In either repository `main` is a moving reference: it names a source, not a reviewed set of bytes, and what it points at can differ between one installation and the next.

## Release tags

Every public release is tagged `fundadmin--vX.Y.Z` in the marketplace repository. The tag is pushed with the release commit, is never moved and is never replaced; a correction takes a new version number. A tag therefore names one immutable set of bytes — the skills, agents, references, manual and metadata reviewed under that version.

Hosts cache by version, so republishing at an unchanged version number is invisible to installed users. The version number is the only upgrade signal.

## What a supervised pilot pins

A supervised pilot pins a reviewed release tag, or a specific commit, and records which one. It does not follow a branch. Pin before the pilot starts, and review a newer release before moving the group to it: a release can change skill instructions, thresholds, filename families, output contracts and bundled references.

Development branches, forks, pull-request references and local checkouts are not user installation targets. A reviewed local checkout of the source repository is a maintainer route for building and testing the plugin, not a way to distribute it to pilot users.

No installation for a controlled financial workflow may be global and unpinned. A global installation that tracks the newest available content changes what the pilot runs with no review step and no record of when it changed.

## Marketplace sync and updates

A marketplace sync can bring later plugin content into a host or a workspace. A newer release can add, remove or reword skills, change what a skill writes, and change the references it cites. An administrator should review the contents of an updated release and its changelog entry before enabling it for a pilot group, and should treat enabling it as a change to the reviewed configuration, recorded as such.

## One installation method per environment

Use exactly one installation method in any one host environment. The plugin route, a plain-skills installation from a source checkout, and raw skill files copied by a third-party installer all provide skills of the same names. Two copies in one host leave it ambiguous which instructions ran, and evidence collected against one copy does not describe the other. Remove the previous installation before switching methods.

Third-party skill installers copy selected raw skill files only. They do not install the plugin manifest, the agents, the marketplace metadata, the version metadata or the release assets, and skills copied that way run without the packaged report helper, so their output is an unverified draft rather than a saved report with source hashes and an evidence sidecar. That route is developer compatibility, not a supervised-pilot configuration.

## What to record in pilot evidence

Record the following for each pilot environment, and again at every change to it:

| Field | What to write down |
|---|---|
| Installation method | Native marketplace plugin, workspace marketplace import, or reviewed source checkout |
| Plugin version and release tag or commit | For example 1.1.0 and `fundadmin--v1.1.0` |
| Host and host version | For example Claude Code 2.1.278 |
| Model or runtime identifier | The resolved identifier from the trace, not an alias |

Record the date of each change and who authorised it. Evidence gathered on one combination of these four does not carry over to another: after an upgrade or a host change the combination is new, and so is the evidence needed for it. Keep this record with the pilot's review evidence, in approved storage outside plugin build inputs.

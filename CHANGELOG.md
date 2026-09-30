# Changelog

Releases of the `gradle-skills` plugin, newest first.
Each release lists the version of every skill it contains; a skill whose version did not change ships unchanged from the previous release.
See [Versions](CONTRIBUTING.md#versions) for how plugin and skill versions relate.

<!--
Template for a release:

## X.Y.Z — YYYY-MM-DD

| Skill | Version | |
|---|---|---|
| gradle-best-practices | A.B.C | changed / unchanged / added |
| gradle-wrapper-upgrade | D.E.F | changed / unchanged / added |

### gradle-best-practices A.B.C

- What changed for someone using the skill, not what changed in the files.
- Evaluation: [gradle-best-practices-A.B.C](evals/gradle-best-practices/gradle-best-practices-A.B.C.md)
-->

## 1.0.0 — Unreleased

First release.

| Skill | Version | |
|---|---|---|
| gradle-best-practices | 1.0.0 | added |
| gradle-wrapper-upgrade | 1.0.0 | added |

### gradle-best-practices 1.0.0

- Audits a Gradle build against the official best practices and proposes fixes, from a catalog of 48 practices captured from the Gradle 9.9.0 nightly documentation and shipped with the skill.
- Evaluation: [gradle-best-practices-1.0.0](evals/gradle-best-practices/gradle-best-practices-1.0.0.md)

### gradle-wrapper-upgrade 1.0.0

- Upgrades an existing Gradle wrapper on Gradle 7.0–9.x, verifies the result, and rolls back when the build no longer configures on the new version.
- Evaluation: [gradle-wrapper-upgrade-1.0.0](evals/gradle-wrapper-upgrade/gradle-wrapper-upgrade-1.0.0.md)

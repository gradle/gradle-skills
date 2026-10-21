# Security

## Validate the Gradle Distribution SHA-256 Checksum · `validate_gradle_checksum` · High
When: `gradle/wrapper/gradle-wrapper.properties` exists.
Detect (det): no `distributionSha256Sum` key in that file.
Fix: Add the published `distributionSha256Sum` for the exact distribution in `distributionUrl`.

## Validate the Gradle Wrapper on every Upgrade · `validate_wrapper_checksum` · Medium
When: `gradle/wrapper/gradle-wrapper.jar` is committed to the project. This is about that **jar**, not the distribution it downloads — a tampered wrapper jar executes attacker code on every `./gradlew` invocation, and it is a binary no reviewer reads. The distribution's own checksum is the separate `validate_gradle_checksum` entry above; do not conflate the two, and report both when both apply.
Detect (det): the jar is present at `gradle/wrapper/gradle-wrapper.jar`. That presence is the whole of what is checkable here. **Whether it is genuine cannot be established from the files this skill reads** — that means comparing its SHA-256 against Gradle's published list, a network lookup this skill does not make. So report this wherever the jar is committed, phrased as standing advice rather than a detected defect, and never as a clean bill of health for the binary.
Fix: Regenerate the wrapper with a trusted Gradle install and diff the result against what is committed — a genuine jar is byte-identical to the one that install ships.

## Do not Run `./gradlew` on Untrusted Projects · `run_gradle_on_external_projects` · Recommendation
When: operator guidance, not a property of the project under audit. Do not report it as a finding against the project. Mention it only if the audit surfaced something suspicious — an `exec` / `ProcessBuilder` call in a build script, an obfuscated string, or a `distributionUrl` on a non-Gradle host — in which case report *that*, with this anchor as the reference.
Detect (heur): `exec(`, `ProcessBuilder`, `Runtime.getRuntime().exec`, base64-looking literals, or downloads from unexpected hosts in build scripts.
Fix: Report the specific construct and what it does. Do not remove it silently.

## Build Output Should Be Byte-for-Byte Reproducible · `builds_should_be_reproducible` · Medium
When: the build produces an archive (`jar`, `war`, `zip`, or any `AbstractArchiveTask`).
Detect (det): `isPreserveFileTimestamps = true` / `preserveFileTimestamps = true`; `isReproducibleFileOrder = false` / `reproducibleFileOrder = false`; or no `java { toolchain { languageVersion = ... } }` block, which leaves the build dependent on the local `JAVA_HOME`.
Fix: Remove overrides of the Gradle 9 defaults and pin the JDK with a toolchain.

## Build your Published Artifacts Securely · `build-published-artifacts-securely` · Medium
When: the build publishes artifacts (`maven-publish`, a `publishing { }` block, or `signing`). `builds_should_be_reproducible` is its prerequisite — raise the two together.
Detect (det): the build publishes. That is the whole of what is checkable here. **This practice is advisory and is not evaluated against the project.** It is about where and how the publishing pipeline runs, and this skill reads only Gradle files, so it never sees that configuration. Report it once, as standing advice, whenever the build publishes — never as a detected violation, and never as a pass. Do not go looking for pipeline configuration to judge, and do not name a CI product; the advice is about the properties the publishing environment must have, whatever runs it.
Fix: Publish from a fresh, isolated, ephemeral machine with the build cache and any prior outputs disabled.

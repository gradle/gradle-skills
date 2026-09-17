# Security

## Validate the Gradle Distribution SHA-256 Checksum · `validate_gradle_checksum` · High
When: `gradle/wrapper/gradle-wrapper.properties` exists.
Detect (det): no `distributionSha256Sum` key in that file.

## Validate the Gradle Wrapper on every Upgrade · `validate_wrapper_checksum` · Medium
When: a wrapper exists. This is a process practice — it describes what the project's workflow should do, so report it as a recommendation about CI or review rather than a code defect, unless one of the signals below is present.
Detect (det): `distributionUrl` pointing somewhere other than `https://services.gradle.org/`; or no wrapper-validation step in CI configuration, where that configuration is visible in the project.

## Do not Run `./gradlew` on Untrusted Projects · `run_gradle_on_external_projects` · Recommendation
When: operator guidance, not a property of the project under audit. Do not report it as a finding against the project. Mention it only if the audit surfaced something suspicious — an `exec` / `ProcessBuilder` call in a build script, an obfuscated string, or a `distributionUrl` on a non-Gradle host — in which case report *that*, with this anchor as the reference.
Detect (heur): `exec(`, `ProcessBuilder`, `Runtime.getRuntime().exec`, base64-looking literals, or downloads from unexpected hosts in build scripts.

## Build Output Should Be Byte-for-Byte Reproducible · `builds_should_be_reproducible` · Medium
When: the build produces an archive (`jar`, `war`, `zip`, or any `AbstractArchiveTask`).
Detect (det): `isPreserveFileTimestamps = true` / `preserveFileTimestamps = true`; `isReproducibleFileOrder = false` / `reproducibleFileOrder = false`; or no `java { toolchain { languageVersion = ... } }` block, which leaves the build dependent on the local `JAVA_HOME`.

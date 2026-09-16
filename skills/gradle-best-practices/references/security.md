# Security

Base URL for every anchor below: `https://docs.gradle.org/current/userguide/best_practices_security.html`

---

## Validate the Gradle Distribution SHA-256 Checksum
`validate_gradle_checksum` · 9.1.0 · **High**

- **Rule:** Set `distributionSha256Sum` in `gradle-wrapper.properties` so the downloaded distribution's integrity is verified.
- **Applies when:** `gradle/wrapper/gradle-wrapper.properties` exists.
- **Detect** (deterministic): no `distributionSha256Sum` key in `gradle/wrapper/gradle-wrapper.properties`.
- **Fix:** see `references/fixes/validate_gradle_checksum.md` — read it only when you are about to apply this entry.

---

## Validate the Gradle Wrapper on every Upgrade
`validate_wrapper_checksum` · 9.3.0 · **Medium**

- **Rule:** Treat wrapper changes as security-sensitive: verify the wrapper JAR and distribution settings whenever Gradle is upgraded.
- **Applies when:** A wrapper exists. This is a process practice — it describes what the project's workflow should do, so report it as a recommendation about CI/review rather than a code defect, unless one of the detectable signals below is present.
- **Detect** (deterministic): `distributionUrl` pointing somewhere other than `https://services.gradle.org/`; absence of any wrapper-validation step in CI configuration, where CI configuration is visible in the project.
- **Fix:** see `references/fixes/validate_wrapper_checksum.md` — read it only when you are about to apply this entry.

---

## Do not Run `./gradlew` on Untrusted Projects
`run_gradle_on_external_projects` · 9.7.0 · **Recommendation**

- **Rule:** Running `./gradlew` executes arbitrary build logic; inspect an unfamiliar project before running or opening it in an IDE.
- **Applies when:** This is operator guidance, not a property of the project under audit. Do not report it as a finding against the project. Mention it only if the audit itself surfaced something suspicious — an `exec`/`ProcessBuilder` call in a build script, an obfuscated string, or a `distributionUrl` on a non-Gradle host — in which case report *that*, with this anchor as the reference.
- **Detect** (heuristic): `exec(`, `ProcessBuilder`, `Runtime.getRuntime().exec`, base64-looking literals, or downloads from unexpected hosts in build scripts.
- **Fix:** see `references/fixes/run_gradle_on_external_projects.md` — read it only when you are about to apply this entry.

---

## Build Output Should Be Byte-for-Byte Reproducible
`builds_should_be_reproducible` · 9.7.0 · **Medium**

- **Rule:** Identical sources should produce byte-identical outputs on any machine at any time.
- **Applies when:** The build produces an archive (`jar`, `war`, `zip`, or any `AbstractArchiveTask`).
- **Detect** (deterministic): `isPreserveFileTimestamps = true` / `preserveFileTimestamps = true`; `isReproducibleFileOrder = false` / `reproducibleFileOrder = false`; or no `java { toolchain { languageVersion = ... } }` block, which leaves the build dependent on the local `JAVA_HOME`.
- **Fix:** see `references/fixes/builds_should_be_reproducible.md` — read it only when you are about to apply this entry.

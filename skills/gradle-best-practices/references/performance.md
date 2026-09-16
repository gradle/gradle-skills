# Performance

Base URL for every anchor below: `https://docs.gradle.org/current/userguide/best_practices_performance.html`

---

## Enable UTF-8
`use_utf8_encoding` · 9.0.0 · **Medium**

- **Rule:** Set UTF-8 as the default file encoding so behaviour is consistent across platforms and does not defeat caching through a platform-dependent default.
- **Applies when:** Always.
- **Detect** (deterministic): `org.gradle.jvmargs` in the root `gradle.properties` does not contain `-Dfile.encoding=UTF-8` (including the case where `org.gradle.jvmargs` is absent entirely).
- **Fix:** see `references/fixes/use_utf8_encoding.md` — read it only when you are about to apply this entry.

---

## Use the Build Cache
`use_build_cache` · 9.1.0 · **Medium**

- **Rule:** Enable the build cache so task outputs are reused instead of recomputed when inputs have not changed.
- **Applies when:** Always.
- **Detect** (deterministic): root `gradle.properties` lacks `org.gradle.caching=true`, or sets `org.gradle.caching=false`.
- **Fix:** see `references/fixes/use_build_cache.md` — read it only when you are about to apply this entry.

---

## Use the Configuration Cache
`use_configuration_cache` · 9.1.0 · **High**

- **Rule:** Enable the configuration cache so the configuration phase is skipped and the task graph is loaded from disk.
- **Applies when:** Always.
- **Detect** (deterministic): root `gradle.properties` lacks `org.gradle.configuration-cache=true`, or sets it to `false`.
- **Fix:** see `references/fixes/use_configuration_cache.md` — read it only when you are about to apply this entry.

---

## Avoid Expensive Computations in Configuration Phase
`avoid_computations_in_configuration_phase` · 9.0.0 · **High**

- **Rule:** Move file I/O, network calls and CPU-heavy work out of the configuration phase and into task actions, so it runs only when needed.
- **Applies when:** Always.
- **Detect** (heuristic): work performed at the top level of a build script or inside a `tasks.register` / `tasks.create` configuration block rather than in a `@TaskAction` / `doLast`. Concrete markers: `File(...).readText()`, `readLines()`, `Files.` calls, `URL(...)`, `exec`/`providers.exec` results consumed eagerly, `Thread.sleep`, or a loop over files outside a task action.
- **Fix:** see `references/fixes/avoid_computations_in_configuration_phase.md` — read it only when you are about to apply this entry.

---

## Prefer the `-bin` Gradle Distribution
`prefer_bin_distribution` · 9.4.0 · **Recommendation**

- **Rule:** Prefer the smaller `-bin` distribution over `-all`, which additionally carries sources and documentation.
- **Applies when:** A wrapper exists.
- **Detect** (deterministic): `distributionUrl` in `gradle/wrapper/gradle-wrapper.properties` ends with `-all.zip`.
- **Fix:** see `references/fixes/prefer_bin_distribution.md` — read it only when you are about to apply this entry.

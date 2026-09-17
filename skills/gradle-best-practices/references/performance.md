# Performance

## Enable UTF-8 · `use_utf8_encoding` · Medium
When: always.
Detect (det): `org.gradle.jvmargs` in the root `gradle.properties` does not contain `-Dfile.encoding=UTF-8`, including the case where `org.gradle.jvmargs` is absent entirely.

## Use the Build Cache · `use_build_cache` · Medium
When: always.
Detect (det): root `gradle.properties` lacks `org.gradle.caching=true`, or sets it to `false`.

## Use the Configuration Cache · `use_configuration_cache` · High
When: always.
Detect (det): root `gradle.properties` lacks `org.gradle.configuration-cache=true`, or sets it to `false`.

## Avoid Expensive Computations in Configuration Phase · `avoid_computations_in_configuration_phase` · High
When: always.
Detect (heur): work at the top level of a build script, or inside a `tasks.register` / `tasks.create` configuration block, rather than in a `@TaskAction` / `doLast`. Markers: `File(...).readText()`, `readLines()`, `Files.` calls, `URL(...)`, `exec` / `providers.exec` results consumed eagerly, `Thread.sleep`, or a loop over files outside a task action.

## Prefer the `-bin` Gradle Distribution · `prefer_bin_distribution` · Recommendation
When: a wrapper exists.
Detect (det): `distributionUrl` in `gradle/wrapper/gradle-wrapper.properties` ends with `-all.zip`.

# General

## Use Kotlin DSL · `use_kotlin_dsl` · Recommendation
When: always.
Detect (det): any file named `build.gradle` or `settings.gradle` (no `.kts`).
Fix: Convert the script to `.gradle.kts`, one script at a time. Structural — plan first.

## Use the Latest Minor Version of Gradle · `use_latest_minor_versions` · Medium
When: a wrapper exists.
Detect (heur): the version in `distributionUrl` (`gradle/wrapper/gradle-wrapper.properties`). Flag only if clearly old — a superseded major, or several minors behind. Do not guess at "latest"; state the version found and that it needs checking, rather than asserting a newer number.
Fix: Run `./gradlew wrapper --gradle-version <v>`, then update plugins. Gradle before plugins.

## Apply Plugins Using the `plugins` Block · `use_the_plugins_block` · Medium
When: always.
Detect (det): `apply plugin:`, `apply(plugin =`, or a `buildscript {` block containing `classpath(` / `classpath `, in any build or settings script.
Fix: Replace with `plugins { id("…") }` and delete the `buildscript { }` classpath entry.

## Don't Assume your Plugin is Applied after Another · `dont_assume_plugin_order` · Medium
When: build logic in `buildSrc/` or `build-logic/`, or a script configuring another plugin's extensions.
Detect (heur): `extensions.getByType(` / `extensions.getByName(`, or configuration of another plugin's extension at the top level of a plugin's `apply`, with no `pluginManager.withPlugin` guard. `subprojects {}` / `allprojects {}` blocks configuring plugin extensions are the common case.
Fix: Wrap in `pluginManager.withPlugin("id") { … }`, or apply the prerequisite explicitly.

## Do Not Use Internal APIs · `do_not_use_internal_apis` · High
When: Java/Kotlin/Groovy source under `buildSrc/` or `build-logic/`, or scripts importing Gradle types.
Detect (det): `org.gradle.` … `.internal.` in an import or fully-qualified reference; a cast or reference to a type ending `Internal` (e.g. `AttributeContainerInternal`) or `Impl`.
Fix: Use the public API equivalent; if none exists, copy the logic into the project.

## Set Build Flags in `gradle.properties` · `use_the_gradle_properties_file` · Medium
When: always.
Detect (heur): `org.gradle.*` flags absent from the root `gradle.properties` while appearing in CI configuration, scripts or documentation as `-D` / `-P` arguments. Also flag a missing root `gradle.properties` in a build that plainly needs flags (see `performance.md`).
Fix: Move the flags into the root `gradle.properties`, one `key=value` per line.

## Name Your Root Project · `name_your_root_project` · Medium
When: a settings file exists — or should; a build with none is its own finding.
Detect (det): no `rootProject.name` assignment in `settings.gradle.kts` / `settings.gradle`.
Fix: Add `rootProject.name = "…"` to the settings file, after any `pluginManagement { }`.

## Do not use `gradle.properties` in subprojects · `do_not_use_gradle_properties_in_subprojects` · Medium
When: more than one project.
Detect (det): a `gradle.properties` file at any path other than the root project, or an included build's own root.
Fix: Move the values to the root `gradle.properties`; use a convention plugin for per-project config.

## Avoid `afterEvaluate` · `avoid_after_evaluate` · High
When: always.
Detect (det): `afterEvaluate` anywhere in a build script, settings script, or build logic source.
Fix: Use lazy `Property`/`Provider` wiring, and `pluginManager.withPlugin` to react to plugins.

## Consider use of `@Incubating` APIs carefully · `consider_use_of_incubating_apis_carefully` · Recommendation
When: build logic source or scripts using recent Gradle APIs.
Detect (heur): APIs annotated `@Incubating`, or an `@OptIn`-style suppression of an incubating warning. Flag only where the usage is load-bearing, and note it as a maintenance risk rather than a defect.
Fix: Record which incubating APIs are used and why; re-check them on every Gradle upgrade.

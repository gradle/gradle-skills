# General

## Use Kotlin DSL · `use_kotlin_dsl` · Recommendation
When: always.
Detect (det): any file named `build.gradle` or `settings.gradle` (no `.kts`).

## Use the Latest Minor Version of Gradle · `use_latest_minor_versions` · Medium
When: a wrapper exists.
Detect (heur): the version in `distributionUrl` (`gradle/wrapper/gradle-wrapper.properties`). Flag only if clearly old — a superseded major, or several minors behind. Do not guess at "latest"; state the version found and that it needs checking, rather than asserting a newer number.

## Apply Plugins Using the `plugins` Block · `use_the_plugins_block` · Medium
When: always.
Detect (det): `apply plugin:`, `apply(plugin =`, or a `buildscript {` block containing `classpath(` / `classpath `, in any build or settings script.

## Don't Assume your Plugin is Applied after Another · `dont_assume_plugin_order` · Medium
When: build logic in `buildSrc/` or `build-logic/`, or a script configuring another plugin's extensions.
Detect (heur): `extensions.getByType(` / `extensions.getByName(`, or configuration of another plugin's extension at the top level of a plugin's `apply`, with no `pluginManager.withPlugin` guard. `subprojects {}` / `allprojects {}` blocks configuring plugin extensions are the common case.

## Do Not Use Internal APIs · `do_not_use_internal_apis` · High
When: Java/Kotlin/Groovy source under `buildSrc/` or `build-logic/`, or scripts importing Gradle types.
Detect (det): `org.gradle.` … `.internal.` in an import or fully-qualified reference; a cast or reference to a type ending `Internal` (e.g. `AttributeContainerInternal`) or `Impl`.

## Set Build Flags in `gradle.properties` · `use_the_gradle_properties_file` · Medium
When: always.
Detect (heur): `org.gradle.*` flags absent from the root `gradle.properties` while appearing in CI configuration, scripts or documentation as `-D` / `-P` arguments. Also flag a missing root `gradle.properties` in a build that plainly needs flags (see `performance.md`).

## Name Your Root Project · `name_your_root_project` · Medium
When: a settings file exists — or should; a build with none is its own finding.
Detect (det): no `rootProject.name` assignment in `settings.gradle.kts` / `settings.gradle`.

## Do not use `gradle.properties` in subprojects · `do_not_use_gradle_properties_in_subprojects` · Medium
When: more than one project.
Detect (det): a `gradle.properties` file at any path other than the root project, or an included build's own root.

## Avoid `afterEvaluate` · `avoid_after_evaluate` · High
When: always.
Detect (det): `afterEvaluate` anywhere in a build script, settings script, or build logic source.

## Consider use of `@Incubating` APIs carefully · `consider_use_of_incubating_apis_carefully` · Recommendation
When: build logic source or scripts using recent Gradle APIs.
Detect (heur): APIs annotated `@Incubating`, or an `@OptIn`-style suppression of an incubating warning. Flag only where the usage is load-bearing, and note it as a maintenance risk rather than a defect.

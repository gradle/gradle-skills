# General

Base URL for every anchor below: `https://docs.gradle.org/current/userguide/best_practices_general.html`

---

## Use Kotlin DSL
`use_kotlin_dsl` · 8.14 · **Recommendation**

- **Rule:** Prefer the Kotlin DSL (`build.gradle.kts`, `settings.gradle.kts`) over the Groovy DSL (`build.gradle`, `settings.gradle`) for type safety and IDE support.
- **Applies when:** Always.
- **Detect** (deterministic): any file named `build.gradle` or `settings.gradle` (no `.kts`) exists.
- **Fix:** see `references/fixes/use_kotlin_dsl.md` — read it only when you are about to apply this entry.

---

## Use the Latest Minor Version of Gradle
`use_latest_minor_versions` · 8.14 · **Medium**

- **Rule:** Stay on the latest minor version of the major Gradle release in use, and keep plugins on their latest compatible versions.
- **Applies when:** A wrapper exists.
- **Detect** (heuristic): read `distributionUrl` in `gradle/wrapper/gradle-wrapper.properties` and note the version. Flag only if the version is clearly old (a superseded major, or a minor several releases behind). Do not guess at "latest" — state the version found and that it should be checked against the current release, rather than asserting a specific newer number.
- **Fix:** see `references/fixes/use_latest_minor_versions.md` — read it only when you are about to apply this entry.

---

## Apply Plugins Using the `plugins` Block
`use_the_plugins_block` · 8.14 · **Medium**

- **Rule:** Always apply plugins with the `plugins {}` block.
- **Applies when:** Always.
- **Detect** (deterministic): any of `apply plugin:`, `apply(plugin =`, or a `buildscript {` block containing `classpath(` / `classpath ` in any build or settings script.
- **Fix:** see `references/fixes/use_the_plugins_block.md` — read it only when you are about to apply this entry.

---

## Don't Assume your Plugin is Applied after Another
`dont_assume_plugin_order` · — · **Medium**

- **Rule:** Do not write build logic that depends on a particular plugin application order.
- **Applies when:** The build contains build logic in `buildSrc/`, `build-logic/`, or a script that configures another plugin's extensions.
- **Detect** (heuristic): `extensions.getByType(`, `extensions.getByName(`, or configuration of another plugin's extension at the top level of a plugin's `apply`, with no `pluginManager.withPlugin` guard. `subprojects {}` or `allprojects {}` blocks that configure plugin extensions are the common case.
- **Fix:** see `references/fixes/dont_assume_plugin_order.md` — read it only when you are about to apply this entry.

---

## Do Not Use Internal APIs
`do_not_use_internal_apis` · 8.14 · **High**

- **Rule:** Do not use APIs from a package where any segment is `internal`, or types whose names end in `Internal` or `Impl`.
- **Applies when:** The build has Java/Kotlin/Groovy source under `buildSrc/` or `build-logic/`, or scripts that import Gradle types.
- **Detect** (deterministic): `org.gradle.` … `.internal.` in an import or fully-qualified reference; a cast or reference to a type ending `Internal` (e.g. `AttributeContainerInternal`) or `Impl`.
- **Fix:** see `references/fixes/do_not_use_internal_apis.md` — read it only when you are about to apply this entry.

---

## Set Build Flags in `gradle.properties`
`use_the_gradle_properties_file` · 9.0.0 · **Medium**

- **Rule:** Set Gradle build flags in the root `gradle.properties`, checked into source control, rather than passing them per-invocation.
- **Applies when:** Always.
- **Detect** (heuristic): `org.gradle.*` flags absent from the root `gradle.properties` while appearing in CI configuration, scripts, or documentation as `-D` / `-P` command-line arguments. Also flag a missing root `gradle.properties` in a build that plainly needs flags (see `performance.md`).
- **Fix:** see `references/fixes/use_the_gradle_properties_file.md` — read it only when you are about to apply this entry.

---

## Name Your Root Project
`name_your_root_project` · 9.2.0 · **Medium**

- **Rule:** Always set the root project's name in the settings file, so it does not depend on the checkout directory name.
- **Applies when:** A settings file exists (or should — a build with no settings file at all is its own finding).
- **Detect** (deterministic): no `rootProject.name` assignment in `settings.gradle.kts` / `settings.gradle`.
- **Fix:** see `references/fixes/name_your_root_project.md` — read it only when you are about to apply this entry.

---

## Do not use `gradle.properties` in subprojects
`do_not_use_gradle_properties_in_subprojects` · 9.2.0 · **Medium**

- **Rule:** Do not place a `gradle.properties` file inside a subproject to configure the build; properties there are handled inconsistently.
- **Applies when:** The build has more than one project.
- **Detect** (deterministic): a `gradle.properties` file at any path other than the root project (and other than an included build's own root).
- **Fix:** see `references/fixes/do_not_use_gradle_properties_in_subprojects.md` — read it only when you are about to apply this entry.

---

## Avoid `afterEvaluate`
`avoid_after_evaluate` · 9.6.0 · **High**

- **Rule:** Do not use `project.afterEvaluate {}` to configure tasks, wire properties, or react to plugin application.
- **Applies when:** Always.
- **Detect** (deterministic): `afterEvaluate` anywhere in a build script, settings script, or build logic source.
- **Fix:** see `references/fixes/avoid_after_evaluate.md` — read it only when you are about to apply this entry.

---

## Consider use of `@Incubating` APIs carefully
`consider_use_of_incubating_apis_carefully` · 9.7.0 · **Recommendation**

- **Rule:** Adopt incubating APIs deliberately, aware that they can change between releases.
- **Applies when:** The build has build logic source or scripts using recent Gradle APIs.
- **Detect** (heuristic): use of APIs annotated `@Incubating`, or an `@OptIn`-style suppression of an incubating warning. Flag only where the usage is load-bearing, and note it as a maintenance risk rather than a defect.
- **Fix:** see `references/fixes/consider_use_of_incubating_apis_carefully.md` — read it only when you are about to apply this entry.

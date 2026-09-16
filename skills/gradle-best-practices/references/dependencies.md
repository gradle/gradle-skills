# Dependencies

Base URL for every anchor below: `https://docs.gradle.org/current/userguide/best_practices_dependencies.html`

---

## Declare Dependencies using a single GAV String
`single-gav-string` · 8.14 · **Medium**

- **Rule:** Use the `"group:artifact:version"` string form. The named-argument form is deprecated.
- **Applies when:** Any `dependencies {}` block exists.
- **Detect** (deterministic): a dependency declaration using named arguments — `group:` / `name:` / `version:` (Groovy) or `group =` / `name =` / `version =` (Kotlin) inside a dependency call.
- **Fix:** see `references/fixes/single-gav-string.md` — read it only when you are about to apply this entry.

---

## Use Version Catalogs to Centralize Dependency Versions
`use_version_catalogs` · 9.0.0 · **Medium**

- **Rule:** Centralize versions in `gradle/libs.versions.toml` rather than declaring them in build scripts or extension properties.
- **Applies when:** Any `dependencies {}` block exists.
- **Detect** (deterministic): no `gradle/libs.versions.toml`, while hard-coded versions appear in dependency strings; or versions held in `ext`/`extra`/local variables (`val fooVersion =`, `def fooVersion =`, `project.ext[`).
- **Fix:** see `references/fixes/use_version_catalogs.md` — read it only when you are about to apply this entry.

---

## Name Version Catalog Entries Appropriately
`name_version_catalog_entries` · 9.0.0 · **Recommendation**

- **Rule:** Name catalog entries from the module coordinates: 1–3 dash-separated segments, dropping the TLD segment, converting artifact dashes to camelCase, and avoiding redundancy.
- **Applies when:** `gradle/libs.versions.toml` exists.
- **Detect** (deterministic): entry keys that use `_` as a separator, repeat a segment (`ktor-ktor-client-core`), begin with a TLD (`com-`, `org-`), or are bare generic words (`java`, `core`, `module`).
- **Fix:** see `references/fixes/name_version_catalog_entries.md` — read it only when you are about to apply this entry.

---

## Set up your Dependency Repositories in the Settings file
`set_up_repositories_in_settings` · 9.0.0 · **Medium**

- **Rule:** Declare repositories in `settings.gradle(.kts)` under `pluginManagement` and `dependencyResolutionManagement`, not in individual build scripts.
- **Applies when:** Any `repositories {}` block exists anywhere.
- **Detect** (deterministic): a `repositories {` block in a `build.gradle`/`build.gradle.kts`, or inside a `buildscript {}` block.
- **Fix:** see `references/fixes/set_up_repositories_in_settings.md` — read it only when you are about to apply this entry.

---

## Don't Explicitly Depend on the Kotlin Standard Library
`dont_depend_on_kotlin_stdlib` · 9.0.0 · **Recommendation**

- **Rule:** Omit an explicit stdlib dependency — the Kotlin Gradle Plugin adds the matching version itself.
- **Applies when:** A Kotlin plugin is applied (`kotlin("jvm")`, `org.jetbrains.kotlin.jvm`, …). Otherwise not applicable.
- **Detect** (deterministic): `kotlin("stdlib")` or `org.jetbrains.kotlin:kotlin-stdlib` in a `dependencies {}` block.
- **Fix:** see `references/fixes/dont_depend_on_kotlin_stdlib.md` — read it only when you are about to apply this entry.

---

## Avoid Redundant Dependency Declarations
`avoid_duplicate_dependencies` · 9.0.0 · **Medium**

- **Rule:** Do not declare the same module more than once, or in two configurations where one already implies the other.
- **Applies when:** Any `dependencies {}` block exists.
- **Detect** (deterministic): the same `group:artifact` appearing twice in one project's dependency blocks — including once in `api` and once in `implementation`, or in both `implementation` and `compileOnly`/`runtimeOnly` where that is redundant.
- **Fix:** see `references/fixes/avoid_duplicate_dependencies.md` — read it only when you are about to apply this entry.

---

## Use Content Filtering with multiple Repositories
`use_content_filtering` · 9.1.0 · **Medium**

- **Rule:** When several repositories are declared, filter which coordinates come from each, so resolution is predictable and a dependency cannot be served by an unintended repository.
- **Applies when:** More than one repository is declared in the same `repositories {}` block.
- **Detect** (deterministic): two or more repository declarations with no `content {` or `exclusiveContent {` block among them.
- **Fix:** see `references/fixes/use_content_filtering.md` — read it only when you are about to apply this entry.

---

## Apply Exclusions Narrowly
`apply_exclusions_narrowly` · 9.2.0 · **Medium**

- **Rule:** Attach an exclusion to the specific dependency that drags in the unwanted module, and name the module — not the whole group, and not the whole configuration.
- **Applies when:** Any `exclude` appears in dependency or configuration handling.
- **Detect** (deterministic): `exclude` inside a `configurations {` block, inside `configurations.configureEach {`, or an `exclude(group = "...")` / `exclude group:` with no `module` argument.
- **Fix:** see `references/fixes/apply_exclusions_narrowly.md` — read it only when you are about to apply this entry.

---

## Always Declare Attributes on Consumable and Resolvable Configurations
`use_attributes_on_configurations` · 9.7.0 · **High**

- **Rule:** Every custom consumable or resolvable configuration must declare at least one attribute, so variant-aware resolution can match it.
- **Applies when:** The build declares a custom configuration via `configurations.consumable(`, `configurations.resolvable(`, `configurations.create(`, or `configurations.dependencyScope(`. Otherwise not applicable.
- **Detect** (deterministic): such a declaration with no `attributes {` block; or a dependency declared against a named configuration (`configuration = "customElements"`, `project(path: ..., configuration: ...)`). The runtime symptom is "Unable to find a matching variant of project".
- **Fix:** see `references/fixes/use_attributes_on_configurations.md` — read it only when you are about to apply this entry.

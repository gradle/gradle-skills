# Structuring Builds

## Do Not Put Source Files in the Root Project · `no_source_in_root` · Medium
When: always — a single-project build with source in the root is exactly the case this describes.
Detect (det): a `src/main/` or `src/test/` directory at the root, and/or a language plugin (`java`, `java-library`, `application`, `groovy`, `kotlin("jvm")`) applied in the root `build.gradle(.kts)`.
Fix: Move `src/` into a new subproject with its own build script and `include("…")` it. Structural.

## Modularize Your Builds · `modularize_builds` · Recommendation
When: the build has one project, or one project holding unrelated concerns.
Detect (heur): a single project whose sources cover clearly separable concerns — unrelated top-level classes, or one build script mixing dependencies belonging to different layers (an application entry point plus utility code plus third-party integrations). Require concrete evidence: name the classes or dependency groups that would move.
Fix: Propose a decomposition into subprojects wired by `implementation(project(":…"))`. Structural.

## Favor `build-logic` Composite Builds for Build Logic · `favor_composite_builds` · Medium
When: `buildSrc/` exists.
Detect (det): a `buildSrc/` directory containing a build script or `src/main/` sources.
Fix: Move build logic into `build-logic/` with its own settings file, pulled in via `includeBuild`. Structural.

## Avoid Unintentionally Creating Empty Projects · `avoid_empty_projects` · Medium
When: the settings file uses a hierarchical include path.
Detect (det): an `include(` argument with two or more colons after the first, e.g. `include(":subs:web:my-web-module")`, without a matching `project(":...").projectDir = file(...)` assignment.
Fix: Set `project(":…").projectDir = file("…")` in settings so no empty intermediate project is synthesized.

## Use Convention Plugins · `use_convention_plugins` · Medium
When: the build has more than one project with a build script.
Detect (det where possible): the same configuration block in two or more build scripts — a `java { }` toolchain or source-compatibility block, `tasks.withType<JavaCompile>` settings, `useJUnitPlatform()`, `maxParallelForks`, or an identical `testImplementation(...)` declaration. Two occurrences is enough to report.
Fix: Extract the duplication into a precompiled script plugin under `build-logic/src/main/kotlin/`. Structural.

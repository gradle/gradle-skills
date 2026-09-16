# Structuring Builds

Base URL for every anchor below: `https://docs.gradle.org/current/userguide/best_practices_structuring_builds.html`

---

## Do Not Put Source Files in the Root Project
`no_source_in_root` · 9.0.0 · **Medium**

- **Rule:** The root project should carry shared settings and conventions, not source. Put source in subprojects.
- **Applies when:** Always (a single-project build with source in the root is exactly the case this describes).
- **Detect** (deterministic): a `src/main/` or `src/test/` directory at the root, and/or a language plugin (`java`, `java-library`, `application`, `groovy`, `kotlin("jvm")`) applied in the root `build.gradle(.kts)`.
- **Fix:** see `references/fixes/no_source_in_root.md` — read it only when you are about to apply this entry.

---

## Modularize Your Builds
`modularize_builds` · 9.0.0 · **Recommendation**

- **Rule:** Split the source into several projects so Gradle can avoid and parallelize work.
- **Applies when:** The build has one project, or one project holding unrelated concerns.
- **Detect** (heuristic): a single project whose sources cover clearly separable concerns — unrelated top-level classes, or one build script mixing dependencies that belong to different layers (an application entry point plus utility code plus third-party integrations). Require concrete evidence: name the classes or dependency groups that would move.
- **Fix:** see `references/fixes/modularize_builds.md` — read it only when you are about to apply this entry.

---

## Favor `build-logic` Composite Builds for Build Logic
`favor_composite_builds` · 9.0.0 · **Medium**

- **Rule:** Put custom plugins and shared build logic in an included composite build (conventionally `build-logic/`) rather than in `buildSrc/`.
- **Applies when:** `buildSrc/` exists.
- **Detect** (deterministic): a `buildSrc/` directory containing a build script or `src/main/` sources.
- **Fix:** see `references/fixes/favor_composite_builds.md` — read it only when you are about to apply this entry.

---

## Avoid Unintentionally Creating Empty Projects
`avoid_empty_projects` · 9.1.0 · **Medium**

- **Rule:** With nested directory layouts, set `projectDir` explicitly so Gradle does not synthesize empty intermediate projects.
- **Applies when:** The settings file uses a hierarchical include path.
- **Detect** (deterministic): an `include(` argument with two or more colons after the first, e.g. `include(":subs:web:my-web-module")`, without a matching `project(":...").projectDir = file(...)` assignment.
- **Fix:** see `references/fixes/avoid_empty_projects.md` — read it only when you are about to apply this entry.

---

## Use Convention Plugins
`use_convention_plugins` · 9.3.0 · **Medium**

- **Rule:** Put shared build logic in reusable convention plugins instead of duplicating configuration across build scripts.
- **Applies when:** The build has more than one project with a build script.
- **Detect** (deterministic where possible): the same configuration block appearing in two or more build scripts — a `java { }` toolchain or source-compatibility block, `tasks.withType<JavaCompile>` settings, `useJUnitPlatform()`, `maxParallelForks`, or an identical `testImplementation(...)` declaration. Two occurrences is enough to report.
- **Fix:** see `references/fixes/use_convention_plugins.md` — read it only when you are about to apply this entry.

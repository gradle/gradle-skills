# Testing

Base URL for the anchor below: `https://docs.gradle.org/current/userguide/best_practices_testing.html`

Read this file only if the project defines a custom task type or plugin. A build that merely consumes plugins has nothing to check here — count the entry as not applicable.

---

## Test your custom Task and Plugins with TestKit
`test_custom_types_with_testkit` · 9.4.0 · **Medium**

- **Rule:** Test custom tasks and plugins with Gradle TestKit, so they graduate from prototypes in a build script into reusable, verified components.
- **Applies when:** The project defines a custom task type or plugin — in `buildSrc/`, `build-logic/`, or inline in a build script.
- **Detect** (deterministic): a custom task class (`: DefaultTask()`, `extends DefaultTask`) or plugin (`: Plugin<Project>`, `implements Plugin<Project>`) exists, while no `gradleTestKit()` dependency and no `GradleRunner` usage appear anywhere in the build.
- **Fix:** see `references/fixes/test_custom_types_with_testkit.md` — read it only when you are about to apply this entry.

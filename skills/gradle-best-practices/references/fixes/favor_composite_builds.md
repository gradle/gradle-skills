# Favor `build-logic` Composite Builds for Build Logic
`favor_composite_builds`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Create `build-logic/` with its own `settings.gradle(.kts)` and a `plugin/` project, move the sources across, declare the plugins with `gradlePlugin { plugins { create("myPlugin") { id = ...; implementationClass = ... } } }`, and add `includeBuild("build-logic")` to the root settings file. Structural.

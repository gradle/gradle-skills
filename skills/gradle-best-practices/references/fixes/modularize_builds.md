# Modularize Your Builds
`modularize_builds`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Propose a decomposition (`app/`, `util/`, `util-guava/`, …), each with its own build script, wired by `implementation(project(":util-guava"))`, applying each plugin only where it belongs. Structural — describe the plan and get confirmation before moving files.

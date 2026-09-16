# Use Convention Plugins
`use_convention_plugins`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Extract to a precompiled script plugin in `build-logic/src/main/kotlin/` (e.g. `my.java-library.gradle.kts`), compose small plugins rather than one large one, and apply with `plugins { id("my.java-library") }`.

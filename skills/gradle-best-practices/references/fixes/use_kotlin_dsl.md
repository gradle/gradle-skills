# Use Kotlin DSL
`use_kotlin_dsl`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** Migrate the script to `.gradle.kts`. This is a structural fix — describe the plan and convert incrementally, one script at a time, confirming the build still succeeds after each.

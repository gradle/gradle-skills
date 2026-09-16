# Enable UTF-8
`use_utf8_encoding`

Fix reference for one entry. The rule, precondition and detection recipe
stay in the category file; this is what to write once you have decided to apply it.

---

- **Fix:** In the root `gradle.properties`: `org.gradle.jvmargs=-Dfile.encoding=UTF-8` (append to any existing value rather than replacing it).

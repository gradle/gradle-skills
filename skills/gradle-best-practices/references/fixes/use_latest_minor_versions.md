# Use the Latest Minor Version of Gradle
`use_latest_minor_versions`

**Rule:** Stay on the latest minor version of the major Gradle release in use, and keep plugins on their latest compatible versions.

---

- **Fix:** Target the **latest minor of the major the project is already on** — crossing a major is a separate job, and being on 8.x is not itself the finding.

  Hand the upgrade to the **`gradle-wrapper-upgrade`** skill, which owns the procedure. Do not reproduce it here, and never hand-edit `gradle-wrapper.properties`.

  Then update plugins and test compatibility — Gradle before plugins.

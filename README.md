# Gradle Skills

[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

Skills that teach AI coding agents how to work on Gradle builds.

They follow the [Agent Skills](https://agentskills.io/home) format, so they work in any agent that reads it: Claude Code, Codex, Cursor, Gemini CLI, and others.

## Available Skills

### gradle-best-practices [![v1.0.0](https://img.shields.io/badge/v1.0.0-02303A?logo=gradle&logoColor=white)](skills/gradle-best-practices)

Audits a build against the [official Gradle best practices](https://docs.gradle.org/current/userguide/best_practices.html) and reports what it finds, ordered by impact. Ask it to, and it applies the fixes.

It reads build scripts, settings files, `gradle.properties`, the wrapper config, the version catalog, and the plugin code under `buildSrc/` and `build-logic/`. Every finding links to the practice it came from.

[Benchmark results](evals/gradle-best-practices/gradle-best-practices-1.0.0.md) across several models and agents.

Try:

- "Check my build"
- "Audit this Gradle project"
- "Apply Gradle best practices"

### gradle-wrapper-upgrade [![v1.0.0](https://img.shields.io/badge/v1.0.0-02303A?logo=gradle&logoColor=white)](skills/gradle-wrapper-upgrade)

Upgrades the Gradle wrapper, to the latest release or to a version you name. It pins the distribution's checksum, regenerates `gradlew`, `gradlew.bat`, and the wrapper jar, and then checks that the build still configures on the new version. If it doesn't, the upgrade is rolled back and you get a smaller version step to try instead, with the release notes for it.

Ask *how* to upgrade and you get the commands, not a changed working tree.

It upgrades a wrapper that already exists. It won't add one to a project that has none, and it won't edit your build scripts.

[Benchmark results](evals/gradle-wrapper-upgrade/gradle-wrapper-upgrade-1.0.0.md) across several models and agents.

Try:

- "Upgrade the Gradle wrapper"
- "Bump Gradle to 8.14.4"
- "How do I upgrade the wrapper?"

## Installation

Install the plugin to use all of the skills.

### Claude Code

```text
/plugin marketplace add gradle/gradle-skills
/plugin install gradle-skills@gradle-skills
```

Claude Code namespaces skills that come from a plugin, so these load as `gradle-skills:gradle-best-practices` and `gradle-skills:gradle-wrapper-upgrade`.

To set this up for a whole team, commit to the project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "gradle-skills": {
      "source": {
        "source": "github",
        "repo": "gradle/gradle-skills"
      }
    }
  },
  "enabledPlugins": {
    "gradle-skills@gradle-skills": true
  }
}
```

That registers the marketplace, but doesn't fetch the plugin. Each collaborator still runs the install once:

```bash
claude plugin install gradle-skills@gradle-skills
```

### Codex, Cursor, Gemini CLI, and others

```bash
npx skills add gradle/gradle-skills
```

Choose your agents when prompted. The skills are written to `.agents/skills/` in the current project; pass `-g` to install them for every project instead. Re-run the command to update.

This covers around 80 agents. [`skills.sh`](https://skills.sh/) has the list, and `npx` needs Node (`brew install node`).

### Anything else

The repository root is also an [Agent Plugins 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) package: `plugin.json` is the manifest, `skills/` holds the skills. Clients that implement the standard can install it directly. Each defines its own procedure, so check your agent's docs or the [list of compatible clients](https://agent-plugins.org/compatible-clients).

## What the Skills Touch

Neither skill declares `allowed-tools`, so both run under whatever permission model your agent already applies — they neither restrict nor pre-approve anything on your behalf. What they actually do:

### `gradle-best-practices`

| | |
|---|---|
| **Reads** | Settings files, build scripts, `gradle.properties`, wrapper config, the version catalog, and Java/Kotlin/Groovy sources under `buildSrc/` and `build-logic/` — plus its own bundled catalog under `references/`. |
| **Writes** | Nothing in audit mode. In apply mode it edits the files above. On request it also writes an HTML report to `build/reports/best-practices-audit.html`. |
| **Runs** | Nothing, unless a fix needs verifying. |
| **Network** | None. The catalog ships with the skill and is read from disk. |

### `gradle-wrapper-upgrade`

| | |
|---|---|
| **Reads** | `gradle/wrapper/gradle-wrapper.properties` and the wrapper scripts. |
| **Writes** | It does not hand-edit the wrapper files — that is the skill's central rule. All four change because Gradle's own `wrapper` task rewrites them. |
| **Runs** | `./gradlew` (the `wrapper` and `tasks` tasks), `curl` against `services.gradle.org`, and `git` — `status` to check the tree, and `checkout --` on the four wrapper paths to roll back a blocked upgrade. |
| **Network** | Yes, unavoidably: it fetches the published SHA-256, and the second `wrapper` run downloads the full distribution (100 MB+). |
| **Outside the project** | Where the tree is dirty or not in git, it copies the four wrapper files to a `mktemp -d` directory, and deletes it once the upgrade verifies. |

Neither skill reaches for a web-search or page-fetch tool. Across the benchmark runs in [`evals/`](evals), all 70 treatment arms made zero `WebFetch`/`WebSearch` calls — the best-practices skill reads its bundled catalog instead, and the wrapper skill goes to a known URL over `curl`.

If you would rather enforce that than trust it, both skills work with web fetch and search denied, and the wrapper skill works with file-write tools denied as well. `gradle-best-practices` needs write access only in apply mode; denying it leaves audit mode working, minus the optional HTML report.

## Repository Structure

```text
plugin.json        Agent Plugins manifest
skills.sh.json     skills.sh grouping
.claude-plugin/    Claude Code plugin manifest and marketplace catalog
skills/<name>/
  SKILL.md         instructions, loaded when the skill triggers
  metadata.json    version, owner, abstract, sources
  references/      loaded on demand, not on trigger
evals/<name>/      benchmark results per skill version
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) to get started, and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for the community standards this project follows.

## Security

Do not report security vulnerabilities in the public issue tracker; see [SECURITY.md](SECURITY.md).

## License

Apache License 2.0 — see [LICENSE](LICENSE).

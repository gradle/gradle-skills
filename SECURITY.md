# Security Policy

This repository is covered by the [Gradle Vulnerability Disclosure Policy](https://github.com/gradle/.github/blob/master/SECURITY.md), which describes the scope, the guidelines for research, and safe harbor.

## Reporting a vulnerability

Do not report security vulnerabilities to the public issue tracker.
Send them to [security@gradle.com](mailto:security@gradle.com), naming the skill and the file involved.

## What counts as a vulnerability in a skill

A skill is a set of instructions an AI agent follows with the user's permissions, usually in a shell with access to the project and its credentials.
A flaw in those instructions is a security issue when following them as written can harm the user. For example, a skill that:

- tells the agent to skip or weaken a security control, such as distribution checksum verification, dependency verification, or repository content filtering;
- has the agent download and run code, or change the build to use a distribution or artifact, from a source that is not verified;
- causes credentials, tokens, or other secrets to be written to logs, reports, or files that get committed;
- lets content from the project under analysis, such as build scripts, properties, or dependency metadata, steer the agent into actions outside the skill's stated scope.

Guidance that is merely wrong or outdated, without a security impact, is a regular bug; open an issue for it.

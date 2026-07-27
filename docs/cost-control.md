# Cost Control & Rate Limiting

## Overview

This document defines the policy for controlling API costs and usage limits for OpenCode workflow executions.

## Default Limits

| Limit | Value | Variable Name |
|---|---|---|
| Max runs per hour | 20 | `MAX_HOURLY_RUNS` |
| Max runs per day | 100 | `MAX_DAILY_RUNS` |

Limits are configurable via [GitHub Actions Variables](https://docs.github.com/en/actions/learn-github-actions/variables) at the repository level:
`Settings → Secrets and variables → Actions → Variables`

## Command Priorities

When approaching rate limits, commands are prioritized:

| Priority | Category | Behavior |
|---|---|---|
| 1 (highest) | `fix`, `security` | Always executed regardless of limit |
| 2 | `feat` | Executed if under limit |
| 3 (lowest) | `refactor`, `docs`, `chore`, `style` | Skipped when near limit |

## Rate Limit Enforcement

The `opencode.yml` workflow enforces limits via these steps:

1. **Pre-flight check** — before running the agent, a script queries recent workflow runs via `gh run list` and counts executions within the current hour and day.
2. **Limit evaluation** — if either hourly or daily limit is exceeded, the workflow fails with a clear message.
3. **Alert notification** — on failure, a GitHub Issue is created automatically with details about the exceeded limit.

## Alert Notification

When a rate limit is exceeded, an issue is created in the repository with:
- Title: `⚠️ Rate limit exceeded`
- Body: includes the limit type (hourly/daily), current count, and limit value
- The workflow run URL for debugging

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `MAX_HOURLY_RUNS` | No | 20 | Max workflow runs per hour |
| `MAX_DAILY_RUNS` | No | 100 | Max workflow runs per day |

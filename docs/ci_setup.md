# GitHub Actions & Security Setup

| Secret          | Where to add                     | Scope      |
| --------------- | -------------------------------- | ---------- |
| `CODECOV_TOKEN` | **Settings → Secrets → Actions** | repository |

1. Go to _Settings → Actions → General_ and set:<br>
   • **Workflow permissions** → _Read and write permissions_ ✔<br>
   • **Allow GitHub Actions to create and approve pull requests** (optional).

2. If self-hosted runners are used, ensure they have the correct labels and are online.

Workflows will fail fast with a clear error if `CODECOV_TOKEN` is absent.

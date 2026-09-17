#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/bootstrap-repository-protection.sh OWNER/REPO

Purpose:
  Apply the Ro-ASD repository-level protection baseline to a NEW public repository.
  This is the enforcement fallback for GitHub Free organizations where
  organization-level rulesets are not enforced.

Safety:
  - refuses repositories outside Project-Ro-ASD
  - refuses archived or non-public repositories
  - refuses repositories whose default branch is already protected
  - never weakens or overwrites existing repository protection
  - adds ro-app-gate only when roasd_type=application
EOF
}

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

[[ $# -eq 1 ]] || { usage >&2; exit 2; }
REPO="$1"
[[ "$REPO" == Project-Ro-ASD/* ]] || fail "repository must be under Project-Ro-ASD"

command -v gh >/dev/null 2>&1 || fail "GitHub CLI (gh) is required"
command -v jq >/dev/null 2>&1 || fail "jq is required"
gh auth status >/dev/null 2>&1 || fail "gh is not authenticated; run: gh auth login"

REPO_JSON="$(gh api "repos/${REPO}")"
ARCHIVED="$(jq -r '.archived' <<<"$REPO_JSON")"
VISIBILITY="$(jq -r '.visibility // empty' <<<"$REPO_JSON")"
DEFAULT_BRANCH="$(jq -r '.default_branch // empty' <<<"$REPO_JSON")"
ROASD_TYPE="$(jq -r '.custom_properties.roasd_type // "unclassified"' <<<"$REPO_JSON")"

[[ "$ARCHIVED" == "false" ]] || fail "repository is archived"
[[ "$VISIBILITY" == "public" ]] || fail "free-plan bootstrap v1 only supports public repositories"
[[ -n "$DEFAULT_BRANCH" ]] || fail "repository has no default branch"

if gh api "repos/${REPO}/branches/${DEFAULT_BRANCH}/protection" >/dev/null 2>&1; then
  fail "${REPO}:${DEFAULT_BRANCH} is already protected; refusing to overwrite existing protection"
fi

if [[ "$ROASD_TYPE" == "application" ]]; then
  REQUIRED_STATUS_CHECKS='{"strict":true,"contexts":["ro-app-gate"]}'
else
  REQUIRED_STATUS_CHECKS='null'
fi

jq -n \
  --argjson checks "$REQUIRED_STATUS_CHECKS" \
  '{
    required_status_checks: $checks,
    enforce_admins: true,
    required_pull_request_reviews: {
      dismiss_stale_reviews: false,
      require_code_owner_reviews: false,
      required_approving_review_count: 0,
      require_last_push_approval: false
    },
    restrictions: null,
    required_linear_history: false,
    allow_force_pushes: false,
    allow_deletions: false,
    block_creations: false,
    required_conversation_resolution: false,
    lock_branch: false,
    allow_fork_syncing: true
  }' | gh api \
      --method PUT \
      -H 'Accept: application/vnd.github+json' \
      -H 'X-GitHub-Api-Version: 2022-11-28' \
      "repos/${REPO}/branches/${DEFAULT_BRANCH}/protection" \
      --input - >/dev/null

printf 'Ro-ASD repository protection applied.\n'
printf '  repository: %s\n' "$REPO"
printf '  default branch: %s\n' "$DEFAULT_BRANCH"
printf '  roasd_type: %s\n' "$ROASD_TYPE"
if [[ "$ROASD_TYPE" == "application" ]]; then
  printf '  required status: ro-app-gate\n'
else
  printf '  required status: none (common baseline only)\n'
fi
printf '  pull request required: yes\n'
printf '  force push: blocked\n'
printf '  deletion: blocked\n'
printf '  admins enforced: yes\n'

#!/bin/bash
# Setup a test git repo with controlled history for weekly-report-generator eval
set -e

TEST_REPO="$HOME/.claude/skills/weekly-report-generator-workspace/test-repo"
rm -rf "$TEST_REPO"
mkdir -p "$TEST_REPO"
cd "$TEST_REPO"

git init
git config user.email "test@example.com"
git config user.name "Test User"

mkdir -p src/utils

# Commit 1: Monday (2 days ago)
echo "// TODO: implement user login" > src/auth.ts
echo "export const API_URL = 'http://localhost:3000';" > src/config.ts
echo "export function sum(a: number, b: number): number { return a + b; }" > src/utils/math.ts
git add .
GIT_COMMITTER_DATE="2026-06-29T10:00:00" git commit -m "feat: add initial project structure" --date="2026-06-29T10:00:00"

# Commit 2: Monday afternoon
echo "// FIXME: handle edge case when password is empty" >> src/auth.ts
echo "export async function login(user: string, pass: string): Promise<boolean> {" >> src/auth.ts
echo "  if (!pass) throw new Error('empty password');" >> src/auth.ts
echo "  return true;" >> src/auth.ts
echo "}" >> src/auth.ts
GIT_COMMITTER_DATE="2026-06-29T14:30:00" git commit -m "feat(auth): add login function" --date="2026-06-29T14:30:00" -a

# Commit 3: Tuesday (today/yesterday)
echo "// fix: validate email format before login" >> src/auth.ts
echo "export function validateEmail(email: string): boolean {" >> src/auth.ts
echo "  return email.includes('@');" >> src/auth.ts
echo "}" >> src/auth.ts
echo "" > src/utils/string.ts
echo "export function capitalize(s: string): string {" >> src/utils/string.ts
echo "  return s.charAt(0).toUpperCase() + s.slice(1);" >> src/utils/string.ts
echo "}" >> src/utils/string.ts
GIT_COMMITTER_DATE="2026-06-30T09:15:00" git commit -m "fix(auth): add email validation" --date="2026-06-30T09:15:00" -a

# Add another author commit
git config user.email "dev2@example.com"
git config user.name "Dev Two"
echo "// TODO: optimize query performance" >> src/utils/math.ts
echo "// HACK: temporary workaround for safari bug" >> src/config.ts
GIT_COMMITTER_DATE="2026-06-30T11:00:00" git commit -m "chore: add performance notes and browser workaround" --date="2026-06-30T11:00:00" -a

# Reset author
git config user.email "test@example.com"
git config user.name "Test User"

echo ""
echo "=== Test repo created at $TEST_REPO ==="
echo "=== Commit log ==="
git log --format="%ad|%an|%s" --date=short
echo ""
echo "=== TODO/FIXME grep ==="
grep -rn "TODO\|FIXME\|HACK" --include="*.ts" .

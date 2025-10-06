# Git Commit Workflow - MANDATORY PROCESS

## 🔴 CRITICAL RULE: Stage ONLY Immediately Before Commit

**NEVER stage files early during development. Staging is the LAST step before committing.**

## The Problem with Early Staging

**What happens when you stage too early:**

1. ⏰ **Time T1**: You stage files with `git add`
   - Staging area = snapshot at T1
2. ⏰ **Time T2-T5**: You continue working
   - Update config files
   - Run tests (generates test reports)
   - Update documentation
   - Modify settings
3. ⏰ **Time T6**: You commit with `git commit`
   - **Only commits the T1 snapshot**
   - **All work after T1 is MISSING**

**Result: Incomplete, broken atomic commits**

## Correct Atomic Commit Workflow

### Phase 1: DO ALL THE WORK FIRST

```bash
# Make ALL code changes
# Run ALL tests
# Update ALL documentation
# Modify ALL config files
# Generate ALL test reports

# ⚠️ DO NOT RUN git add YET
```

### Phase 2: VERIFY EVERYTHING IS COMPLETE

```bash
# Check what files changed
git status

# Review all changes
git diff

# Ensure:
✅ All code changes complete
✅ All tests passing
✅ All docs updated
✅ All config files modified
✅ All test reports generated
```

### Phase 3: STAGE EVERYTHING AT ONCE

```bash
# Stage ALL related files in ONE command
git add -A

# OR stage specific files if you're certain:
git add file1.py file2.ts test-report.txt config.json docs.md

# ⚠️ This is the FIRST time you should run git add
```

### Phase 4: VERIFY STAGING IMMEDIATELY

```bash
# Check staging area
git status

# Should show:
# - Changes to be committed: [ALL your files]
# - Changes not staged for commit: [NONE related to your task]
# - Untracked files: [NONE related to your task]

# If anything is unstaged/untracked that should be included:
git add [missing-file]
```

### Phase 5: COMMIT IMMEDIATELY

```bash
# Create commit RIGHT AFTER staging
git commit -m "$(cat <<'EOF'
[TAG] Descriptive commit message

- Change 1
- Change 2
- Change 3

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# ⚠️ NO DELAY between git add and git commit
```

### Phase 6: PUSH IMMEDIATELY

```bash
# Push right after commit
git push

# Verify push succeeded
```

## Timeline: Correct vs Incorrect

### ❌ INCORRECT (Early Staging)

```
09:00 - Edit backend files → git add backend/
09:15 - Edit frontend files → git add frontend/
09:30 - Update docs → git add docs/
09:45 - Run tests (generates test-reports/) ← NOT staged
10:00 - Update .claude/settings.local.json ← NOT staged
10:15 - git commit ← INCOMPLETE! Missing test reports + settings
```

### ✅ CORRECT (Stage at End)

```
09:00 - Edit backend files
09:15 - Edit frontend files
09:30 - Update docs
09:45 - Run tests (generates test-reports/)
10:00 - Update .claude/settings.local.json
10:15 - git status (verify all changes)
10:16 - git add -A ← Stage EVERYTHING
10:17 - git status (verify staging)
10:18 - git commit ← COMPLETE! All files included
10:19 - git push
```

## What Belongs in an Atomic Commit

**A single atomic commit should include:**

1. ✅ **Code changes** (backend + frontend)
2. ✅ **Test files** (if modified)
3. ✅ **Test reports** (evidence of passing tests)
4. ✅ **Documentation updates** (CLAUDE.md, README.md, etc.)
5. ✅ **Memory updates** (.serena/memories/)
6. ✅ **Config changes** (.claude/settings.local.json, etc.)
7. ✅ **Task plan updates** (TODO_task_plan.md, etc.)

**All of these should be staged together, at the END, in ONE `git add` command.**

## Common Mistakes to Avoid

### Mistake 1: Staging as You Go

```bash
❌ git add backend/api.py
❌ [continue working...]
❌ git add frontend/component.tsx
❌ [continue working...]
❌ git add docs/README.md
❌ [run tests - generates reports]
❌ git commit  # ← Missing test reports!
```

### Mistake 2: Forgetting Test Evidence

```bash
❌ git add src/
❌ git add docs/
❌ git commit  # ← Where are the test reports?
```

### Mistake 3: Ignoring Config Changes

```bash
❌ git add src/ docs/ test-reports/
❌ git commit  # ← Missing .claude/settings.local.json!
```

## Verification Checklist Before Commit

**Before running `git commit`, verify:**

- [ ] All code changes complete and working
- [ ] All tests passing (27/27 PASS for this project)
- [ ] Test reports generated and reviewed
- [ ] All documentation updated (CLAUDE.md, tech_stack.md, etc.)
- [ ] All config files modified (if needed)
- [ ] All Serena memories updated (if needed)
- [ ] `git status` shows ALL files staged
- [ ] `git status` shows NOTHING unstaged that should be included
- [ ] No more than 60 seconds between `git add` and `git commit`

## Recovery from Early Staging

**If you already staged files too early:**

```bash
# Option 1: Unstage everything and start over
git reset HEAD

# Do remaining work
[finish all tasks...]

# Stage everything at once
git add -A

# Commit immediately
git commit -m "..."
```

```bash
# Option 2: Add missing files before committing
git status  # See what's unstaged

git add [missing-file-1]
git add [missing-file-2]

# Verify everything is staged
git status

# Commit immediately
git commit -m "..."
```

## Why This Matters

**Atomic commits are the foundation of:**

1. **Reproducible builds** - Anyone can checkout the commit and it works
2. **Clean history** - Each commit is a complete, working unit
3. **Easy rollbacks** - Can revert entire feature, not partial changes
4. **Code review** - Reviewers see ALL related changes together
5. **CI/CD** - Build systems expect complete, working commits

**Incomplete commits break all of these.**

## Enforcement

**In this project, atomic commits are MANDATORY:**

- 🔴 Commits missing test evidence will be reverted
- 🔴 Commits missing documentation will be reverted
- 🔴 Commits with partial changes will be reverted
- ✅ Only complete atomic commits are acceptable

## Summary

1. **DO ALL WORK FIRST** (code, tests, docs, config)
2. **VERIFY COMPLETION** (git status, review changes)
3. **STAGE EVERYTHING** (git add -A)
4. **VERIFY STAGING** (git status again)
5. **COMMIT IMMEDIATELY** (git commit)
6. **PUSH IMMEDIATELY** (git push)

**Remember: `git add` is the LAST step before `git commit`, not a step during development.**

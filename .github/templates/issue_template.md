## 🔗 Jira Reference

[{bug_key}]({jira_url}) • {priority} Priority • Status: {status}

## 📝 Description

{description}

## 🖥️ Environment

```
{environment}
```

{attachments_section}

{custom_fields_section}

---

## 🤖 Instructions for GitHub Copilot Workspace

### 🎯 Your Mission

Analyze this Jira bug, reproduce it, and implement a minimal, tested fix.

### ⚠️ CRITICAL RULE: Surgical Edits Only

**DO NOT replace entire files!** Make targeted changes to only the problematic code:

- ✅ Edit specific lines/functions that need fixing
- ✅ Preserve all existing data and structure
- ❌ Never delete and recreate entire files
- ❌ Never rewrite data files completely

**Example:** If student ID 8 has wrong data, fix only that entry - don't regenerate all 300+ lines!

### 📍 Primary Code Location

**Search in:** `brand-landscape-analyzer-app/` or `student-management-app/` folder first

---

## ⚡ Quick Start Guide

### Phase 1️⃣: Investigation (Required)

**Before writing any code, complete these steps:**

1. **🔍 Search the repository:**
   - Search for keywords from the issue title and description
   - Check recent commits that might have introduced this bug
   - Look for related test files
   - **List all files you examined** in your final comment

2. **📎 Inspect attachments** (if present):
   - Download screenshots and view at full resolution
   - For images with text: extract error messages using OCR
   - Review logs for: stack traces, error codes, timestamps
   - **Document findings:** error messages, affected components

3. **🔄 Attempt to reproduce:**
   - Follow the reproduction steps from the description exactly
   - Record the exact commands/inputs you used
   - Document actual vs expected behavior
   - **If cannot reproduce:** STOP and add a comment explaining why

### Phase 2️⃣: Fix (Only if reproducible)

**If you successfully reproduced the bug:**

4. **🔧 Implement minimal fix:**
   - **CRITICAL: Make surgical edits only** - modify only the broken lines
   - DO NOT rewrite entire files or functions
   - DO NOT replace data files completely (edit specific entries only)
   - Keep existing code structure and formatting
   - Avoid refactoring unrelated code
   - Root cause should be clear in your implementation
   - **Example:** For a data validation bug, fix only the validation logic, not the entire file

5. **🧪 Add/update tests:**
   - Write a test that reproduces the bug (fails before fix)
   - Verify test passes after your fix
   - Keep tests small and deterministic
   - Run full test suite and fix any failures

6. **✅ Validate thoroughly:**
   - Manually verify fix using original reproduction steps
   - Test edge cases
   - Ensure no regressions in related functionality

### Phase 3️⃣: Document & Submit

7. **🌿 Create branch:**

   ```
   fix/{bug_key}-brief-description
   ```

   Example: `fix/SCRUM-38-search-numericals`

8. **📝 Create Pull Request** with this structure:

````markdown
## Fixes [{bug_key}]({jira_url})

### 🐛 Problem

[Root cause explanation]

### 🔧 Solution

[Your fix approach]

### 📁 Files Changed

- `path/file.ext` - [what changed and why]

### 🧪 Tests Added/Modified

- `path/test.ext` - [test coverage]

### 🔍 Findings from Attachments

[Error messages, log analysis, screenshot insights]

### ✅ Validation Steps

```bash
# How to verify the fix locally:
# 1. [command or action]
# 2. [expected result]
```
````

### ⚠️ Risks / Follow-ups

[Any concerns or future improvements]

````

9. **💬 Post summary comment on this issue:**
```markdown
🤖 **Copilot Fix Summary**

**Reproducibility:** ✅ Reproduced / ❌ Could not reproduce
**Root Cause:** [Brief explanation]
**Files Changed:** [List with brief descriptions]
**Tests Added:** [Test file paths]
**Attachment Findings:** [Key discoveries from logs/screenshots]
**Validation:** [How to verify the fix]
**PR:** #[PR number]
**Follow-ups:** [Any remaining tasks]
````

---

## ✅ DO:

- ✅ Search repository thoroughly before making changes
- ✅ Download and analyze ALL attachments
- ✅ Extract text from error screenshots using OCR
- ✅ Document reproduction attempt clearly
- ✅ **Make surgical edits - change only the problematic code**
- ✅ **Preserve existing file structure and formatting**
- ✅ Add tests that verify your fix
- ✅ Run full test suite
- ✅ Create properly named branch
- ✅ Write detailed PR following the template
- ✅ Post summary comment on this issue

## ❌ DON'T:

- ❌ **Replace entire files when only a few lines need fixing**
- ❌ **Rewrite data files completely - edit specific entries only**
- ❌ Create PR if bug cannot be reproduced (comment instead)
- ❌ Add new top-level modules without strong justification
- ❌ Modify `.gitignore` or unrelated config files
- ❌ Add excessive comments (only for non-obvious logic)
- ❌ Refactor unrelated code or reformat files
- ❌ Skip test validation
- ❌ Make assumptions without documenting them

---

## 🚨 If You Cannot Reproduce:

**DO NOT create a PR. Instead:**

1. Add a detailed comment explaining:
   - What you tried (exact steps, commands)
   - Why reproduction failed
   - What information is missing
2. Tag the reporter: @{reporter}
3. Ask for clarification on specific points

---

## 🎓 Success Criteria:

- [ ] Bug reproduced OR detailed explanation of why not
- [ ] Root cause identified and documented
- [ ] Minimal fix implemented in existing files
- [ ] Tests added that verify the fix
- [ ] Full test suite passes
- [ ] PR created with complete documentation
- [ ] Summary comment posted on this issue
- [ ] All findings from attachments documented

---

**🚀 Start by replying:** "🤖 Copilot assigned to {bug_key}. Beginning investigation..."

---

<sub>📅 Created: {created} • Updated: {updated} • Synced from Jira</sub>

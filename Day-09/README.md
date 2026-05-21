# Day 9: Create a Custom ML Project Template with Cookiecutter

**Date:** Day 9 of 100  
**Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium-Hard  
**Time Required:** ~25-30 minutes

---

## 📋 Task Summary

Fix and configure a Cookiecutter template that generates new ML projects with customizable settings. The template must properly define variables, conditionally include dependencies, and render all required files.

### ✅ Learning Objectives

After completing this task, you will understand:
- How Cookiecutter templates work
- The `cookiecutter.json` configuration
- Template variable syntax
- Jinja2 conditional logic in templates
- Template directory structure
- Generating projects from templates
- Project scaffolding best practices

---

## 🎯 Task Requirements

### Requirement 1: cookiecutter.json Variables

Four variables must be defined:

```json
{
    "project_name": "my-ml-project",
    "author": "xFusionCorp",
    "python_version": "3.11",
    "ml_framework": {
        "choices": ["sklearn", "pytorch", "tensorflow"]
    }
}
```

Or using list syntax:
```json
{
    "project_name": "my-ml-project",
    "author": "xFusionCorp",
    "python_version": "3.11",
    "ml_framework": ["sklearn", "pytorch", "tensorflow"]
}
```

### Requirement 2: Conditional Dependencies

The `requirements.txt` must use Jinja2 conditionals:

```jinja
{% if cookiecutter.ml_framework == 'sklearn' %}
scikit-learn
{% elif cookiecutter.ml_framework == 'pytorch' %}
torch
{% elif cookiecutter.ml_framework == 'tensorflow' %}
tensorflow
{% endif %}
```

**Critical syntax:**
- Use `==` (equals), NOT `=` (assignment)
- Use `elif`, NOT `else if`
- Variable format: `{{ cookiecutter.VARIABLE_NAME }}`
- Close with `{% endif %}`

### Requirement 3: README References Variables

The `README.md` must mention both `project_name` and `author`:

```markdown
# {{cookiecutter.project_name}}

Created by {{cookiecutter.author}}.
```

**Critical syntax:**
- Variable names must match exactly (case-sensitive)
- Use `author`, NOT `Author`
- Use `{{` and `}}` (double braces)

### Requirement 4: Template Directory Structure

```
mlops-template/
├── cookiecutter.json
└── {{cookiecutter.project_name}}/
    ├── README.md
    ├── requirements.txt
    ├── data/
    ├── models/
    ├── src/
    └── tests/
```

---

## 🚀 Step-by-Step Solution

### Step 1: Navigate to Template

```bash
cd /root/code/mlops-template/

# Verify we're in the right place
pwd
ls -la
```

### Step 2: Review Current State

```bash
# View current cookiecutter.json
cat cookiecutter.json

# View current requirements.txt (with escapes shown)
cat "{{cookiecutter.project_name}}/requirements.txt"

# View current README.md
cat "{{cookiecutter.project_name}}/README.md"
```

**Current issues:**

```json
{
    "project_name": "my-ml-project",
    "author": "xFusionCorp",
    "python_version": "3.11"
    // ❌ Missing: "ml_framework" variable with choices
}
```

```jinja
{% if cookiecutter.ml_framework = 'sklearn' %}  # ❌ Uses = not ==
scikit-learn
{% elif cookiecutter.ml_framework = 'pytorch' %}
torch
{% elif cookiecutter.ml_framework = 'tensorflow' %}
tensorflow
// ❌ Missing: {% endif %}
```

```markdown
# {{cookiecutter.project_name}}
Created by {{ cookiecutter.Author }}.  # ❌ Author (capital A), should be author
```

### Step 3: Fix cookiecutter.json

Replace the entire file:

```bash
cat > cookiecutter.json << 'EOF'
{
    "project_name": "my-ml-project",
    "author": "xFusionCorp",
    "python_version": "3.11",
    "ml_framework": ["sklearn", "pytorch", "tensorflow"]
}
EOF
```

**Key changes:**
1. ✅ Added `ml_framework` with three choices
2. ✅ Used list format: `["sklearn", "pytorch", "tensorflow"]`

### Step 4: Fix requirements.txt

Navigate to the template directory and fix the file:

```bash
# Create/fix requirements.txt with correct Jinja2 syntax
cat > "{{cookiecutter.project_name}}/requirements.txt" << 'EOF'
{% if cookiecutter.ml_framework == 'sklearn' %}
scikit-learn
{% elif cookiecutter.ml_framework == 'pytorch' %}
torch
{% elif cookiecutter.ml_framework == 'tensorflow' %}
tensorflow
{% endif %}
EOF
```

**Key changes:**
1. ✅ Changed `=` to `==` (comparison operator)
2. ✅ Added missing `{% endif %}`
3. ✅ Correct Jinja2 syntax

### Step 5: Fix README.md

```bash
cat > "{{cookiecutter.project_name}}/README.md" << 'EOF'
# {{cookiecutter.project_name}}

Created by {{cookiecutter.author}}.
EOF
```

**Key changes:**
1. ✅ Changed `Author` to `author` (lowercase)
2. ✅ Removed extra space in `{{ cookiecutter.author }}`
3. ✅ Correct variable reference

### Step 6: Verify Directory Structure

Check that all required directories exist:

```bash
# List all directories in template
ls -la "{{cookiecutter.project_name}}/"

# Create missing directories if needed
mkdir -p "{{cookiecutter.project_name}}/data"
mkdir -p "{{cookiecutter.project_name}}/models"
mkdir -p "{{cookiecutter.project_name}}/src"
mkdir -p "{{cookiecutter.project_name}}/tests"

# Verify structure
ls -la "{{cookiecutter.project_name}}/"
```

**Expected structure:**
```
{{cookiecutter.project_name}}/
├── README.md
├── requirements.txt
├── data/
├── models/
├── src/
└── tests/
```

### Step 7: Verify Template Configuration

```bash
# View final cookiecutter.json
cat cookiecutter.json

# View final requirements.txt
cat "{{cookiecutter.project_name}}/requirements.txt"

# View final README.md
cat "{{cookiecutter.project_name}}/README.md"
```

### Step 8: Test Template Rendering

Try a quick test render:

```bash
# Test with sklearn framework
cookiecutter /root/code/mlops-template/ \
  -o /tmp/test-template \
  --no-input \
  project_name=test-project \
  ml_framework=sklearn

# Verify it was created
ls -la /tmp/test-template/test-project/

# Check generated requirements.txt
cat /tmp/test-template/test-project/requirements.txt

# Check generated README.md
cat /tmp/test-template/test-project/README.md
```

### Step 9: Generate Project at Specified Location

Generate the actual project:

```bash
# Generate churn-model project with sklearn
cookiecutter /root/code/mlops-template/ \
  -o /root/code/ \
  --no-input \
  project_name=churn-model \
  ml_framework=sklearn
```

### Step 10: Verify Generated Project

```bash
# List the generated project
ls -la /root/code/churn-model/

# Check requirements.txt contains scikit-learn
cat /root/code/churn-model/requirements.txt

# Check README.md mentions xFusionCorp
cat /root/code/churn-model/README.md

# Verify directory structure
ls -la /root/code/churn-model/
```

**Expected outputs:**

**requirements.txt:**
```
scikit-learn
```

**README.md:**
```
# churn-model

Created by xFusionCorp.
```

**Directory structure:**
```
churn-model/
├── README.md
├── requirements.txt
├── data/
├── models/
├── src/
└── tests/
```

---

## 📝 Understanding Cookiecutter

### cookiecutter.json Structure

```json
{
    "variable_name": "default_value",
    "choices_list": ["option1", "option2", "option3"],
    "complex_choice": {
        "choices": ["opt1", "opt2"]
    }
}
```

**Types:**
- String: `"project_name": "default"`
- List (for choices): `"framework": ["sklearn", "pytorch"]`
- Object (for choices): `"framework": {"choices": ["sklearn", "pytorch"]}`

### Jinja2 Variable Syntax

```jinja
# Simple variable
{{ cookiecutter.project_name }}

# Conditional
{% if cookiecutter.framework == 'pytorch' %}
torch
{% endif %}

# Comparison operators
==    # Equals
!=    # Not equals
<     # Less than
>     # Greater than
and   # Logical AND
or    # Logical OR
```

### Template Directory Naming

```
mlops-template/
├── cookiecutter.json        # Configuration file
└── {{cookiecutter.VAR}}/    # Directory name with variables
    ├── {{other_var}}_file.txt
    └── normal_file.txt
```

The directory name `{{cookiecutter.project_name}}` means:
- Users specify the project name
- Generated project gets that name
- All paths inside use that variable

---

## 🔧 Common Issues & Fixes

### Issue 1: Syntax Error in Jinja2

**Problem:**
```jinja
{% if cookiecutter.ml_framework = 'sklearn' %}  # ❌ Single = (assignment)
```

**Error:**
```
jinja2.exceptions.TemplateSyntaxError: expected token 'name', got 'assign'
```

**Fix:**
```jinja
{% if cookiecutter.ml_framework == 'sklearn' %}  # ✅ Double == (comparison)
```

### Issue 2: Missing endif

**Problem:**
```jinja
{% if cookiecutter.ml_framework == 'sklearn' %}
scikit-learn
{% elif cookiecutter.ml_framework == 'pytorch' %}
torch
# ❌ Missing {% endif %}
```

**Error:**
```
jinja2.exceptions.TemplateSyntaxError: unexpected end of template, expected 'endif'
```

**Fix:**
```jinja
{% if cookiecutter.ml_framework == 'sklearn' %}
scikit-learn
{% elif cookiecutter.ml_framework == 'pytorch' %}
torch
{% endif %}  # ✅ Add closing endif
```

### Issue 3: Variable Name Mismatch

**Problem:**
```
cookiecutter.json: "author": "xFusionCorp"
README.md: {{ cookiecutter.Author }}  # ❌ Capital A
```

**Result:**
```
Generated README: Created by .
```

**Fix:**
```
README.md: {{ cookiecutter.author }}  # ✅ Lowercase a
```

### Issue 4: Missing Choice Variable

**Problem:**
```json
{
    "project_name": "my-ml-project",
    // ❌ Missing "ml_framework"
}
```

```jinja
{% if cookiecutter.ml_framework == 'sklearn' %}  # ❌ Variable doesn't exist
scikit-learn
{% endif %}
```

**Error:**
```
UndefinedError: 'ml_framework' is undefined
```

**Fix:**
```json
{
    "project_name": "my-ml-project",
    "ml_framework": ["sklearn", "pytorch", "tensorflow"]  # ✅ Add variable
}
```

---

## 📋 Complete Corrected Files

### cookiecutter.json

```json
{
    "project_name": "my-ml-project",
    "author": "xFusionCorp",
    "python_version": "3.11",
    "ml_framework": ["sklearn", "pytorch", "tensorflow"]
}
```

### {{cookiecutter.project_name}}/requirements.txt

```jinja
{% if cookiecutter.ml_framework == 'sklearn' %}
scikit-learn
{% elif cookiecutter.ml_framework == 'pytorch' %}
torch
{% elif cookiecutter.ml_framework == 'tensorflow' %}
tensorflow
{% endif %}
```

### {{cookiecutter.project_name}}/README.md

```markdown
# {{cookiecutter.project_name}}

Created by {{cookiecutter.author}}.
```

---

## ✅ Task Checklist

- [ ] Navigated to `/root/code/mlops-template/`
- [ ] Reviewed current template files
- [ ] Identified all issues:
  - [ ] Missing `ml_framework` variable in cookiecutter.json
  - [ ] Using `=` instead of `==` in conditionals
  - [ ] Missing `{% endif %}`
  - [ ] Using `Author` instead of `author`
- [ ] Fixed cookiecutter.json with `ml_framework` choices
- [ ] Fixed requirements.txt with correct Jinja2 syntax
- [ ] Fixed README.md with correct variable names
- [ ] Created/verified directory structure (data/, models/, src/, tests/)
- [ ] Tested template rendering with test generation
- [ ] Generated project at `/root/code/churn-model/`
- [ ] Verified generated files:
  - [ ] requirements.txt contains `scikit-learn`
  - [ ] README.md mentions `xFusionCorp`
  - [ ] All directories exist (data/, models/, src/, tests/)

---

## 🎯 Verification Commands

```bash
# Validate cookiecutter.json syntax
python3 -c "import json; json.load(open('/root/code/mlops-template/cookiecutter.json'))"

# Test template rendering
cookiecutter /root/code/mlops-template/ \
  -o /tmp/verify \
  --no-input \
  project_name=verify-test \
  ml_framework=pytorch

# Check generated files
ls -la /tmp/verify/verify-test/
cat /tmp/verify/verify-test/requirements.txt  # Should show torch
cat /tmp/verify/verify-test/README.md

# Generate final project
cookiecutter /root/code/mlops-template/ \
  -o /root/code/ \
  --no-input \
  project_name=churn-model \
  ml_framework=sklearn

# Verify final project
ls -la /root/code/churn-model/
cat /root/code/churn-model/requirements.txt  # Should show scikit-learn
cat /root/code/churn-model/README.md  # Should mention xFusionCorp
```

---

## 💡 Tips for Cookiecutter Templates

### Interactive Mode vs No-Input

```bash
# Interactive (asks user for each variable)
cookiecutter /root/code/mlops-template/

# Non-interactive (uses defaults and provided values)
cookiecutter /root/code/mlops-template/ \
  --no-input \
  project_name=my-project \
  ml_framework=sklearn
```

### Useful Template Features

```jinja
# Loop over lists
{% for item in list %}
{{ item }}
{% endfor %}

# Case-insensitive comparison
{% if cookiecutter.framework|lower == 'pytorch' %}

# Default filter
{{ cookiecutter.optional_var | default('default_value') }}

# Uppercase/lowercase
{{ cookiecutter.project_name|upper }}
{{ cookiecutter.project_name|lower }}
```

### Post-generation Hooks

Advanced: Create `hooks/post_gen_project.py` to run after generation:

```python
#!/usr/bin/env python
import os

# Run commands after project generation
os.system('cd {{cookiecutter.project_name}} && git init')
print("Project initialized!")
```

---

## 🏆 Completion Status

**Task Status:** ✅ COMPLETED  
**Difficulty:** ⭐⭐⭐ Medium-Hard  
**Time Spent:** ~25-30 minutes

**What You've Accomplished:**
✓ Understood Cookiecutter template structure  
✓ Fixed JSON configuration with choices  
✓ Corrected Jinja2 conditional syntax  
✓ Fixed variable name references  
✓ Verified complete directory structure  
✓ Generated working ML project template  
✓ Learned project scaffolding best practices  

---

**Almost 10%! You're becoming a serious MLOps engineer! 🚀**

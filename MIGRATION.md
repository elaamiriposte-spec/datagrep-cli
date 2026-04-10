# Migration Guide: Positional vs Flag Style

## Overview

DataGrep v1.0+ supports **two complementary syntax styles**:
- **Positional Style** (legacy): `datagrep file.csv columns value`
- **Flag Style** (modern): `datagrep --file file.csv --columns columns --search value`

Both styles are **fully supported and compatible**. This guide helps you understand the differences and when to use each.

## Quick Comparison

| Feature | Positional | Flag |
|---------|-----------|------|
| **Syntax** | `datagrep file cols val` | `datagrep --file file --columns cols --search val` |
| **Argument Order** | Fixed | Flexible |
| **Self-Documenting** | No | Yes |
| **Typing Length** | Shorter | Longer |
| **Clarity in Scripts** | Less clear | More clear |
| **Backward Compat** | ✅ Yes | ✅ New |
| **Flags Take Precedence** | N/A | ✅ Yes |

## When to Use Each Style

### Use Positional Style When:
✅ Quick one-off commands  
✅ You're already familiar with CLI tools  
✅ Typing minimal commands  
✅ Working in short scripts  
✅ Familiar with existing datagrep usage  

**Example:**
```bash
datagrep data.csv name john
```

### Use Flag Style When:
✅ Writing production scripts  
✅ Collaborating with team members  
✅ Complex commands with many filters  
✅ Self-documentation is important  
✅ Reading code months later  
✅ Teaching others how to use datagrep  

**Example:**
```bash
datagrep --file data.csv --columns name --search john --ignore-case --output-format json
```

## Migration Examples

### Basic Search

**Before (Positional):**
```bash
datagrep data.csv name john
```

**After (Flag):**
```bash
datagrep --file data.csv --columns name --search john
```

### Multi-Column Search

**Before:**
```bash
datagrep data.csv "name,email" john
```

**After:**
```bash
datagrep --file data.csv --columns "name,email" --search john
```

### Case-Insensitive Search

**Before:**
```bash
datagrep data.csv email alice --ignore-case
```

**After:**
```bash
datagrep --file data.csv --columns email --search alice --ignore-case
```

### With Output Format

**Before:**
```bash
datagrep data.csv city london --output-format table --select "name,city,country"
```

**After:**
```bash
datagrep --file data.csv --columns city --search london --output-format table --select "name,city,country"
```

### With Filters and Sorting

**Before:**
```bash
datagrep data.csv name alice --where "age > 25" --sort name:asc --output-format json
```

**After:**
```bash
datagrep --file data.csv --columns name --search alice --where "age > 25" --sort name:asc --output-format json
```

### Inspection Mode

**Before:**
```bash
# Show schema and samples
datagrep data.csv

# Show first 5 rows
datagrep data.csv --sample 5

# Describe schema only
datagrep data.csv --describe

# Count records
datagrep data.csv --count
```

**After:**
```bash
# Show schema and samples
datagrep --file data.csv

# Show first 5 rows
datagrep --file data.csv --sample 5

# Describe schema only
datagrep --file data.csv --describe

# Count records
datagrep --file data.csv --count
```

### Empty/Not-Empty Filters

**Before:**
```bash
# Find records with empty phone
datagrep data.csv phone --empty

# Find records with non-empty phone
datagrep data.csv phone --not-empty
```

**After:**
```bash
# Find records with empty phone
datagrep --file data.csv --columns phone --empty

# Find records with non-empty phone
datagrep --file data.csv --columns phone --not-empty
```

### With stdin

**Before:**
```bash
cat data.csv | datagrep - name john
```

**After:**
```bash
cat data.csv | datagrep --file - --columns name --search john
```

Or (shorthand):
```bash
cat data.csv | datagrep --columns name --search john
```

### Default stdin

**Before:**
```bash
datagrep name john  # Reads from stdin
```

**After (same syntax works):**
```bash
datagrep --columns name --search john  # Reads from stdin
```

## Flexible Mixing

You can mix both styles - flags take precedence:

```bash
# File positional, search as flag
datagrep data.csv --search john

# File as flag, columns positional
datagrep --file data.csv "name,email" john

# All flags (most explicit and modern)
datagrep --file data.csv --columns name --search john
```

## Backward Compatibility

✅ **100% backward compatible** - all existing scripts work unchanged

All positional-style commands continue to work exactly as before:

```bash
# ✅ Still works
datagrep data.csv name john
datagrep data.csv "name,email" alice --ignore-case
datagrep data.csv city london --output-format table
```

## Argument Precedence

When both positional and flag versions are provided, **flags take precedence**:

```bash
# File positional is "old.csv", but flag is used instead
datagrep old.csv --file new.csv --columns name --search john
# → Searches in new.csv

# Columns positional is "email", but flag is used instead
datagrep data.csv email --columns name --search john
# → Searches in "name" column, not "email"
```

## FAQ

### Q: Do I need to migrate my scripts?
**A:** No! Positional style continues to work unchanged. Migrate when it makes sense for your use case.

### Q: Can I use both styles in the same script?
**A:** Yes! You can have some commands in positional style and others in flag style in the same script.

### Q: Which style should I use for production?
**A:** Flag style is recommended for production because it's more self-documenting and easier to maintain.

### Q: Are there performance differences?
**A:** No, both styles perform identically. It's purely a syntax choice.

### Q: What about shell completions?
**A:** Shell completions work with both styles. See [README.md](README.md#-shell-completion).

### Q: Can I mix styles in one command?
**A:** Yes! Positional arguments work alongside flags. Flags take precedence if both are provided.

```bash
# Mixed: file positional, other options as flags
datagrep data.csv --columns name --search john

# Mixed: some default positional, others flagged
datagrep data.csv "name,email" --search john
```

## Helper Tips

### Convert List of Commands

If you want to batch convert commands from positional to flag style:

**Bash one-liner to print flag style version:**
```bash
# Show what flag version looks like for a positional command
echo "Positional: datagrep data.csv name john"
echo "Flag style: datagrep --file data.csv --columns name --search john"
```

### Aliases for Your Preference

Create shell aliases if you want shorter forms:

```bash
# In ~/.bashrc or ~/.zshrc
alias dg="datagrep --file"
alias dgf="datagrep --file"

# Then use:
dg data.csv --columns name --search john
```

Or for positional style lovers:
```bash
# If you prefer positional style, keep using it!
# The alias isn't needed - just use datagrep normally
```

## See Also

- [README.md](README.md) - Full documentation
- [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) - Development guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contributing guide

## Feedback

If you have suggestions on the migration path or flag naming, please open an issue on GitHub!

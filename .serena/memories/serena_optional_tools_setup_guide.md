# Serena Optional Tools Setup Guide

## 🛠️ **How to Enable Optional Tools in Serena**

Based on the official Serena documentation, here's how to enable the optional tools you requested:

### **Configuration Method: `included_optional_tools`**

The optional tools are disabled by default and must be explicitly enabled using the `included_optional_tools` configuration parameter in one of these locations:

1. **Project-level configuration** (`.serena/project.yml`)
2. **Global configuration** (`~/.serena/serena_config.yml`)
3. **Custom modes/contexts** (YAML files in `~/.serena/`)

### **📋 List of Optional Tools to Enable:**

```yaml
included_optional_tools:
  - delete_lines
  - get_current_config
  - initial_instructions
  - insert_at_line
  - replace_lines
  - restart_language_server
  - summarize_changes
  - switch_modes
```

### **🔧 Configuration Options:**

#### **Option 1: Project-Level Configuration (Recommended)**

Edit `/WDLabs/CCB/.serena/project.yml`:

```yaml
# language of the project (csharp, python, rust, java, typescript, go, cpp, or ruby)
language: cpp

# Enable optional tools
included_optional_tools:
  - delete_lines
  - get_current_config
  - initial_instructions
  - insert_at_line
  - replace_lines
  - restart_language_server
  - summarize_changes
  - switch_modes
```

#### **Option 2: Global Configuration**

Edit `~/.serena/serena_config.yml`:

```yaml
included_optional_tools:
  - delete_lines
  - get_current_config
  - initial_instructions
  - insert_at_line
  - replace_lines
  - restart_language_server
  - summarize_changes
  - switch_modes
```

#### **Option 3: Custom Mode/Context**

Create a custom mode file in `~/.serena/` (e.g., `enhanced_mode.yml`):

```yaml
name: enhanced_mode
description: Enhanced mode with all optional tools enabled
included_optional_tools:
  - delete_lines
  - get_current_config
  - initial_instructions
  - insert_at_line
  - replace_lines
  - restart_language_server
  - summarize_changes
  - switch_modes
```

### **🚀 Tool Descriptions:**

- **`delete_lines`**: Deletes a range of lines within a file
- **`get_current_config`**: Prints current configuration including active projects, tools, contexts, and modes
- **`initial_instructions`**: Gets initial instructions for current project (useful when system prompt cannot be set)
- **`insert_at_line`**: Inserts content at a given line in a file
- **`replace_lines`**: Replaces a range of lines within a file with new content
- **`restart_language_server`**: Restarts language server (useful when edits not through Serena happen)
- **`summarize_changes`**: Provides instructions for summarizing changes made to codebase
- **`switch_modes`**: Activates modes by providing a list of their names

### **✅ Next Steps:**

1. Choose your preferred configuration method
2. Add the `included_optional_tools` section to your chosen config file
3. Restart Serena to apply the changes
4. Verify tools are available by asking Serena to show current configuration

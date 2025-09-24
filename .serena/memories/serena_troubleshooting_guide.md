# Serena Troubleshooting Guide - CCB Project

## Common Issues and Solutions

### Project Activation Issues

**Problem**: get_current_config shows wrong active project
**Solution**: This is a session-level display bug. Tools actually work correctly with CCB project.
**Verification**: Check that memories can be created and files can be accessed in CCB directory.

### Language Server Issues

**Problem**: clangd errors during indexing
**Solution**: Ensure clangd is properly installed:

```bash
sudo apt-get install clangd-12
sudo update-alternatives --install /usr/bin/clangd clangd /usr/bin/clangd-12 100
```

### Memory Location Issues

**Problem**: Memories being saved to wrong project
**Solution**: Verify project is properly registered in serena_config.yml and .serena/project.yml exists

### Tool Availability Issues

**Problem**: Optional tools not available
**Solution**: Check .serena/project.yml includes_optional_tools section

### Indexing Issues

**Problem**: Slow or failed indexing
**Solution**:

- Ensure clangd is installed and working
- Check for compile_commands.json (if needed)
- Use quick 10-second test: `timeout 10s uvx --from git+https://github.com/oraios/serena serena project index /WDLabs/CCB`

## Configuration Verification Commands

```bash
# Check current directory
pwd

# Check .serena directory exists
ls -la .serena/

# Check project configuration
cat .serena/project.yml

# Check global configuration
cat /home/1000211866/.serena/serena_config.yml

# Test indexing (quick test)
timeout 10s uvx --from git+https://github.com/oraios/serena serena project index /WDLabs/CCB
```

## Tool Testing Checklist

- [ ] get_current_config works
- [ ] list_dir shows CCB project structure
- [ ] find_file can locate files
- [ ] Memory operations work (list, read, write, delete)
- [ ] Symbol analysis works (get_symbols_overview, find_symbol)
- [ ] Pattern search works
- [ ] Mode switching works
- [ ] Language server restart works
- [ ] Optional tools are available
- [ ] Editing tools work (insert, replace, delete)

## Emergency Reset Procedure

If configuration gets corrupted:

1. Delete .serena directory: `rm -rf .serena/`
2. Re-run project setup
3. Re-enable optional tools
4. Re-run verification tests

feat: Update startup script documentation to prioritize working start-app-xterm.sh

- Update START_SCRIPT_README.md to prioritize start-app-xterm.sh as RECOMMENDED option
- Mark start-app.sh as BROKEN with clear warnings and DO NOT USE instructions
- Update README.md Quick Start section to use start-app-xterm.sh as primary option
- Update CLAUDE.md and AGENTS.md with consistent startup script recommendations
- Add status indicators: ✅ WORKING for start-app-xterm.sh, ❌ BROKEN for start-app.sh
- Include test validation results: "5/5 successful tests with Playwright validation"
- Fix gnome-terminal syntax in start-app.sh (-- to -e) but keep marked as broken
- Remove duplicate sections and fix linting errors in START_SCRIPT_README.md
- Add language specifications to fenced code blocks for markdown compliance
- Create Serena memories documenting startup script status and documentation updates

This ensures users are guided to the working start-app-xterm.sh script while keeping
the broken start-app.sh file for future debugging. All documentation is now consistent
across the project with clear warnings about the non-functional script.
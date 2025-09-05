# New Task Details

[GPT-5] Fix incorrectly setup Github MCP Server

## Task Description

<Task 1> Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Analyze, Investigate, & fix incorrectly setup GitHub MCP server

- There may have been an incorrect understanding when recently setting up the GitHub MCP server
- Investigate the current code to fix all incorrect code, tests and documentation to remove ALL references and usage of the CLI\UI for Github MCP Server
- Like most MCP servers in our project, MCP servers are mainly focused on the DEVELOPMENT ENVIRONMENT to enhance the workflow
- The ONLY MCP server that the end user CLI & UI code should use is the Polygon MCP server, which is already being used in our app by the AI Agent running the CLI and\or UI
- Github, Sequential-Thinking, Context7, Filesystem are all MCP servers in our project that is ONLY for DEVELOPMENT ENVIRONMENT and NOT for the end user
- It makes zero logical sense to have these development MCP servers being used during the app runtime itself because they have nothing to do with a Finance App

<Task 2> Specialist(s) to use Sequential-Thinking Tools to perform test usage of Github MCP Tools to confirm all the Github MCP tools are setup correctly, supported, and usable in the development environment

- Github MCP Tools will serve as the Primary Repo management tool, so we need it out first
- You can try to create some test branches, tags, commits, to test out the currently supported Github tools

- Since this is first time usage of Githhub MCp tools, there may be soem authentication steps needed

<Task 3> Specialist(s) to use Context7, Sequential-Thinking, Filesystem & any other relevant Tools to Analyze & update MCP_TOOL_USAGE_GUIDE.md, CLAUDE.md, & and any other project docs with newly added Github MCP Tools Support

- The Primary tool for Repo management should be Github, since our projects are stored on github repos
- The Secondary and\or Fail Safe toll for Repo management should be the existin git commands currently used frequently

<Closing_Tasks> Specialist(s) to use Context7, Sequential-Thinking, Filesystem, Github, & any other relevant Tools to perform 4x Final Steps for: Review\Fix Loop, Task Summary & CLAUDE.md Update, Atomic Github Commit & Github Push, & Final Verification

### Step 1: Review/Fix Loop

- Specialist performs comprehensive code review using `mcp__sequential-thinking__sequentialthinking` for systematic analysis
- Uses `mcp__filesystem__*` tools for all file operations and examination
- Optional `mcp__context7__resolve-library-id` + `mcp__context7__get-library-docs` calls if specific documentation/best practices needed for fixes
- Continue review/fix cycle until achieving PASSING code review status

### Step 2: Task Summary & CLAUDE.md Update

- Generate comprehensive task completion summary
- Update CLAUDE.md "Last Completed Task Summary" section between `<!-- LAST_COMPLETED_TASK_START -->` and `<!-- LAST_COMPLETED_TASK_END -->` markers
- Include all deliverables, changes made, and completion status
- This ensures task summary is included in the atomic commit

### Step 3: Atomic Git Commit & Push

- Run `git status` to review all staged and unstaged changes
- Create single atomic Github commit containing ALL changes: code files, documentation updates, and task summary
- Github Push commit to GitHub repository using provided personal access token
- **CRITICAL**: Must Github push to complete the workflow - Github commit without Github push is incomplete

### Step 4: Final Verification

- Run final `git status` to confirm successful commit and push
- Verify working tree is clean and branch is up-to-date with remote
- Confirm all changes are properly Github committed and Github pushed

**Key Requirements:**

## Requirements

## Expected Outcome

## Additional Context

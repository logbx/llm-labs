# Obsidian Usage Guide

This repository is structured as an [Obsidian](https://obsidian.md/) vault, which is a collection of interconnected markdown files that can be viewed and edited with any text editor, but offers enhanced features when opened in Obsidian.

## Wiki-Style Links

Throughout this vault, you'll find **wiki-style links** in the format `[[page-name]]`. These are Obsidian's internal linking syntax and work seamlessly within the Obsidian app.

### How to Read Wiki Links

If you're viewing these files outside of Obsidian:
- `[[workflows/current]]` → Navigate to `workflows/current.md`
- `[[tools/cursor]]` → Navigate to `tools/cursor.md`
- `[[templates/README]]` → Navigate to `templates/README.md`

Links with display text use the format `[[page-name|Display Text]]`:
- `[[templates/prd-prompt-template|Cursor PRD Template]]` → Links to `templates/prd-prompt-template.md` but shows as "Cursor PRD Template"

### Missing Link Targets

Some wiki links point to files that don't yet exist. This is intentional - they represent planned content or placeholders for future documentation. Known missing targets include:

**Tools:**
- `tools/context7.md` - Context7 integration (planned)
- `tools/claude-code.md` - Claude Code setup (planned)
- `tools/cursor.md` - Cursor IDE notes (planned)
- `tools/firebase.md` - Firebase integration (planned)
- `tools/bmat.md` - BMAT methodology (deprecated)

**Resources:**
- `resources/to-explore.md` - Reading list (planned)

**Notes:**
- `notes/lessons-learned.md` - Accumulated insights (planned)

**AI Drafts:**
- `ai-drafts/agentic-experiment.md` - Experiment log (planned)
- `ai-drafts/context-sync-test.md` - Context testing (planned)
- `ai-drafts/chatiq-stack-validation-example.md` - Stack validation example (planned)

**Workflows:**
- `workflows/current-setup.md` - Detailed setup (consolidated into `workflows/current.md`)

## Using This Vault in Obsidian

### First-Time Setup

1. **Install Obsidian**: Download from [obsidian.md](https://obsidian.md/)
2. **Open as Vault**: File → Open Folder as Vault → Select this directory
3. **Trust the Author**: Obsidian may ask about community plugins - this vault uses standard markdown only

### Recommended Settings

**For best experience:**
- Enable "Strict Line Breaks" (Settings → Editor → Strict Line Breaks)
- Enable "Readable Line Length" for comfortable reading
- Use "File Tree" view to see directory structure

### Key Features

When using Obsidian, you get:
- **Graph View**: Visualize connections between documents
- **Backlinks**: See all pages linking to the current page
- **Quick Switcher**: `Cmd/Ctrl + O` to quickly jump between files
- **Link Auto-complete**: Type `[[` to see available pages
- **Search**: `Cmd/Ctrl + Shift + F` to search across all files

## Viewing Without Obsidian

This vault works perfectly fine without Obsidian:
- All files are standard Markdown
- Read files with any text editor, IDE, or markdown viewer
- Navigate using your file browser or IDE's file tree
- Wiki links appear as `[[page-name]]` but you can mentally convert them to paths

## Contributing

When adding content:
- Use wiki-links for internal references: `[[path/to/file]]`
- Create actual files for important references
- Leave placeholder links for planned content
- Document missing targets in this file

## Learn More

- [Obsidian Documentation](https://help.obsidian.md/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Obsidian Community](https://obsidian.md/community)
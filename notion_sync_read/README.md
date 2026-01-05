# Notion Sync Read

A utility to export pages from a Notion database into Markdown files organized as per database properties with modular architecture.

## Prerequisites

- Python 3.8+
- A Notion integration API key with access to the target database
- Bash shell environment
- Dependencies: `notion-client`, `python-slugify`, `python-dotenv`, `decouple`, `uv` (for package management)

## Configuration

The script requires a `.env` file with these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `NOTION_API_KEY` | Notion integration token | Required |
| `NOTION_DATABASE_ID` | The database containing pages to export | Required |
| `OUTPUT_DIR` | Output directory for Markdown files | `docs/notion_export` |
| `SUBFOLDER_KEY` | Database property used for subfolder organization | `stage` |

## Architecture

The project follows a modular structure:

- **sync_notion_export.py**: Main orchestration script that coordinates the export pipeline
- **constants.py**: Configuration management and environment variable loading
- **converter.py**: Converts Notion blocks to Markdown format
- **extract_properties.py**: Extracts and processes page properties from Notion pages
- **run_notion_export.sh**: Bash wrapper that manages dependencies and execution

## What It Does

1. **Queries the Notion database** - Uses Notion data sources API to fetch all pages with pagination
2. **Extracts page properties** - Retrieves all properties from each page (title, stage, description, etc.)
3. **Fetches blocks** - Retrieves all blocks (content) from each page
4. **Converts to Markdown** - Transforms supported Notion block types to Markdown format
5. **Organizes by property** - Organizes output files into subfolders based on `SUBFOLDER_KEY` property
6. **Generates frontmatter** - Adds metadata to each file with all extracted properties

### Output Structure

```
OUTPUT_DIR/
├── stage1/
│   ├── page_title_1.md
│   └── page_title_2.md
└── stage2/
    └── page_title_3.md
```

Each Markdown file includes:
- **Title** as H1 heading
- **Frontmatter** with all page properties (uppercase keys)
- **Content** with converted blocks in Markdown format

## Supported Block Types

The converter supports the following Notion block types:
- Headings (all levels)
- Paragraphs
- Lists (bulleted and numbered)
- Quotes
- Code blocks
- Callouts
- Tables (basic)

Unsupported blocks are skipped without error.

## Step-by-Step Usage

1. **Copy the shell script to your working directory:**
   ```bash
   cp run_notion_export.sh /path/to/your/project/
   ```

2. **Create a `.env` file with required configuration:**
   ```bash
   NOTION_API_KEY=your_notion_api_key_here
   NOTION_DATABASE_ID=your_database_id_here
   OUTPUT_DIR=docs/notion_export
   SUBFOLDER_KEY=stage
   ```

3. **Run the automation:**
   ```bash
   chmod +x run_notion_export.sh
   ./run_notion_export.sh
   ```

4. **Access the exported files** - Find your organized Markdown files in `OUTPUT_DIR` grouped by the property specified in `SUBFOLDER_KEY`

## Notes & Troubleshooting

- **No data sources found**: The script requires that your Notion database has a configured data source. Error: `"No data_sources found on database"`
- **Missing SUBFOLDER_KEY property**: If the specified property doesn't exist or has no value, files are saved directly to `OUTPUT_DIR` without subfolder organization
- **Dependency installation**: The script uses `uv pip` for fast dependency installation. If `uv` is not available, it will fail
- **File cleanup**: On success, temporary files are automatically cleaned up. On failure, files are kept in the working directory for debugging
- **Property extraction**: All page properties are automatically extracted and included in the frontmatter, regardless of type

## Environment Variables Details

### SUBFOLDER_KEY

Controls which database property is used for organizing exported files into subfolders. For example:
- `SUBFOLDER_KEY=stage` - Organizes by Stage property
- `SUBFOLDER_KEY=project` - Organizes by Project property
- `SUBFOLDER_KEY=category` - Organizes by Category property

If a page's property value is empty/null, the file is saved to the root output directory.

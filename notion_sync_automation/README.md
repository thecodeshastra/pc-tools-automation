# Notion Sync Automation

A small utility to export pages from a Notion database into Markdown files organized as per database data.

**Prerequisites**
- Python 3.8+
- A Notion integration API key with access to the target database.
- Bash shell environment.

**Configuration**
The script requires a `.env` file with these environment variables:

- `NOTION_API_KEY`: Notion integration token.
- `NOTION_DATABASE_ID`: The database containing the pages to export.
- `OUTPUT_DIR`: Where Markdown files will be written (default: `docs/notion_export`).

The script will automatically:
- Copy required Python files from the source repository.
- Install dependencies.
- Run the exporter.
- Clean up temporary files on successful completion.

**What it does**
- Queries the Notion database's data source and paginates through all pages.
- For each page, it fetches the blocks and converts supported block types into Markdown.
- Writes one Markdown file per Notion page under `OUTPUT_DIR/<Stage>/<slugified-title>.md`.
- Each file includes a small frontmatter containing `STAGE`, `DESCRIPTION`, `PAGE_ID`, and `SOURCE`.

**Step-by-step guide**
1. Copy `run_notion_export.sh` to your working directory.
2. Create a `.env` file with `NOTION_API_KEY` and `NOTION_DATABASE_ID` (see Configuration above).
3. Run the script:

```bash
chmod +x run_notion_export.sh
./run_notion_export.sh
```

4. After the run completes, open the `OUTPUT_DIR` (default `docs/notion_export`) to find the exported Markdown files grouped by `Stage`.

**Notes & troubleshooting**
- If the database has no `data_sources` set, the script will raise: "No data_sources found on database".
- The converter supports headings, paragraphs, lists, quotes, code blocks, callouts and simple tables. Unsupported blocks are skipped.
- Use the `OUTPUT_DIR` env var to control where files are saved.

If you want, I can also add a simple example `.env.example` and a CI job snippet to automate exports.

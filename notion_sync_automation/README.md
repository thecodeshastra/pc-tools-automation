# Notion Sync Automation

A small utility to export pages from a Notion database into Markdown files organized as per database data.

**Use Cases**
- Backup Notion documentation as Markdown for version control.
- Publish Notion content to a static site or documentation site.
- Generate readable Markdown notes from Notion pages for editors or CI workflows.

**Prerequisites**
- Python 3.8+
- A Notion integration API key with access to the target database.

**Install**
1. From the repository root, install dependencies:

```bash
pip install -r notion-sync-automation/requirements.txt
```

**Configuration**
Create a `.env` file in the project root (or export environment variables) with the following keys:

```
NOTION_API_KEY=your_notion_integration_token
NOTION_DATABASE_ID=your_database_id
OUTPUT_DIR=docs/notion_export
```

- `NOTION_API_KEY`: Notion integration token.
- `NOTION_DATABASE_ID`: The database containing the pages to export.
- `OUTPUT_DIR`: Where Markdown files will be written (default: `docs/notion_export`).

The code uses `NOTION` client from `notion_client` and reads those values via `python-decouple`/`.env`.

**What it does**
- Queries the Notion database's data source and paginates through all pages.
- For each page, it fetches the blocks and converts supported block types into Markdown.
- Writes one Markdown file per Notion page under `OUTPUT_DIR/<Stage>/<slugified-title>.md`.
- Each file includes a small frontmatter containing `STAGE`, `DESCRIPTION`, `PAGE_ID`, and `SOURCE`.

**Step-by-step guide**
1. Ensure dependencies are installed (`pip install -r notion-sync-automation/requirements.txt`).
2. Create a `.env` with `NOTION_API_KEY` and `NOTION_DATABASE_ID` (see Configuration above).
3. Run the exporter from the project root:

```bash
python -m notion_sync_automation.sync_notion_export
```

Alternatively, run the script directly from its folder:

```bash
cd notion-sync-automation
python sync_notion_export.py
```

4. After the run completes, open the `OUTPUT_DIR` (default `docs/notion_export`) to find the exported Markdown files grouped by `Stage`.

**Notes & troubleshooting**
- If the database has no `data_sources` set, the script will raise: "No data_sources found on database".
- The converter supports headings, paragraphs, lists, quotes, code blocks, callouts and simple tables. Unsupported blocks are skipped.
- Use the `OUTPUT_DIR` env var to control where files are saved.

**Files of interest**
- `notion-sync-automation/sync_notion_export.py` — main exporter.
- `notion-sync-automation/converter.py` — converts Notion blocks to Markdown.
- `notion-sync-automation/constants.py` — env and constants (defaults and frontmatter generator).

If you want, I can also add a simple example `.env.example` and a CI job snippet to automate exports.

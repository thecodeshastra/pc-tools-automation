"""Notion export automation"""

# python modules
import os
import json

# import json
import shutil

# third party modules
from slugify import slugify

# notion_sync_automation modules
from notion_sync_automation.constants import (
    NOTION,
    OUTPUT_DIR,
    DATABASE_ID,
    SUBFOLDER_KEY,
    generate_frontmatter,
)
from notion_sync_automation.converter import block_to_md
from notion_sync_automation.extract_properties import extract_all_property_value

# constants


def get_data_source_id(database_id: str) -> str:
    """Get the data source ID for the given database ID

    Args:
        database_id (str): The database ID

    Returns:
        str: The data source ID
    """
    # retrieve database metadata
    database = NOTION.databases.retrieve(database_id=database_id)
    # extract data source ID
    data_sources = database.get("data_sources", [])
    if not data_sources:
        raise RuntimeError("No data_sources found on database")
    return data_sources[0]["id"]


def fetch_database_pages() -> list:
    """Fetch all pages from the database

    Returns:
        list: List of pages
    """
    pages = []
    cursor = None
    # get data source id
    data_source_id = get_data_source_id(DATABASE_ID)
    # paginate through all pages
    while True:
        response = NOTION.data_sources.query(
            data_source_id=data_source_id, start_cursor=cursor
        )
        pages.extend(response["results"])
        # break if no more pages
        if not response["has_more"]:
            break
        # cursor for next page
        cursor = response["next_cursor"]

    return pages


def fetch_blocks(page_id: str) -> list:
    """Fetch all blocks from the page

    Args:
        page_id (str): The ID of the page to fetch blocks from

    Returns:
        list: List of blocks
    """
    blocks = []
    cursor = None

    while True:
        res = NOTION.blocks.children.list(block_id=page_id, start_cursor=cursor)
        blocks.extend(res["results"])

        if not res["has_more"]:
            break
        cursor = res["next_cursor"]

    return blocks


def reset_output_dir(output_dir: str) -> None:
    """Reset the output directory

    Args:
        output_dir (str): The output directory to reset
    """
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)


def save_temp_data(
    page: dict, blocks: list, output_dir: str = "temp/notion_export"
) -> None:
    """Save the page and blocks to a temporary directory

    Args:
        output_dir (str): The output directory
        page (dict): The page to save
        blocks (list): The blocks to save
    """
    # create temp directory
    temp_dir = os.path.join(output_dir, page["id"])
    os.makedirs(temp_dir, exist_ok=True)
    # save page data as json files
    with open(os.path.join(temp_dir, "page.json"), "w", encoding="utf-8") as f:
        json.dump(page, f, indent=2)
    # save blocks data as json files
    with open(os.path.join(temp_dir, "blocks.json"), "w", encoding="utf-8") as f:
        json.dump(blocks, f, indent=2)


def export_page(page: dict) -> None:
    """Export a page to the output directory

    Args:
        page (dict): The page to export
    """
    # get page metadata
    page_id = page["id"]
    # get all properties
    all_properties = extract_all_property_value(page)
    title = all_properties["title"]
    title = slugify(title, separator="_")
    # fetch blocks
    blocks = fetch_blocks(page_id)

    # # save temp data
    # save_temp_data(page, blocks)

    # write to markdown file
    # generate output directory if not exists
    if all_properties[SUBFOLDER_KEY] is None:
        sub_dir = OUTPUT_DIR
    else:
        sub_dir = os.path.join(OUTPUT_DIR, all_properties[SUBFOLDER_KEY])
        os.makedirs(sub_dir, exist_ok=True)
    # generate file path
    output_md = os.path.join(sub_dir, f"{title}.md")
    # open the file in write mode
    with open(output_md, "w", encoding="utf-8") as f:
        # write title as H1
        f.write(f"# {title}\n")
        # write frontmatter
        f.write(generate_frontmatter(all_properties))
        # loop through blocks and convert to markdown
        for block in blocks:
            line = block_to_md(block)
            if line:
                # if line is not empty, write to file
                f.write(line + "\n\n")
    # print success message
    print(f"✔ Exported: {title}")


def main() -> None:
    """Main function"""
    # reset output directory first
    reset_output_dir(OUTPUT_DIR)
    # fetch all pages from the database
    pages = fetch_database_pages()
    # loop through each page and export
    for page in pages:
        export_page(page)


if __name__ == "__main__":
    main()

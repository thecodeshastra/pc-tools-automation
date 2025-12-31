"""All constants for Notion Sync Automation"""

from notion_client import Client
from decouple import config
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# constants for Notion Sync Automation
NOTION_API_KEY= config("NOTION_API_KEY", default="Notion API Key not set")
DATABASE_ID = config("NOTION_DATABASE_ID", default="Notion Database ID not set")
OUTPUT_DIR = config("OUTPUT_DIR", default="docs/notion_export")
NOTION = Client(auth=NOTION_API_KEY)


def generate_frontmatter(stage: str, description: str, page_id: str) -> str:
    """Generate frontmatter for the markdown file
    Args:
        stage (str): The stage of the page
        description (str): The description of the page
        page_id (str): The Notion page ID
    Returns:
        str: The frontmatter string
    """
    return f"""---
STAGE: {stage}
DESCRIPTION: {description}
PAGE_ID: {page_id}
SOURCE: notion
---

"""

"""All constants for Notion Sync Automation"""

from notion_client import Client
from decouple import config
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# constants for Notion Sync Automation
NOTION_API_KEY = config("NOTION_API_KEY", default="Notion API Key not set")
DATABASE_ID = config("NOTION_DATABASE_ID", default="Notion Database ID not set")
OUTPUT_DIR = config("OUTPUT_DIR", default="docs/notion_export")
NOTION = Client(auth=NOTION_API_KEY)
SUBFOLDER_KEY = config("SUBFOLDER_KEY", default="stage")


class PropertyType:
    """Constants for Notion property types

    """
    TITLE = "title"
    SELECT = "select"
    RICH_TEXT = "rich_text"
    PLAIN_TEXT = "plain_text"
    TYPE = "type"
    MULTI_SELECT = "multi_select"
    NUMBER = "number"
    DATE = "date"
    PEOPLE = "people"
    STATUS = "status"
    PLACE = "place"
    CHECKBOX = "checkbox"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    LAST_EDITED_BY = "last_edited_by"
    CREATED_BY = "created_by"
    LAST_EDITED_TIME = "last_edited_time"
    CREATED_TIME = "created_time"
    FORMULA = "formula"
    ROLLUP = "rollup"
    FILES = "files"
    RELATION = "relation"


def generate_frontmatter(all_properties: dict) -> str:
    """Generate frontmatter for the markdown file
    Args:
        all_properties (dict): The properties of the page
    Returns:
        str: The frontmatter string
    """
    final_formatter = ""
    for key, value in all_properties.items():
        if key == "title":
            continue
        if isinstance(value, list):
            value = ", ".join(value)
        elif isinstance(value, bool):
            value = str(value).lower()
        elif isinstance(value, (int, float)):
            value = str(value)
        final_formatter += f"{key.upper()}: {value}\n"
    return final_formatter + "\n---\n\n"

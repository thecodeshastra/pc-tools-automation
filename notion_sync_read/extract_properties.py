"""
Docstring for notion_sync_automation.extract_properties
"""

# notion_sync_automation module
from notion_sync_read.constants import PropertyType


def extract_all_property_value(page: dict) -> dict:
    """Extract the stage ID from the page

    Args:
        page (dict): The page to extract the stage ID from

    Returns:
        dict: All properties of the page
    """
    prop = page["properties"]
    default_value = None
    if not prop:
        return {}
    all_properties = {}
    for key, value in prop.items():
        if value[PropertyType.TYPE] == PropertyType.TITLE:
            if value[PropertyType.TITLE] is not None:
                if len(value[PropertyType.TITLE]) > 1:
                    title = "_".join(
                        [t[PropertyType.PLAIN_TEXT] for t in value[PropertyType.TITLE]]
                    )
                else:
                    title = value[PropertyType.TITLE][0][PropertyType.PLAIN_TEXT]
            else:
                title = "Untitled"
            all_properties[key] = title
            all_properties[PropertyType.TITLE] = title
        elif value[PropertyType.TYPE] == PropertyType.SELECT:
            if value[PropertyType.SELECT] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.SELECT]["name"]
        elif value[PropertyType.TYPE] == PropertyType.RICH_TEXT:
            if (
                value[PropertyType.RICH_TEXT] is default_value
                or len(value[PropertyType.RICH_TEXT]) == 0
            ):
                all_properties[key] = ""
            else:
                all_properties[key] = value[PropertyType.RICH_TEXT][0][
                    PropertyType.PLAIN_TEXT
                ]
        elif value[PropertyType.TYPE] == PropertyType.MULTI_SELECT:
            if (
                value[PropertyType.MULTI_SELECT] is default_value
                or len(value[PropertyType.MULTI_SELECT]) == 0
            ):
                all_properties[key] = []
            else:
                all_properties[key] = [
                    v["name"] for v in value[PropertyType.MULTI_SELECT]
                ]
        elif value[PropertyType.TYPE] == PropertyType.NUMBER:
            if value[PropertyType.NUMBER] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.NUMBER]
        elif value[PropertyType.TYPE] == PropertyType.DATE:
            if value[PropertyType.DATE] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.DATE]["start"]
        elif value[PropertyType.TYPE] == PropertyType.PEOPLE:
            if (
                value[PropertyType.PEOPLE] is default_value
                or len(value[PropertyType.PEOPLE]) == 0
            ):
                all_properties[key] = []
            else:
                all_properties[key] = [v["name"] for v in value[PropertyType.PEOPLE]]
        elif value[PropertyType.TYPE] == PropertyType.STATUS:
            if value[PropertyType.STATUS] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.STATUS]["name"]
        elif value[PropertyType.TYPE] == PropertyType.PLACE:
            if value[PropertyType.PLACE] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.PLACE]["name"]
        elif value[PropertyType.TYPE] == PropertyType.CHECKBOX and isinstance(
            value[PropertyType.CHECKBOX], bool
        ):
            all_properties[key] = value[PropertyType.CHECKBOX]
        elif value[PropertyType.TYPE] == PropertyType.CREATED_TIME:
            if value[PropertyType.CREATED_TIME] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.CREATED_TIME]
        elif value[PropertyType.TYPE] == PropertyType.URL:
            if value[PropertyType.URL] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.URL]
        elif value[PropertyType.TYPE] == PropertyType.EMAIL:
            if value[PropertyType.EMAIL] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.EMAIL]
        elif value[PropertyType.TYPE] == PropertyType.PHONE_NUMBER:
            if value[PropertyType.PHONE_NUMBER] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.PHONE_NUMBER]
        elif value[PropertyType.TYPE] == PropertyType.LAST_EDITED_BY:
            if value[PropertyType.LAST_EDITED_BY] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.LAST_EDITED_BY]["name"]
        elif value[PropertyType.TYPE] == PropertyType.CREATED_BY:
            if value[PropertyType.CREATED_BY] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.CREATED_BY]["name"]
        elif value[PropertyType.TYPE] == PropertyType.LAST_EDITED_TIME:
            if value[PropertyType.LAST_EDITED_TIME] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.LAST_EDITED_TIME]
        elif value[PropertyType.TYPE] == PropertyType.CREATED_TIME:
            if value[PropertyType.CREATED_TIME] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.CREATED_TIME]
        elif value[PropertyType.TYPE] == PropertyType.FORMULA:
            if value[PropertyType.FORMULA] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.FORMULA]["number"]
        elif value[PropertyType.TYPE] == PropertyType.ROLLUP:
            if value[PropertyType.ROLLUP] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.ROLLUP]["number"]
        elif value[PropertyType.TYPE] == PropertyType.FILES:
            if value[PropertyType.FILES] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.FILES]["name"]
        elif value[PropertyType.TYPE] == PropertyType.RELATION:
            if value[PropertyType.RELATION] is default_value:
                all_properties[key] = default_value
            else:
                all_properties[key] = value[PropertyType.RELATION]["id"]
        else:
            all_properties[key] = value
    return all_properties

"""Convert Notion blocks to Markdown format"""


def rich_text_to_md(rich_text: list) -> str:
    """
    Convert Notion rich_text array into Markdown,
    preserving inline annotations (bold, italic, code, etc.)

    Args:
        rich_text (list): List of rich_text objects from Notion
    Returns:
        str: The markdown representation of the rich text
    """
    if not rich_text:
        return ""

    parts = []

    for span in rich_text:
        text = span.get("plain_text", "")
        ann = span.get("annotations", {})

        # Inline code has highest priority
        if ann.get("code"):
            text = f"`{text}`"

        # Bold + italic combinations
        if ann.get("bold") and ann.get("italic"):
            text = f"***{text}***"
        elif ann.get("bold"):
            text = f"**{text}**"
        elif ann.get("italic"):
            text = f"*{text}*"

        # Strikethrough
        if ann.get("strikethrough"):
            text = f"~~{text}~~"

        # Underline (Markdown has no native underline; keep readable)
        if ann.get("underline"):
            text = f"<u>{text}</u>"

        # Links
        if span.get("href"):
            text = f"[{text}]({span['href']})"
        # mentions
        if span["type"] == "mention":
            mention = span["mention"]

            if mention["type"] == "page":
                text = f"@{mention['page']['id']}"

            elif mention["type"] == "user":
                text = "@user"

            elif mention["type"] == "date":
                text = mention["date"].get("start", "")

        parts.append(text)

    return "".join(parts)


def table_to_md(block: dict) -> str | None:
    """
    table_to_md converts a Notion table block to Markdown format.
    
    Args:
        block (dict): The table block to convert
    Returns:
        str | None: The markdown representation of the table or None if empty
    """
    rows = block.get("children", [])
    table = []

    for row in rows:
        cells = row["table_row"]["cells"]
        table.append([" ".join(r["plain_text"] for r in cell) for cell in cells])

    if not table:
        return None

    header = "| " + " | ".join(table[0]) + " |"
    divider = "| " + " | ".join("---" for _ in table[0]) + " |"

    lines = [header, divider]

    for row in table[1:]:
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


def block_to_md(block: dict, indent: int = 0) -> str | None:
    """
    Convert a Notion block to Markdown format.

    Args:
        block (dict): The Notion block to convert
        indent (int): The indentation level for nested blocks
    Returns:
        str | None: The markdown representation of the block or None if unsupported
    """
    t = block["type"]
    b = block[t]
    prefix = " " * indent

    if t == "heading_1":
        return "# " + rich_text_to_md(b["rich_text"])

    if t == "heading_2":
        return "## " + rich_text_to_md(b["rich_text"])

    if t == "heading_3":
        return "### " + rich_text_to_md(b["rich_text"])

    if t == "paragraph":
        text = rich_text_to_md(b["rich_text"])
        return text if text else None

    if t == "bulleted_list_item":
        return f"{prefix}- {rich_text_to_md(b['rich_text'])}"

    if t == "numbered_list_item":
        return f"{prefix}1. {rich_text_to_md(b['rich_text'])}"

    if t == "quote":
        return f"{prefix}> {rich_text_to_md(b['rich_text'])}"

    if t == "code":
        lang = b.get("language", "")
        code = rich_text_to_md(b["rich_text"])
        return f"{prefix} ```{lang}\n{code}\n```"

    if t == "divider":
        return "---"

    if t == "callout":
        icon = b.get("icon", {}).get("emoji", "")
        text = rich_text_to_md(b["rich_text"])
        return f"{prefix} > {icon} {text}"

    if t == "table":
        return table_to_md(block)

    return None

"""
Calibre MCP

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

import os
import subprocess

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Calibre")

# Get ENV variables
calibre_base_url = os.environ.get("CALIBRE_BASE_URL", "http://localhost:8080")
calibre_library_id = os.environ.get("CALIBRE_LIBRARY_ID", "Library")

calibre_url = f"{calibre_base_url}/#{calibre_library_id}"


# Add an addition tool
@mcp.tool()
def listBooks(
    fields: list[str] = ["title", "authors"],
    sortBy: str = "title",
    limit: str = "all",
    ascending: bool = True,
) -> str:
    """
    List all books in the Calibre library.

    Available fields: author_sort, authors, comments, cover, formats,
    identifiers, isbn, languages, last_modified, pubdate, publisher, rating,
    series, series_index, size, tags, template, timestamp, title, uuid

    Args
        fields (list[str]): List of fields to include in the output.
        sortBy (str): Field to sort the output by.
        limit (str): Number of results to return. Use "all" for no limit.
        ascending (bool): Whether to sort in ascending order.
    """

    command_list = [
        "calibredb",
        "--with-library",
        "http://localhost:8080/#Library",
        "list",
        "--fields",
        ",".join(fields),
        "--sort-by",
        sortBy,
    ]

    if limit != "all":
        command_list.append("--limit")
        command_list.append(limit)

    if ascending:
        command_list.append("--ascending")

    calibre_list = subprocess.check_output(
        command_list,
        text=True,
    )
    return calibre_list


if __name__ == "__main__":
    mcp.run()  # defaults to stdio transport

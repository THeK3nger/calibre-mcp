"""
Calibre MCP

To start the server run

    uv run mcp dev server.py
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
        calibre_url,
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


@mcp.tool()
def searchBooks(
    query: str, limit: str = "all", return_fields: list[str] = ["title", "authors"]
) -> str:
    """
    Search books in the Calibre library using Calibre's search query language.

    The search query supports Calibre's powerful search syntax including:
    - Simple text: "robot" (searches all fields)
    - Field-specific: author:asimov, title:"i robot", tag:fiction
    - Boolean operators: author:asimov AND title:foundation
    - Wildcards: author:asim*
    - Date ranges: pubdate:>2020, date:2010..2020
    - Numeric comparisons: rating:>3, series_index:=1
    - Regular expressions: title:~".*robot.*"
    - Negation: NOT author:asimov, -tag:fiction

    Available search fields: author, title, tag, series, publisher, pubdate,
    rating, language, identifier, format, comments, cover, date, size, etc.

    Args:
        query (str): Search expression using Calibre's query language
        limit (str): Maximum number of book IDs to return. Use "all" for no limit
        return_fields (list[str]): Fields to include when displaying results

    Returns:
        str: Comma-separated list of matching book IDs and their details
    """

    # First get the book IDs that match the search
    search_command = ["calibredb", "--with-library", calibre_url, "search", query]

    if limit != "all":
        search_command.extend(["--limit", limit])

    try:
        # Get matching book IDs
        search_result = subprocess.check_output(
            search_command,
            text=True,
        ).strip()

        if not search_result:
            return "No books found matching the search criteria."

        # Get detailed information for the matching books
        list_command = [
            "calibredb",
            "--with-library",
            calibre_url,
            "list",
            "--fields",
            ",".join(return_fields),
            "--search",
            query,
        ]

        if limit != "all":
            list_command.extend(["--limit", limit])

        detailed_result = subprocess.check_output(
            list_command,
            text=True,
        )

        return f"Found {len(search_result.split(','))} matching books:\n\n{detailed_result}"

    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return "No books found matching the search criteria."
        return f"Error executing search: {e}"


if __name__ == "__main__":
    mcp.run()  # defaults to stdio transport

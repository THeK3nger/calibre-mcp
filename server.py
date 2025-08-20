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


@mcp.tool()
def fullTextSearch(
    search_expression: str,
    include_snippets: bool = False,
    restrict_to: str = "",
    output_format: str = "text",
    exact_words_only: bool = False,
    match_start_marker: str = "<<",
    match_end_marker: str = ">>",
) -> str:
    """
    Perform a full text search on the entire Calibre library or a subset of books.

    This searches within the actual content of books (e.g., inside EPUB files),
    not just metadata like title, author, etc. Requires the library to be indexed.

    Args:
        search_expression (str): The text to search for within book contents
        include_snippets (bool): Include text snippets around matches (slower but more informative)
        restrict_to (str): Restrict search to specific books using search expression or IDs
                          Examples: "ids:1,2,3" or "search:tag:fiction"
        output_format (str): Output format - "text" for plain text or "json" for JSON
        exact_words_only (bool): Only match exact words, not related words
        match_start_marker (str): Marker for start of matched words in snippets
        match_end_marker (str): Marker for end of matched words in snippets

    Returns:
        str: Full text search results with book matches and optional snippets
    """

    command_list = [
        "calibredb",
        "--with-library",
        calibre_url,
        "fts_search",
    ]

    if include_snippets:
        command_list.append("--include-snippets")

    if exact_words_only:
        command_list.append("--do-not-match-on-related-words")

    if restrict_to:
        command_list.extend(["--restrict-to", restrict_to])

    if output_format:
        command_list.extend(["--output-format", output_format])

    if match_start_marker != "<<":
        command_list.extend(["--match-start-marker", match_start_marker])

    if match_end_marker != ">>":
        command_list.extend(["--match-end-marker", match_end_marker])

    command_list.append(search_expression)

    try:
        result = subprocess.check_output(
            command_list,
            text=True,
        )
        return result.strip() if result.strip() else "No full text matches found."

    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return "No full text matches found."
        return f"Error executing full text search: {e}"


@mcp.tool()
def showDetails(book_id: str) -> str:
    """
    Show detailed metadata for a specific book by its ID.

    This retrieves comprehensive metadata information for a single book
    including title, authors, tags, series information, file formats,
    publication details, and more.

    Args:
        book_id (str): The unique ID of the book in the Calibre library

    Returns:
        str: Detailed metadata information for the specified book
    """

    command_list = [
        "calibredb",
        "--with-library",
        calibre_url,
        "show_metadata",
        book_id,
    ]

    try:
        result = subprocess.check_output(
            command_list,
            text=True,
        )
        return result.strip()

    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return f"Book with ID '{book_id}' not found in the library."
        return f"Error retrieving book details: {e}"


if __name__ == "__main__":
    mcp.run()  # defaults to stdio transport

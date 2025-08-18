# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Calibre MCP (Model Context Protocol) server that provides an interface to interact with a Calibre library via the Calibre Content Server. The project is written in Python and uses the FastMCP framework to expose Calibre functionality as MCP tools.

## Development Setup

The project uses `uv` as the package manager and requires Python 3.10+.

### Common Commands

- **Run the MCP server in development mode**: `uv run mcp dev server.py`
- **Install the MCP server**: `uv run mcp install server.py`
- **Install dependencies**: `uv sync`
- **Run a command in the project environment**: `uv run <command>`

### Environment Variables

The server requires two environment variables to connect to Calibre:
- `CALIBRE_BASE_URL`: Base URL of the Calibre Content Server (default: "http://localhost:8080")
- `CALIBRE_LIBRARY_ID`: Library ID in Calibre (default: "Library")

## Architecture

The project consists of a single Python file (`server.py`) that:

1. **MCP Server Setup**: Creates a FastMCP server instance named "Calibre"
2. **Environment Configuration**: Reads Calibre connection settings from environment variables
3. **Tool Implementation**: Exposes two main tools:
   - `listBooks`: Lists books with configurable fields, sorting, and limits
   - `searchBooks`: Searches books using Calibre's query language with Boolean operators, wildcards, and field-specific searches

### Key Dependencies

- **mcp[cli]**: The MCP framework for creating server tools
- **calibredb**: External command-line tool (part of Calibre) used for all library operations

### Tool Design Pattern

Both tools follow the same pattern:
1. Construct `calibredb` command with appropriate flags
2. Execute via `subprocess.check_output`
3. Return formatted results or error messages

The server acts as a wrapper around `calibredb` commands, providing structured access to Calibre functionality through the MCP protocol.

## Calibre Integration

The server communicates with Calibre through:
- **Calibre Content Server**: Must be running and accessible
- **calibredb CLI**: Used for all database operations
- **Library URL format**: `{base_url}/#{library_id}`

Available search fields include: author, title, tag, series, publisher, pubdate, rating, language, identifier, format, comments, cover, date, size.